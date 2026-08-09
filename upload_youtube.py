"""
Paso 4 (OPCIONAL, siguiente fase) — Sube el MP4 a YouTube como Short.
Requiere OAuth del canal una vez (token.json). No se usa en el test gratis de render.

Subida ~100 vídeos/día en el tramo gratuito de la YouTube Data API.
Instala: pip install google-api-python-client google-auth google-auth-oauthlib
"""
import os
import sys
import tempfile
import requests


def upload_short(mp4_url: str, title: str, description: str, tags=None):
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("Instala las libs de Google para usar la subida a YouTube.", file=sys.stderr)
        sys.exit(1)

    token_file = os.environ.get("YT_TOKEN_FILE", "token.json")
    if not os.path.exists(token_file):
        print(f"ERROR: no existe {token_file} (autoriza el canal una vez).", file=sys.stderr)
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(
        token_file, ["https://www.googleapis.com/auth/youtube.upload"]
    )
    youtube = build("youtube", "v3", credentials=creds)

    # Descargar el MP4 a un temporal
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    with requests.get(mp4_url, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=8192):
            tmp.write(chunk)
    tmp.close()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags or [],
            "categoryId": "27",           # Educación
        },
        "status": {
            "privacyStatus": "private",   # empieza en privado; revísalo antes de publicar
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(tmp.name, mimetype="video/mp4", resumable=True)
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    os.unlink(tmp.name)

    vid = resp.get("id")
    print(f"Subido a YouTube: https://youtu.be/{vid} (privado)")
    return vid
