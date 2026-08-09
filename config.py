"""
Configuración central del pipeline de vídeo de Habliko.
Todo lo ajustable (marca, idiomas, voces, tema, publicación) está aquí.
Las CLAVES nunca van aquí: se leen de variables de entorno / GitHub Secrets.
"""
import os

# --- Claves (desde entorno / GitHub Secrets) -------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
JSON2VIDEO_API_KEY = os.environ.get("JSON2VIDEO_API_KEY", "")

# YouTube (OAuth): se obtienen una vez y se guardan como secrets.
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

# --- Marca Habliko ---------------------------------------------------------
BRAND = {
    "name": "Habliko",
    "url": "habliko.com",
    "bg_color": "#0E7C6B",
    "text_color": "#FFFFFF",
    "accent_color": "#FFD23F",
    "logo_url": "",
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

# --- Luxemburgués (LB): hueco Liesmaschinn ---------------------------------
LB_ENABLED = False

# --- Ritmo del bucle -------------------------------------------------------
PAUSE_BETWEEN = 2

# --- Publicación en YouTube ------------------------------------------------
# Privacidad de subida. "private" es lo prudente: subes en privado, revisas
# y luego lo pasas a público o lo programas. Opciones: private | unlisted | public
PUBLISH_PRIVACY = os.environ.get("PUBLISH_PRIVACY", "private")
YT_CATEGORY_ID = "27"                         # Educación

# --- Tema del reel ---------------------------------------------------------
TOPIC = os.environ.get(
    "TOPIC",
    "Por qué aprender un idioma con Habliko es más fácil: IA que se adapta a tu nivel, "
    "8 idiomas, niveles A1-C2 y práctica en pocos minutos al día.",
)

FREE_PLAN_SECONDS = 600
HOBBY_PLAN_SECONDS = 50 * 60
