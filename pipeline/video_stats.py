"""Print status, views and length of videos: python pipeline/video_stats.py ID,ID,..."""
import sys
from upload_youtube import service

yt = service()
for v in yt.videos().list(part="snippet,statistics,status,contentDetails", id=sys.argv[1]).execute()["items"]:
    s = v["statistics"]
    print(f'{v["id"]} {v["status"]["privacyStatus"]:8} {v["snippet"]["publishedAt"][:10]} {v["contentDetails"]["duration"]:10} views={s.get("viewCount")} likes={s.get("likeCount")} comments={s.get("commentCount")} | {v["snippet"]["title"][:60]}')
