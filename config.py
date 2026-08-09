"""
Configuración central del pipeline de vídeo de Habliko.
Todo lo ajustable (marca, idiomas, voces, tema) está aquí.
Las CLAVES nunca van aquí: se leen de variables de entorno / GitHub Secrets.
"""
import os

# --- Claves (desde entorno / GitHub Secrets) -------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
JSON2VIDEO_API_KEY = os.environ.get("JSON2VIDEO_API_KEY", "")

# --- Modelos / endpoints ---------------------------------------------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"           # el mismo que usas en tus blogs
J2V_URL = "https://api.json2video.com/v2/movies"

# --- Formato del reel ------------------------------------------------------
# Vertical 1080x1920 = tarifa base (1 crédito/segundo). NUNCA 4K.
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_QUALITY = "high"                        # high | medium | low

# --- Marca Habliko ---------------------------------------------------------
BRAND = {
    "name": "Habliko",
    "url": "habliko.com",
    "bg_color": "#0E7C6B",                    # verde Foxi (pon tu HEX real)
    "text_color": "#FFFFFF",
    "accent_color": "#FFD23F",
    "logo_url": "",                           # PNG desde media.habliko.com; "" = sin logo
}

# --- Idiomas ---------------------------------------------------------------
# Orden del bucle. LB va al final porque usa Liesmaschinn (ver abajo).
LANGS = ["es", "en", "fr", "de", "it", "pt", "nl", "lb"]
DEFAULT_LANG = "es"                           # idioma para 'python main.py' sin --all

# Voces Azure (gratis, incluidas en el crédito de render). NO incluye LB.
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

# --- Luxemburgués (LB) -----------------------------------------------------
# El hueco está preparado: cuando integres tu Liesmaschinn en liesmaschinn.py,
# pon LB_ENABLED = True y el bucle renderizará también el LB con tu voz.
# Mientras esté en False, el LB se SALTA (no gasta créditos, no rompe el bucle).
# Recuerda: el texto LB debe validarlo tu hablante nativo antes de publicar.
LB_ENABLED = False

# --- Ritmo del bucle -------------------------------------------------------
PAUSE_BETWEEN = 2                             # segundos de cortesía entre idiomas

# --- Tema del reel ---------------------------------------------------------
TOPIC = os.environ.get(
    "TOPIC",
    "Por qué aprender un idioma con Habliko es más fácil: IA que se adapta a tu nivel, "
    "8 idiomas, niveles A1-C2 y práctica en pocos minutos al día.",
)

# Presupuesto de referencia (para los avisos de consumo)
FREE_PLAN_SECONDS = 600
HOBBY_PLAN_SECONDS = 50 * 60
