"""Change videos that are already on YouTube: title, privacy or scheduled publish time.

usage: python pipeline/update_youtube.py <changes>
<changes> is a JSON list, e.g.
  [{"id": "V1jRL4YLYT8", "title": "New title"},
   {"id": "O0lwOk-9Uao", "publish_at": "2026-11-15T17:00:00Z"},
   {"id": "zVfytIui1tQ", "privacy": "public"}]
Fields left out stay as they are. publish_at keeps the video private until YouTube makes it public at that time.
Needs YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN in the environment.
"""
import json
import sys

from upload_youtube import service


def main():
    yt = service()
    for change in json.loads(sys.argv[1]):
        video = yt.videos().list(part="snippet,status", id=change["id"]).execute()["items"][0]
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
        body = {"id": change["id"]}
        if "snippet" in parts:
            body["snippet"] = {k: snippet[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage") if k in snippet}
        if "status" in parts:
            body["status"] = status
        yt.videos().update(part=",".join(parts), body=body).execute()
        print(f"Updated https://youtu.be/{change['id']}: " + ", ".join(f"{k}={v}" for k, v in change.items() if k != "id"))


if __name__ == "__main__":
    main()
