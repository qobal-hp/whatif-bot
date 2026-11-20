"""Put the long form's link at the top of already-uploaded shorts' descriptions.

usage: python pipeline/relink_shorts.py SHORT_ID=LONG_ID,SHORT_ID=LONG_ID,...
"""
import sys

from upload_youtube import service


def main():
    pairs = dict(p.split("=", 1) for p in sys.argv[1].split(",") if "=" in p)
    yt = service()
    found = {}
    ids = list(pairs)
    for i in range(0, len(ids), 50):
        for item in yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute().get("items", []):
            found[item["id"]] = item["snippet"]
    for short, long in pairs.items():
        snippet = found.get(short)
        if not snippet:
            print(f"{short}: not found (deleted, or on the other channel)")
            continue
        url = f"https://youtu.be/{long}"
        if url in snippet.get("description", ""):
            print(f"{short}: already linked")
            continue
        lines = [l for l in snippet.get("description", "").split("\n") if "full episode" not in l.lower()]
        description = f"\U0001F3AC Full episode: {url}\n\n" + "\n".join(lines).strip()
        body = {"id": short, "snippet": {"title": snippet["title"], "categoryId": snippet["categoryId"],
                                         "description": description, "tags": snippet.get("tags", []),
                                         "defaultLanguage": snippet.get("defaultLanguage", "en")}}
        yt.videos().update(part="snippet", body=body).execute()
        print(f"{short}: linked to {url}")


if __name__ == "__main__":
    main()
