"""Delete private videos by id (refuses anything that is not private). usage: python delete_videos.py <ids.txt>"""
import sys
from upload_youtube import service

yt = service()
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute()["items"]:
        if v["status"]["privacyStatus"] != "private":
            print(f"KEPT (not private) {v['id']} {v['snippet']['title']}")
            continue
        yt.videos().delete(id=v["id"]).execute()
        print(f"DELETED {v['id']} {v['snippet']['title']}")
