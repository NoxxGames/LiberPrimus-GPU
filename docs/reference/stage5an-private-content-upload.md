# Stage 5AN Private Content Upload

Stage 5AN creates the SFTP-ready webroot at:

```text
website-export/stage5an/webserver-root/
```

Copy the contents of that directory to the private webserver root. After upload, the expected paths are:

```text
http://liberprimus-gpu-data.info/index.html
http://liberprimus-gpu-data.info/private-content/index.html
```

The generated private-content manifest is expected at:

```text
http://liberprimus-gpu-data.info/private-content/data/content-pack-manifest.json
```

This upload is a private Deep Research handoff, not public publication. Use access control when hosted content includes private or review-gated extracts. Do not upload raw `third_party/` folders, raw workbooks, images, archives, audio/video, SQLite databases, or `codex-output/`.
