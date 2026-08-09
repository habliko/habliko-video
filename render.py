"""
Paso 3 — Renderiza en JSON2Video y espera el MP4.
Devuelve (url_mp4, duracion_segundos). La duración = créditos consumidos.
"""
import sys
import time
import requests

import config


def render_movie(movie: dict) -> tuple[str, float]:
    if not config.JSON2VIDEO_API_KEY:
        print("ERROR: falta JSON2VIDEO_API_KEY en el entorno.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "x-api-key": config.JSON2VIDEO_API_KEY,
        "Content-Type": "application/json",
    }

    r = requests.post(config.J2V_URL, headers=headers, json=movie, timeout=60)
    if r.status_code not in (200, 201):
        print(f"ERROR JSON2Video POST {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    project = r.json().get("project")
    if not project:
        print(f"ERROR: sin project id en la respuesta: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(f"   Render lanzado. project={project}")

    for _ in range(120):                      # ~4 min máx (2s * 120)
        time.sleep(2)
        s = requests.get(
            config.J2V_URL, headers=headers,
            params={"project": project}, timeout=30,
        )
        if s.status_code != 200:
            continue
        movie_info = s.json().get("movie", {})
        status = movie_info.get("status")
        if status == "done":
            url = movie_info.get("url", "")
            duration = float(movie_info.get("duration", 0) or 0)
            return url, duration
        if status == "error":
            print(f"ERROR de render: {movie_info}", file=sys.stderr)
            sys.exit(1)

    print("ERROR: timeout esperando el render.", file=sys.stderr)
    sys.exit(1)
