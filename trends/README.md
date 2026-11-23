# Trends Shorts pipeline

1. GPT makes one ZIP per issue (production.json in `trends-v2` format — see SCHEMA.md, plus facts.json, thumbnail.png, trends_screenshot.png).
2. Upload the ZIPs into `trends/inbox/` on the `trends-pipeline` branch (GitHub web or app: Add file → Upload files).
3. The "Trends Shorts render" workflow validates each ZIP, makes the ElevenLabs narration (voice from `voices.json` by country + voice_style), renders the 1080×1920 MP4 and checks it.
4. Results land on the `trends-output` branch under `out/<job_id>/`: `video.mp4`, `thumbnail.png`, `upload.json`, `report.md`, `contact_sheet.jpg`. Processed ZIPs move to `trends/done/`.

Nothing is uploaded to YouTube by this pipeline.
