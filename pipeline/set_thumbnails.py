"""Set custom thumbnails. usage: python set_thumbnails.py <json {videoId: repo-relative image path}>"""
import json
import sys
from googleapiclient.http import MediaFileUpload
from upload_youtube import service

yt = service()
for vid, path in json.load(open(sys.argv[1])).items():
    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(f"../{path}", mimetype="image/jpeg")).execute()
    print(f"THUMB {vid} <- {path}")
