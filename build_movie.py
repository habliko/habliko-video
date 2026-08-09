"""
Paso 2 — Convierte el guion en el JSON de película para JSON2Video.
Formato vertical 1080x1920. Duración de escena automática (se ajusta a la voz).

Voz:
- Idiomas con Azure (es/en/fr/de/it/pt/nl): elemento 'voice' (gratis, incluido).
- LB: elemento 'audio' con el WAV de tu Liesmaschinn (vía liesmaschinn.synthesize).
"""
import sys

import config
import liesmaschinn


def _text_element(on_screen: str) -> dict:
    b = config.BRAND
    return {
        "type": "text",
        "text": on_screen or "",
        "duration": -1,
        "settings": {
            "font-family": "Montserrat",
            "font-size": "88px",
            "font-weight": "800",
            "color": b["text_color"],
            "text-align": "center",
            "vertical-align": "center",
            "horizontal-align": "center",
            "padding": "80px",
            "text-shadow": "2px 2px 8px rgba(0,0,0,0.45)",
        },
    }


def build_movie(script: dict, lang: str) -> dict:
    b = config.BRAND
    is_lb = lang == "lb"
    voice = config.VOICES.get(lang)

    if not is_lb and not voice:
        print(f"ERROR: no hay voz Azure para el idioma '{lang}'.", file=sys.stderr)
        sys.exit(1)

    scenes = []
    for sc in script["scenes"]:
        elements = []

        if is_lb:
            # Rama LB: audio de Liesmaschinn (WAV hosteado). Requiere LB_ENABLED.
            audio_url = liesmaschinn.synthesize(sc["voice_text"])
            if not audio_url:
                print(
                    "ERROR: Liesmaschinn aún no devuelve audio para LB. "
                    "Implementa liesmaschinn.synthesize() y pon LB_ENABLED=True.",
                    file=sys.stderr,
                )
                sys.exit(1)
            elements.append({"type": "audio", "src": audio_url})
        else:
            elements.append({
                "type": "voice",
                "text": sc["voice_text"],
                "voice": voice,
                "model": "azure",
            })

        elements.append(_text_element(sc.get("on_screen", "")))
        scenes.append({"background-color": b["bg_color"], "elements": elements})

    movie = {
        "resolution": "custom",
        "width": config.VIDEO_WIDTH,
        "height": config.VIDEO_HEIGHT,
        "quality": config.VIDEO_QUALITY,
        "scenes": scenes,
        "client-data": {"project": "habliko-video", "lang": lang},
    }

    if b.get("logo_url"):
        movie["elements"] = [{
            "type": "image", "src": b["logo_url"],
            "width": 240, "x": 60, "y": 60, "duration": -1,
        }]

    return movie
