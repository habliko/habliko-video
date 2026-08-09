"""
Pipeline PoC de vídeo Habliko (plan gratuito).
Flujo: Groq (guion) -> JSON2Video (voz + render) -> informe de créditos.

Uso:
    python main.py               # genera y renderiza un reel
    python main.py --dry-run     # solo genera el guion y muestra el JSON (0 créditos)
"""
import json
import sys

import config
from generate_script import generate
from build_movie import build_movie
from render import render_movie

FREE_PLAN_SECONDS = 600   # plan gratis = 10 min = 600 s


def main():
    dry_run = "--dry-run" in sys.argv

    print(f"== Habliko Video PoC == idioma: {config.LANG}\n")

    # 1) Guion
    print("1) Generando guion con Groq...")
    script = generate()
    print(json.dumps(script, ensure_ascii=False, indent=2))

    # 2) Película
    print("\n2) Construyendo la película JSON2Video...")
    movie = build_movie(script)

    if dry_run:
        print("\n[DRY-RUN] Película (no se ha renderizado, 0 créditos):")
        print(json.dumps(movie, ensure_ascii=False, indent=2))
        return

    # 3) Render
    print("\n3) Renderizando en JSON2Video...")
    url, duration = render_movie(movie)

    # 4) Informe de consumo
    print("\n== LISTO ==")
    print(f"MP4:            {url}")
    print(f"Duración:       {duration:.1f} s  ->  {duration:.0f} créditos")
    if duration > 0:
        cabe_gratis = int(FREE_PLAN_SECONDS // duration)
        cabe_hobby = int((50 * 60) // duration)
        print(f"Con el plan GRATIS (600 s) caben ~{cabe_gratis} reels como este.")
        print(f"Con HOBBY (~50 min)      caben ~{cabe_hobby} reels como este.")

    # Guarda un registro simple
    with open("last_run.json", "w", encoding="utf-8") as f:
        json.dump(
            {"url": url, "duration_s": duration, "caption": script.get("caption"),
             "hashtags": script.get("hashtags"), "lang": config.LANG},
            f, ensure_ascii=False, indent=2,
        )
    print("\nRegistro guardado en last_run.json")


if __name__ == "__main__":
    main()
