"""Change videos that are already on YouTube: title, privacy or scheduled publish time.

usage: python pipeline/update_youtube.py <changes>
<changes> is a JSON list, e.g.
  [{"id": "V1jRL4YLYT8", "title": "New title"},
   {"id": "O0lwOk-9Uao", "publish_at": "2026-11-15T17:00:00Z"},
   {"id": "zVfytIui1tQ", "privacy": "public"},
   {"id": "V1jRL4YLYT8", "thumbnail": "thumb-output:thumbs/thumb2.jpg"}]
Fields left out stay as they are. thumbnail is a file in the repo, or "<branch>:<path>" for a file on another branch. publish_at keeps the video private until YouTube makes it public at that time.
Needs YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN in the environment.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from googleapiclient.http import MediaFileUpload
from upload_youtube import service


def thumbnail_file(where):
    if ":" not in where:
        return str(Path(__file__).resolve().parent.parent / where)
    branch, path = where.split(":", 1)
    subprocess.run(["git", "fetch", "-q", "--depth=1", "origin", branch], check=True)
    out = Path(tempfile.mkdtemp()) / Path(path).name
    out.write_bytes(subprocess.run(["git", "show", f"FETCH_HEAD:{path}"], check=True, capture_output=True).stdout)
    return str(out)


def main():
    yt = service()
    me = yt.channels().list(part="snippet,status", mine=True).execute().get("items", [])
    for c in me:
        print(f"Signed in as channel: {c['snippet']['title']} ({c['id']}), long uploads: {c.get('status', {}).get('longUploadsStatus')}")
    for change in json.loads(sys.argv[1]):
        if change.get("delete"):
            yt.videos().delete(id=change["id"]).execute()
            print(f"Deleted https://youtu.be/{change['id']}")
            continue
        found = yt.videos().list(part="snippet,status,processingDetails", id=change["id"]).execute()["items"]
        if not found:
            print(f"Not found on this channel: https://youtu.be/{change['id']}")
            continue
        video = found[0]
        snippet, status = video["snippet"], video["status"]
        parts = []
        if "title" in change or "description" in change:
            snippet["title"] = change.get("title", snippet["title"])[:100]
            snippet["description"] = change.get("description", snippet.get("description", ""))
            parts.append("snippet")
        if "privacy" in change or "publish_at" in change:
            status = {k: status[k] for k in ("privacyStatus", "selfDeclaredMadeForKids", "containsSyntheticMedia") if k in status}
            if change.get("publish_at"):
                status["privacyStatus"] = "private"
                status["publishAt"] = change["publish_at"]
            else:
                status["privacyStatus"] = change["privacy"]
            parts.append("status")
        if change.get("thumbnail"):
            yt.thumbnails().set(videoId=change["id"], media_body=MediaFileUpload(thumbnail_file(change["thumbnail"]))).execute()
            print(f"Thumbnail set on https://youtu.be/{change['id']}")
        if not parts:
            continue
        body = {"id": change["id"]}
        if "snippet" in parts:
            body["snippet"] = {k: snippet[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage") if k in snippet}
        if "status" in parts:
            body["status"] = status
        yt.videos().update(part=",".join(parts), body=body).execute()
        print(f"Updated https://youtu.be/{change['id']}: " + ", ".join(f"{k}={v}" for k, v in change.items() if k not in ("id", "thumbnail")))


if __name__ == "__main__":
    main()
