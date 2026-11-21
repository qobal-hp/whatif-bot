"""List every upload of the authorized channel, plus its existing playlists."""
import re
from upload_youtube import service

yt = service()
ch = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
print("CHANNEL", ch["snippet"]["title"])
uploads, ids, token = ch["contentDetails"]["relatedPlaylists"]["uploads"], [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=token).execute()
    ids += [i["contentDetails"]["videoId"] for i in r["items"]]
    token = r.get("nextPageToken")
    if not token:
        break
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part="snippet,contentDetails,status", id=",".join(ids[k:k + 50])).execute()["items"]:
        d = v["contentDetails"]["duration"]
        secs = sum(int(n) * m for n, m in zip(re.findall(r"(\d+)H", d) + ["0"], [3600]) if n) \
            + sum(int(n) * 60 for n in re.findall(r"(\d+)M", d)) + sum(int(n) for n in re.findall(r"(\d+)S", d))
        kind = "SHORT" if secs <= 180 else "LONG"
        print(f"{kind}\t{v['id']}\t{v['status']['privacyStatus']}\t{v['snippet']['publishedAt'][:10]}\t{secs // 60}m\t{v['snippet']['title']}")
for p in yt.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50).execute().get("items", []):
    print(f"PLAYLIST\t{p['id']}\t{p['contentDetails']['itemCount']}\t{p['snippet']['title']}")
