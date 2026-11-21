"""Upload an episode, its thumbnail and its shorts to YouTube.

usage: python pipeline/upload_youtube.py <spec.json> <dir with episode.mp4, thumb.jpg, short*.mp4> <privacy> [only] [schedule]
"only" is an optional comma-separated list of what to upload, e.g. "short1" or "episode,short1".
"schedule" optionally sets publish times in UTC, e.g. "short2=2026-11-13T17:00:00Z,short3=2026-11-14T17:00:00Z";
scheduled videos are uploaded private and YouTube makes them public at that time.
Needs YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN in the environment.
"""
import json
import os
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    )
    return build("youtube", "v3", credentials=creds)


def upload(yt, path, title, description, tags, privacy, publish_at=None, localizations=None, category="28", language="en"):
    body = {
        "snippet": {"title": title[:100], "description": description, "tags": tags, "categoryId": category,
                    "defaultLanguage": language, "defaultAudioLanguage": language},
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
    }
    if publish_at:
        body["status"]["privacyStatus"] = "private"
        body["status"]["publishAt"] = publish_at
    if localizations:
        # Titles and descriptions in other languages, shown to viewers whose YouTube is set to that language.
        body["localizations"] = {lang: {"title": v["title"][:100], "description": v["description"]} for lang, v in localizations.items()}
    request = yt.videos().insert(
        part="snippet,status" + (",localizations" if localizations else ""),
        body=body,
        media_body=MediaFileUpload(str(path), chunksize=16 * 1024 * 1024, resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    when = f", goes public {publish_at}" if publish_at else ""
    print(f"Uploaded {path.name}: https://youtu.be/{response['id']} ({body['status']['privacyStatus']}{when})")
    return response["id"]


def captions(yt, video_id, files, name):
    """Upload subtitle files named <name>.<lang>.srt next to the video, if any."""
    for srt in sorted(files.glob(f"{name}.*.srt")):
        lang = srt.suffixes[-2].lstrip(".")
        try:
            yt.captions().insert(
                part="snippet",
                body={"snippet": {"videoId": video_id, "language": lang, "name": {"en": "English", "es": "Espa\u00f1ol"}.get(lang, lang), "isDraft": False}},
                media_body=MediaFileUpload(str(srt), mimetype="application/octet-stream"),
            ).execute()
            print(f"Captions {lang} added to {video_id}")
        except Exception as err:  # e.g. the token lacks the captions permission; the video is up regardless
            print(f"Captions {lang} could not be added: {err}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    files = Path(sys.argv[2])
    privacy = sys.argv[3]
    only = {o.strip() for o in sys.argv[4].split(",") if o.strip()} if len(sys.argv) > 4 else set()
    schedule = dict(p.split("=", 1) for p in sys.argv[5].split(",") if "=" in p) if len(sys.argv) > 5 else {}
    wanted = lambda name: not only or name in only
    meta = spec["youtube"]
    yt = service()
    expect = meta.get("channel_title")
    if expect:  # refuse to upload to the wrong channel
        mine = [c["snippet"]["title"] for c in yt.channels().list(part="snippet", mine=True).execute().get("items", [])]
        print(f"Authorized channel: {mine}")
        if not any(expect.lower() in m.lower() for m in mine):
            sys.exit(f"This token belongs to {mine}, not {expect}; nothing uploaded")

    long_url = meta.get("long_url", "")  # the long form's link, for shorts uploaded on their own
    episode = files / "episode.mp4"
    if episode.exists() and wanted("episode"):
        description = meta["description"]
        chapters = files / "chapters.txt"
        if "{chapters}" in description:
            description = description.replace("{chapters}", chapters.read_text().strip() if chapters.exists() else "")
        video_id = upload(yt, episode, meta["title"], description, meta["tags"], privacy, schedule.get("episode"),
                          meta.get("localizations"), meta.get("category", "28"), meta.get("language", "en"))
        captions(yt, video_id, files, "episode")
        long_url = f"https://youtu.be/{video_id}"
        thumb = files / "thumb.jpg"
        if thumb.exists():
            try:
                yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumb))).execute()
                print("Thumbnail set")
            except Exception as err:  # the video is already up; a thumbnail can be added by hand
                print(f"Thumbnail could not be set: {err}")

    for short in spec.get("shorts", []):
        path = files / f"{short['id']}.mp4"
        if path.exists() and wanted(short["id"]):
            # Every short carries a link to its long form in the description.
            if not long_url:
                sys.exit(f"No long-form link for {short['id']}: upload the episode with it, or set youtube.long_url in the spec")
            description = short.get("description", meta.get("shorts_description", ""))
            lines = [l for l in description.split("\n") if "full episode" not in l.lower()]
            description = f"\U0001F3AC Full episode: {long_url}\n\n" + "\n".join(lines).strip()
            short_id = upload(yt, path, short["youtube_title"], description,
                              meta["tags"], privacy, schedule.get(short["id"]), short.get("localizations"), meta.get("category", "28"), meta.get("language", "en"))
            captions(yt, short_id, files, short["id"])


if __name__ == "__main__":
    main()
