"""
Configuración central del pipeline de vídeo de Habliko.
Estilo visual: "Ink moderno" (tinta oscura + menta, tipografía Inter).
"""
import os

# --- Claves (desde entorno / GitHub Secrets) -------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
JSON2VIDEO_API_KEY = os.environ.get("JSON2VIDEO_API_KEY", "")
YT_CLIENT_ID = os.environ.get("YT_CLIENT_ID", "")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET", "")
YT_REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN", "")

# --- Modelos / endpoints ---------------------------------------------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"
J2V_URL = "https://api.json2video.com/v2/movies"

# Proveedores de IA en orden (Cerebras principal + Groq respaldo, mismo modelo).
# Se prueban en orden; si uno da 429 salta al siguiente. Solo se usa el que
# tenga API key definida.  Cerebras: 1M tok/dia | Groq: 200k tok/dia
AI_PROVIDERS = [
    {
        "name": "cerebras",
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "key": CEREBRAS_API_KEY,
        "model": "gpt-oss-120b",
    },
    {
        "name": "groq",
        "url": GROQ_URL,
        "key": GROQ_API_KEY,
        "model": GROQ_MODEL,
    },
]

# --- Formato del reel ------------------------------------------------------
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_QUALITY = "high"

# --- Medios en tu R2 (servido por media.habliko.com) -----------------------
MEDIA_BASE = "https://media.habliko.com"

# Logo (carpeta habliko-media/habliko/logos/). Pon el NOMBRE REAL del archivo:
LOGO_URL = f"{MEDIA_BASE}/habliko/logos/logo.png"   # <-- ajusta el nombre

# Música (carpeta habliko-media/musica/): 3 pistas, se elige una AL AZAR por reel.
# Pon los NOMBRES REALES de tus 3 archivos:
MUSIC_URLS = [
    f"{MEDIA_BASE}/musica/track1.mp3",              # <-- ajusta el nombre
    f"{MEDIA_BASE}/musica/track2.mp3",              # <-- ajusta el nombre
    f"{MEDIA_BASE}/musica/track3.mp3",              # <-- ajusta el nombre
]
MUSIC_VOLUME = 0.2
BG_VIDEO_VOLUME = 0.7          # volumen del audio del MP4 de fondo, bajo la voz                                  # bajita bajo la voz (0-1)

# Fondos (carpeta habliko-media/fondos/): PNG 1080x1920 SIN texto, se elige uno
# AL AZAR por reel. Deja la lista vacía para usar el fondo tinta plano.
BG_URLS = [
    f"{MEDIA_BASE}/habliko/fondos/fondo1.mp4",   # bajo habliko/ (mismo prefijo que Foxi/logo)
    # f"{MEDIA_BASE}/habliko/fondos/fondo2.mp4",
]

# Foxi (personaje, aparte del logo). Sube el PNG transparente a tu R2 y ajusta el nombre.
# Ruta sugerida: habliko-media/habliko/foxi/foxi.png
FOXI_URL = os.environ.get("FOXI_URL", f"{MEDIA_BASE}/habliko/foxi/foxi.png")

# --- Marca Habliko :: estilo "Ink moderno" ---------------------------------
BRAND = {
    "name": "Habliko",
    "url": "habliko.com",
    "bg_color": "#EDE7DD",        # fallback claro (el vídeo lo cubre)
    "text_color": "#14213D",      # texto OSCURO para fondos claros
    "accent_color": "#0E7C6B",    # teal que lee sobre blanco
    "caption_color": "#334155",
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
# "public" = se publica directo | "unlisted" = oculto con enlace | "private" = solo tú
PUBLISH_PRIVACY = os.environ.get("PUBLISH_PRIVACY", "public")
YT_CATEGORY_ID = "27"

TOPIC = os.environ.get(
    "TOPIC",
    "Por qué aprender un idioma con Habliko es más fácil: IA que se adapta a tu nivel, "
    "8 idiomas, niveles A1-C2 y práctica en pocos minutos al día.",
)

FREE_PLAN_SECONDS = 600
HOBBY_PLAN_SECONDS = 50 * 60
