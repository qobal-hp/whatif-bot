"""List the videos on the signed-in channel with their upload and privacy status (debugging uploads)."""
from upload_youtube import service

yt = service()
ch = yt.channels().list(part="snippet,contentDetails,status", mine=True).execute()["items"]
for c in ch:
    print("channel:", c["snippet"]["title"], c["id"], c.get("status"))
    pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
    try:
        items = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=50).execute().get("items", [])
    except Exception as e:
        print("uploads playlist:", e); items = []
    ids = [i["contentDetails"]["videoId"] for i in items]
    print("uploads:", len(ids))
    if ids:
        for v in yt.videos().list(part="snippet,status", id=",".join(ids)).execute().get("items", []):
            print(v["id"], v["status"].get("uploadStatus"), v["status"].get("rejectionReason"), v["status"].get("failureReason"), v["status"].get("privacyStatus"), v["snippet"]["title"][:50])
s = yt.search().list(part="id", forMine=True, type="video", maxResults=50).execute()
print("search forMine:", [i["id"]["videoId"] for i in s.get("items", [])])
