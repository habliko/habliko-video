"""
Configuración central del pipeline de vídeo de Habliko.
Todo lo que quieras tocar (marca, idioma, tema, voces) está aquí.
Las CLAVES nunca van aquí: se leen de variables de entorno / GitHub Secrets.
"""
import os

# --- Claves (desde entorno / GitHub Secrets) -------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
JSON2VIDEO_API_KEY = os.environ.get("JSON2VIDEO_API_KEY", "")

# --- Modelos / endpoints ---------------------------------------------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"          # el mismo que usas en tus blogs
J2V_URL = "https://api.json2video.com/v2/movies"

# --- Formato del reel ------------------------------------------------------
# Vertical 1080x1920 = tarifa base (1 crédito/segundo). NUNCA 4K.
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_QUALITY = "high"                       # high | medium | low (low = más rápido)

# --- Marca Habliko ---------------------------------------------------------
BRAND = {
    "name": "Habliko",
    "url": "habliko.com",
    "bg_color": "#0E7C6B",                    # verde Foxi (cámbialo a tu HEX real)
    "text_color": "#FFFFFF",
    "accent_color": "#FFD23F",
    # Opcional: logo/Foxi PNG servido desde tu R2 (media.habliko.com).
    # Déjalo en "" para que el test gratis renderice sin depender de assets.
    "logo_url": "",
}

# --- Idioma del reel (PoC = español) ---------------------------------------
# Voces Azure (gratis, incluidas en el crédito de render).
# Azure NO tiene luxemburgués: el LB se resolverá luego con tu Liesmaschinn.
LANG = os.environ.get("LANG_CODE", "es")

VOICES = {
    "es": "es-ES-ElviraNeural",
    "en": "en-US-EmmaMultilingualNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "it": "it-IT-ElsaNeural",
    "pt": "pt-PT-RaquelNeural",
    "nl": "nl-NL-ColetteNeural",
    # "lb": pendiente -> Liesmaschinn (pista de audio propia)
}

LANG_NAMES = {
    "es": "español", "en": "English", "fr": "français", "de": "Deutsch",
    "it": "italiano", "pt": "português", "nl": "Nederlands",
}

# --- Tema del reel ---------------------------------------------------------
# Cámbialo o pásalo por variable de entorno TOPIC.
TOPIC = os.environ.get(
    "TOPIC",
    "Por qué aprender un idioma con Habliko es más fácil: IA que se adapta a tu nivel, "
    "8 idiomas, niveles A1-C2 y práctica en pocos minutos al día.",
)
