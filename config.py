"""
Configuración central del pipeline de vídeo de Habliko.
Estilo visual: "Ink moderno" (tinta oscura + menta, tipografía Inter).
"""
import os

# --- Claves (desde entorno / GitHub Secrets) -------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
JSON2VIDEO_API_KEY = os.environ.get("JSON2VIDEO_API_KEY", "")
YT_CLIENT_ID = os.environ.get("YT_CLIENT_ID", "")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET", "")
YT_REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN", "")

# --- Modelos / endpoints ---------------------------------------------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"
J2V_URL = "https://api.json2video.com/v2/movies"

# --- Formato del reel ------------------------------------------------------
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_QUALITY = "high"

# --- Medios en tu R2 (servido por media.habliko.com) -----------------------
MEDIA_BASE = "https://media.habliko.com"

# Logo (carpeta habliko-media/habliko/logos/). Pon el NOMBRE REAL del archivo:
LOGO_URL = f"{MEDIA_BASE}/habliko/logos/Foxi sin fondo 500x500.png"   # <-- ajusta el nombre

# Música (carpeta habliko-media/musica/): 3 pistas, se elige una AL AZAR por reel.
# Pon los NOMBRES REALES de tus 3 archivos:
MUSIC_URLS = [
    f"{MEDIA_BASE}/musica/background-music-advertising-30-sec-357379.mp3",              # <-- ajusta el nombre
    f"{MEDIA_BASE}/musica/mondamusic-energetic-sports-sport-512828.mp3",              # <-- ajusta el nombre
    f"{MEDIA_BASE}/musica/tatamusic-advertising-background-music-426849.mp3",              # <-- ajusta el nombre
]
MUSIC_VOLUME = 0.2                                  # bajita bajo la voz (0-1)

# Foxi (opcional, aparte del logo). Vacío = no aparece.
FOXI_URL = os.environ.get("FOXI_URL", "")

# --- Marca Habliko :: estilo "Ink moderno" ---------------------------------
BRAND = {
    "name": "Habliko",
    "url": "habliko.com",
    "bg_color": "#101828",
    "text_color": "#F8FAFC",
    "accent_color": "#22D3AA",
    "caption_color": "#CBD5E1",
    "font": "Inter",
    "logo_url": LOGO_URL,
}

# --- Idiomas ---------------------------------------------------------------
LANGS = ["es", "en", "fr", "de", "it", "pt", "nl", "lb"]
DEFAULT_LANG = "es"

VOICES = {
    "es": "es-ES-ElviraNeural",
    "en": "en-US-EmmaMultilingualNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "it": "it-IT-ElsaNeural",
    "pt": "pt-PT-RaquelNeural",
    "nl": "nl-NL-ColetteNeural",
}

LANG_NAMES = {
    "es": "español", "en": "English", "fr": "français", "de": "Deutsch",
    "it": "italiano", "pt": "português", "nl": "Nederlands", "lb": "Lëtzebuergesch",
}

LB_ENABLED = False
PAUSE_BETWEEN = 2

# --- Publicación en YouTube ------------------------------------------------
PUBLISH_PRIVACY = os.environ.get("PUBLISH_PRIVACY", "private")
YT_CATEGORY_ID = "27"

TOPIC = os.environ.get(
    "TOPIC",
    "Por qué aprender un idioma con Habliko es más fácil: IA que se adapta a tu nivel, "
    "8 idiomas, niveles A1-C2 y práctica en pocos minutos al día.",
)

FREE_PLAN_SECONDS = 600
HOBBY_PLAN_SECONDS = 50 * 60
