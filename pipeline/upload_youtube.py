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


def upload(yt, path, title, description, tags, privacy, publish_at=None):
    body = {
        "snippet": {"title": title[:100], "description": description, "tags": tags, "categoryId": "28"},
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
    }
    if publish_at:
        body["status"]["privacyStatus"] = "private"
        body["status"]["publishAt"] = publish_at
    request = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(path), chunksize=16 * 1024 * 1024, resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    when = f", goes public {publish_at}" if publish_at else ""
    print(f"Uploaded {path.name}: https://youtu.be/{response['id']} ({body['status']['privacyStatus']}{when})")
    return response["id"]


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    files = Path(sys.argv[2])
    privacy = sys.argv[3]
    only = {o.strip() for o in sys.argv[4].split(",") if o.strip()} if len(sys.argv) > 4 else set()
    schedule = dict(p.split("=", 1) for p in sys.argv[5].split(",") if "=" in p) if len(sys.argv) > 5 else {}
    wanted = lambda name: not only or name in only
    meta = spec["youtube"]
    yt = service()

    episode = files / "episode.mp4"
    if episode.exists() and wanted("episode"):
        video_id = upload(yt, episode, meta["title"], meta["description"], meta["tags"], privacy, schedule.get("episode"))
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
            upload(yt, path, short["youtube_title"], meta["shorts_description"], meta["tags"], privacy, schedule.get(short["id"]))


if __name__ == "__main__":
    main()
