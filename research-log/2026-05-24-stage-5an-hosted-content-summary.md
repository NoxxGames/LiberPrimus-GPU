# Stage 5AN Hosted Content Summary

Stage 5AN generated a hosted private-content library under `website-export/stage5an/private-content/` and a combined SFTP-ready webroot under `website-export/stage5an/webserver-root/`.

Summary:

- Hosted-content files: `211`
- Hosted-content size bytes: `1443834`
- Combined webroot generated: `true`
- Combined webroot ZIP created: `true`
- Robots/noindex present: `true`
- Upload instructions created: `true`

Copy the contents of `website-export/stage5an/webserver-root/` to the private webserver root to expose the metadata index at `/index.html` and private content at `/private-content/index.html`.

Noindex metadata is not access control; private hosting should use access controls when generated extracts are uploaded.
