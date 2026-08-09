"""
Paso 2 — Construye el JSON de película para JSON2Video.

Dos modos automáticos según el fondo (config.BG_URLS):
- Fondo VÍDEO (mp4/mov/webm)  -> UNA escena: el vídeo (con su música) suena de
  corrido, narración continua y los textos aparecen por tiempos.
- Fondo imagen / sin fondo     -> multiescena clásico (una escena por frase).

Texto oscuro (config.BRAND) pensado para fondos claros.
"""
import random
import sys

import config
import liesmaschinn

W, H = config.VIDEO_WIDTH, config.VIDEO_HEIGHT
VIDEO_EXT = (".mp4", ".mov", ".webm", ".m4v")


# ---------- helpers de texto ----------
def _headline(text, start=None, duration=-1, vertical="top", pad="380px 90px 0 90px"):
    b = config.BRAND
    el = {
        "type": "text", "text": text or "", "duration": duration,
        "settings": {
            "font-family": b["font"], "font-size": "92px", "font-weight": "800",
            "color": b["text_color"], "text-align": "center",
            "horizontal-align": "center", "vertical-align": vertical,
            "padding": pad, "line-height": "1.1",
        },
    }
    if start is not None:
        el["start"] = start
    return el


def _caption(text, extra_bottom=430):
    b = config.BRAND
    return {
        "type": "text", "text": text or "", "duration": -1,
        "settings": {
            "font-family": b["font"], "font-size": "48px", "font-weight": "600",
            "color": b["caption_color"], "text-align": "center",
            "horizontal-align": "center", "vertical-align": "bottom",
            "padding": f"0 90px {extra_bottom}px 90px", "line-height": "1.3",
        },
    }


def _cta(start=None):
    b = config.BRAND
    el = {
        "type": "text", "text": b["url"], "duration": -1,
        "settings": {
            "font-family": b["font"], "font-size": "60px", "font-weight": "800",
            "color": b["accent_color"], "text-align": "center",
            "horizontal-align": "center", "vertical-align": "bottom",
            "padding": "0 90px 300px 90px",
        },
    }
    if start is not None:
        el["start"] = start
    return el


def _foxi():
    return {"type": "image", "src": config.FOXI_URL, "width": 300,
            "position": "bottom-right", "x": 40, "y": 40, "duration": -1}


# ---------- selección de medios ----------
def _pick_music():
    tracks = [u for u in config.MUSIC_URLS if u]
    return random.choice(tracks) if tracks else None


def _pick_bg():
    bgs = [u for u in getattr(config, "BG_URLS", []) if u]
    return random.choice(bgs) if bgs else None


def _is_video(url):
    return bool(url) and url.lower().split("?")[0].endswith(VIDEO_EXT)


# ---------- modo 1: fondo VÍDEO, una sola escena ----------
def _text_left(text, start, duration, y, size="74px", weight="800",
               color=None, valign="top", height=560):
    """Texto en la COLUMNA IZQUIERDA (zona limpia de fondos con sujeto a la derecha)."""
    b = config.BRAND
    return {
        "type": "text", "text": text or "", "start": start, "duration": duration,
        "x": 60, "y": y, "width": 640, "height": height,
        "settings": {
            "font-family": b["font"], "font-size": size, "font-weight": weight,
            "color": color or b["text_color"], "text-align": "left",
            "horizontal-align": "left", "vertical-align": valign, "line-height": "1.15",
        },
    }


def _blink(text, base_start, y, size, color):
    """'Buscamos promotores' destella 2 veces y luego se queda fijo hasta el final."""
    els, t, on, off = [], base_start, 0.3, 0.3
    for _ in range(2):                       # 2 destellos
        els.append(_text_left(text, round(t, 2), on, y=y, size=size,
                              color=color, height=200))
        t += on + off
    els.append(_text_left(text, round(t, 2), -1, y=y, size=size,
                          color=color, height=200))   # fijo al final
    return els


def _build_video_bg(script, lang, bg, voice):
    b = config.BRAND
    narration = " ".join(s["voice_text"] for s in script["scenes"])
    elements = [
        {"type": "video", "src": bg, "x": 0, "y": 0, "width": W, "height": H,
         "volume": config.BG_VIDEO_VOLUME, "duration": -2},
        {"type": "voice", "text": narration, "voice": voice, "model": "azure",
         "extra-time": config.END_HOLD},
    ]

    END = 9.0
    elements.append(_text_left(script["scenes"][0].get("on_screen", ""), 0, 4.5, y=240))
    if len(script["scenes"]) > 1:
        elements.append(_text_left(script["scenes"][1].get("on_screen", ""), 4.5, END - 4.5, y=240))

    # Tarjeta final: "Buscamos promotores" con PARPADEO + web + mail (fijos al cierre)
    promoter = config.CTA_PROMOTER.get(lang, config.CTA_PROMOTER["es"])
    elements.extend(_blink(promoter, END, y=980, size="60px", color=b["accent_color"]))
    elements.append(_text_left(b["url"], END, -1, y=1110, size="54px",
                               weight="800", color=b["text_color"], height=160))
    elements.append(_text_left(config.CONTACT_EMAIL, END, -1, y=1205, size="46px",
                               weight="700", color=b["text_color"], height=160))

    movie = {
        "resolution": "custom", "width": W, "height": H,
        "quality": config.VIDEO_QUALITY,
        "scenes": [{"background-color": b["bg_color"], "elements": elements}],
        "client-data": {"project": "habliko-video", "lang": lang},
    }
    if b.get("logo_url"):
        movie["elements"] = [{"type": "image", "src": b["logo_url"], "width": 200,
                              "position": "top-left", "x": 60, "y": 60, "duration": -1}]
    return movie


# ---------- modo 2: multiescena (imagen / sin fondo) ----------
def _build_multiscene(script, lang, bg, voice, is_lb):
    b = config.BRAND
    scenes = []
    n = len(script["scenes"])
    for idx, sc in enumerate(script["scenes"]):
        is_last = idx == n - 1
        elements = []
        if bg:
            elements.append({"type": "image", "src": bg, "width": W, "height": H,
                             "x": 0, "y": 0, "duration": -1})
        if is_lb:
            audio_url = liesmaschinn.synthesize(sc["voice_text"])
            if not audio_url:
                print("ERROR: Liesmaschinn aún no devuelve audio para LB.", file=sys.stderr)
                sys.exit(1)
            elements.append({"type": "audio", "src": audio_url})
        else:
            elements.append({"type": "voice", "text": sc["voice_text"],
                             "voice": voice, "model": "azure"})
        elements.append(_headline(sc.get("on_screen", "")))
        elements.append(_caption(sc["voice_text"], extra_bottom=430 if not is_last else 480))
        if config.FOXI_URL:
            elements.append(_foxi())
        if is_last:
            elements.append(_cta())
        scenes.append({"background-color": b["bg_color"],
                       "transition": {"style": "fade", "duration": 0.4},
                       "elements": elements})

    movie = {
        "resolution": "custom", "width": W, "height": H,
        "quality": config.VIDEO_QUALITY, "scenes": scenes,
        "client-data": {"project": "habliko-video", "lang": lang},
    }
    globals_ = []
    music = _pick_music()
    if music:
        globals_.append({"type": "audio", "src": music, "duration": -2,
                         "fade-out": 2, "volume": config.MUSIC_VOLUME})
    if b.get("logo_url"):
        globals_.append({"type": "image", "src": b["logo_url"], "width": 200,
                         "position": "top-left", "x": 60, "y": 60, "duration": -1})
    if globals_:
        movie["elements"] = globals_
    return movie


def build_movie(script: dict, lang: str) -> dict:
    is_lb = lang == "lb"
    voice = config.VOICES.get(lang)
    if not is_lb and not voice:
        print(f"ERROR: no hay voz Azure para el idioma '{lang}'.", file=sys.stderr)
        sys.exit(1)

    bg = _pick_bg()
    if _is_video(bg) and not is_lb:
        return _build_video_bg(script, lang, bg, voice)
    return _build_multiscene(script, lang, bg, voice, is_lb)
