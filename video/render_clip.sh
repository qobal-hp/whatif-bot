#!/usr/bin/env bash
# render_clip.sh FIRST LAST OUT.mp4 — one stretch of the episode, encoded like the full render.
set -euo pipefail
npx remotion render src/index.ts Episode "$3.raw.mp4" --props=public/props.json --frames="$1-$2" --muted --log=warn --concurrency=100%
ffmpeg -v error -y -i "$3.raw.mp4" -c:v libx264 -preset medium -crf 21 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -an "$3"
rm "$3.raw.mp4"
