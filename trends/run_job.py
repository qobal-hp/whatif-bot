"""Process every ZIP in trends/inbox: validate -> ElevenLabs narration -> render -> QC report.

usage: python trends/run_job.py <inbox dir> <output dir>
For each ZIP writes <output dir>/<job_id>/: video.mp4, thumbnail.png, upload.json, report.md, contact_sheet.jpg
Nothing is uploaded to YouTube here.
"""
import json, shutil, subprocess, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "lib"))
from validate import validate  # noqa: E402
import render  # noqa: E402


def safe_extract(zp, dest):
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zp) as z:
        for m in z.infolist():
            name = Path(m.filename).name  # flatten: only top-level files are used
            if m.is_dir() or not name or name.startswith("."):
                continue
            if name in {"production.json", "facts.json", "script.md", "thumbnail.png", "trends_screenshot.png"}:
                with z.open(m) as src, open(dest / name, "wb") as dst:
                    shutil.copyfileobj(src, dst)


def report(path, job_id, val, qc, tts_log):
    L = [f"# {job_id}", ""]
    ok = not val["errors"] and not (qc or {}).get("errors")
    L.append("**Status: " + ("READY FOR REVIEW" if ok else "NEEDS FIXES") + "**\n")
    if qc:
        L.append(f"- Length: {qc.get('duration')} s (speed {qc.get('speed')}x)")
        L.append(f"- First 0.30 s vs thumbnail (mean pixel diff): {qc.get('first_frames_vs_thumbnail', [])[:9]}")
    for title, items in (("Errors", val["errors"] + (qc or {}).get("errors", [])), ("Warnings", val["warnings"] + (qc or {}).get("warnings", []))):
        if items:
            L.append(f"\n## {title}"); L += [f"- {x}" for x in items]
    if tts_log:
        L.append("\n## Narration\n" + tts_log.strip())
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return ok


def main(inbox, outdir):
    inbox, outdir = Path(inbox), Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    work = Path("/tmp/trends_work"); summary = []
    for zp in sorted(inbox.glob("*.zip")):
        jd = work / zp.stem
        shutil.rmtree(jd, ignore_errors=True); safe_extract(zp, jd)
        val = validate(jd)
        try:
            job_id = json.loads((jd / "production.json").read_text(encoding="utf-8")).get("job_id") or zp.stem
        except Exception:
            job_id = zp.stem
        od = outdir / job_id; od.mkdir(parents=True, exist_ok=True)
        qc, tts_log = None, ""
        if not val["errors"]:
            r = subprocess.run([sys.executable, str(HERE / "tts.py"), str(jd), str(jd / "_vo")], capture_output=True, text=True)
            tts_log = r.stdout + r.stderr
            if r.returncode != 0:
                val["errors"].append("narration failed (see Narration section)")
            else:
                try:
                    qc = render.render(jd, jd / "_vo" / "vo.mp3", jd / "_vo" / "vo.json", od)
                except Exception as e:
                    val["errors"].append(f"render failed: {e}")
        prod = json.loads((jd / "production.json").read_text(encoding="utf-8")) if (jd / "production.json").exists() else {}
        (od / "upload.json").write_text(json.dumps({k: prod.get(k) for k in ("job_id", "country", "mode", "title", "description", "first_comment")}, ensure_ascii=False, indent=2))
        if (jd / "thumbnail.png").exists():
            shutil.copy(jd / "thumbnail.png", od / "thumbnail.png")
        ok = report(od / "report.md", job_id, val, qc, tts_log)
        summary.append(f"- {'✅' if ok else '❌'} {job_id}")
        print(job_id, "OK" if ok else "NEEDS FIXES")
    (outdir / "SUMMARY.md").write_text("# Trends render batch\n\n" + "\n".join(summary) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
