"""Post a top comment on each video and build playlists.

usage: python engage.py <config.json>
config: {"comments": {videoId: text}, "short_comment": "text with {url}",
         "playlists": [{"title", "description", "videos": [ids]}]}
Every public short whose description links its long form gets short_comment.
Prints COMMENT <videoId> <commentId> for pinning by hand.
"""
import json
import re
import sys
from upload_youtube import service

cfg = json.load(open(sys.argv[1]))
yt = service()
me = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
print("CHANNEL", me["snippet"]["title"])
uploads, ids, token = me["contentDetails"]["relatedPlaylists"]["uploads"], [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=token).execute()
    ids += [i["contentDetails"]["videoId"] for i in r["items"]]
    token = r.get("nextPageToken")
    if not token:
        break
videos = {}
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute()["items"]:
        videos[v["id"]] = v

comments = dict(cfg.get("comments", {})) if not cfg.get("skip_comments") else {}
if cfg.get("short_comment") and not cfg.get("skip_comments"):
    for vid, v in videos.items():
        if vid in comments or "#shorts" not in v["snippet"]["title"].lower():
            continue
        m = re.search(r"https://youtu\.be/([\w-]{11})", v["snippet"]["description"])
        if m:
            comments[vid] = cfg["short_comment"].format(url=f"https://youtu.be/{m.group(1)}")
        else:
            print(f"SKIP {vid} no long-form link: {v['snippet']['title']}")

for vid, text in comments.items():
    v = videos.get(vid)
    if not v or v["status"]["privacyStatus"] != "public":
        print(f"SKIP {vid} not public")
        continue
    try:
        c = yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
            "snippet": {"textOriginal": text}}}}).execute()
        print(f"COMMENT {vid} {c['id']}")
    except Exception as err:
        print(f"FAIL comment {vid}: {err}")

existing = {p["snippet"]["title"]: p["id"] for p in
            yt.playlists().list(part="snippet", mine=True, maxResults=50).execute().get("items", [])}
for pl in cfg.get("playlists", []):
    pid = existing.get(pl["title"])
    if not pid:
        pid = yt.playlists().insert(part="snippet,status", body={
            "snippet": {"title": pl["title"], "description": pl.get("description", ""),
                        "defaultLanguage": cfg.get("language", "en")},
            "status": {"privacyStatus": "public"}}).execute()["id"]
    vids = pl["videos"]
    if vids == "shorts":
        vids = [i for i in ids if "#shorts" in videos[i]["snippet"]["title"].lower()
                and videos[i]["status"]["privacyStatus"] == "public"]
    have, tok = set(), None
    while True:
        r = yt.playlistItems().list(part="snippet", playlistId=pid, maxResults=50, pageToken=tok).execute()
        have |= {i["snippet"]["resourceId"]["videoId"] for i in r["items"]}
        tok = r.get("nextPageToken")
        if not tok:
            break
    for vid in vids:
        if vid in have:
            continue
        for attempt in range(4):
            try:
                yt.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": pid, "resourceId": {
                    "kind": "youtube#video", "videoId": vid}}}).execute()
                break
            except Exception as err:
                if attempt == 3:
                    print(f"FAIL add {vid} to {pl['title']}: {err}")
                import time
                time.sleep(5)
        continue
        try:
            yt.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": pid, "resourceId": {
                "kind": "youtube#video", "videoId": vid}}}).execute()
        except Exception as err:
            print(f"FAIL add {vid} to {pl['title']}: {err}")
    print(f"PLAYLIST {pl['title']} {pid} {len(vids)}")
