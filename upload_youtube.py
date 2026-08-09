"""
Sube un MP4 a YouTube como Short usando un refresh token (sin navegador en CI).
Requiere los secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
El refresh token se obtiene UNA vez (ver README / auth_youtube.py).

Instala: pip install google-api-python-client google-auth google-auth-oauthlib
"""
import os
import sys
import tempfile
import requests

import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not (config.YT_CLIENT_ID and config.YT_CLIENT_SECRET and config.YT_REFRESH_TOKEN):
        print("ERROR: faltan YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN.",
              file=sys.stderr)
        sys.exit(1)

    creds = Credentials(
        token=None,
        refresh_token=config.YT_REFRESH_TOKEN,
        client_id=config.YT_CLIENT_ID,
        client_secret=config.YT_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds)


def upload_short(mp4_url: str, title: str, description: str,
                 tags=None, privacy: str = None) -> str:
    from googleapiclient.http import MediaFileUpload

    privacy = privacy or config.PUBLISH_PRIVACY
    youtube = _service()

    # Descargar el MP4 desde el CDN de JSON2Video a un temporal
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    with requests.get(mp4_url, stream=True, timeout=180) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            tmp.write(chunk)
    tmp.close()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": (tags or [])[:15],
            "categoryId": config.YT_CATEGORY_ID,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(tmp.name, mimetype="video/mp4", resumable=True)
    resp = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    ).execute()
    os.unlink(tmp.name)

    vid = resp.get("id")
    url = f"https://youtu.be/{vid}"
    print(f"   YouTube ({privacy}): {url}")
    return url
