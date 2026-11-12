"""Report where a video went and whether it can leave private (tries unlisted, then puts it back).

usage: python pipeline/check_video.py [video id] [read]
With "read" it only reports and changes nothing.
Without a video id it only reports which channel the saved permission belongs to.
"""
import sys

from upload_youtube import service

yt = service()
vid = sys.argv[1] if len(sys.argv) > 1 else ""
ch = yt.channels().list(part="snippet", mine=True).execute()["items"]
print("Token's channel(s):", [(c["id"], c["snippet"]["title"]) for c in ch])
if not vid:
    raise SystemExit(0)
items = yt.videos().list(part="snippet,status", id=vid).execute()["items"]
if not items:
    raise SystemExit("Video not found")
v = items[0]
print("Video channel:", v["snippet"]["channelTitle"], v["snippet"]["channelId"])
print("Status:", v["status"])
if len(sys.argv) > 2 and sys.argv[2] == "read":
    raise SystemExit(0)
try:
    body = {"id": vid, "status": {**v["status"], "privacyStatus": "unlisted"}}
    for k in ["uploadStatus", "failureReason", "rejectionReason", "publishAt"]:
        body["status"].pop(k, None)
    r = yt.videos().update(part="status", body=body).execute()
    print("After switching to unlisted:", r["status"]["privacyStatus"])
    after = yt.videos().list(part="status", id=vid).execute()["items"][0]["status"]
    print("Re-read status:", after)
    body["status"]["privacyStatus"] = "private"
    yt.videos().update(part="status", body=body).execute()
    print("Put back to private")
except Exception as err:
    print("Could not change privacy:", err)
