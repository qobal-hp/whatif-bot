"""Change video titles. usage: python retitle.py <json {videoId: new title}>"""
import json
import sys
from upload_youtube import service

yt = service()
for vid, title in json.load(open(sys.argv[1])).items():
    v = yt.videos().list(part="snippet", id=vid).execute()["items"][0]
    snip = v["snippet"]
    old = snip["title"]
    snip["title"] = title
    body = {"id": vid, "snippet": {k: snip[k] for k in ("title", "description", "categoryId", "tags",
                                                       "defaultLanguage") if k in snip}}
    yt.videos().update(part="snippet", body=body).execute()
    print(f"RETITLED {vid}: {old} -> {title}")
