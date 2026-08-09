"""
Paso 2 — Convierte el guion en el JSON de película para JSON2Video.
Formato vertical 1080x1920. Voz por Azure (gratis). Texto en pantalla por escena.
Duración de cada escena = automática, se ajusta a la locución (duration: -1).
"""
import config


def build_movie(script: dict) -> dict:
    voice = config.VOICES.get(config.LANG, config.VOICES["es"])
    b = config.BRAND

    scenes = []
    for sc in script["scenes"]:
        elements = [
            # Voz en off (Azure = incluida, no gasta créditos aparte).
            {
                "type": "voice",
                "text": sc["voice_text"],
                "voice": voice,
                "model": "azure",
            },
            # Texto en pantalla (grande, centrado).
            {
                "type": "text",
                "text": sc.get("on_screen", ""),
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
            },
        ]

        scene = {
            "background-color": b["bg_color"],
            "elements": elements,
        }
        scenes.append(scene)

    movie = {
        "resolution": "custom",
        "width": config.VIDEO_WIDTH,
        "height": config.VIDEO_HEIGHT,
        "quality": config.VIDEO_QUALITY,
        "scenes": scenes,
        # Datos para correlacionar el render con tu registro.
        "client-data": {
            "project": "habliko-video-poc",
            "lang": config.LANG,
        },
    }

    # Logo/Foxi opcional superpuesto en todas las escenas (si lo defines).
    if b.get("logo_url"):
        movie["elements"] = [
            {
                "type": "image",
                "src": b["logo_url"],
                "width": 240,
                "x": 60,
                "y": 60,
                "duration": -1,
            }
        ]

    return movie
