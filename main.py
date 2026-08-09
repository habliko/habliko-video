"""
Pipeline de vídeo Habliko — versión multilingüe (8 idiomas).
Flujo por idioma: Groq (guion) -> JSON2Video (voz + render) -> informe.

Uso:
    python main.py                 # un solo idioma (config.DEFAULT_LANG = es)
    python main.py --lang fr       # un idioma concreto
    python main.py --all           # bucle por los 8 idiomas de config.LANGS
    python main.py --all --dry-run # genera los 8 guiones SIN renderizar (0 créditos)

El LB se salta automáticamente mientras config.LB_ENABLED sea False.
"""
import json
import sys
import time

import config
from generate_script import generate
from build_movie import build_movie
from render import render_movie


def _arg_value(flag: str, default=None):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def run_one(lang: str, dry_run: bool) -> float:
    """Procesa un idioma. Devuelve los segundos (créditos) consumidos."""
    print(f"\n----- [{lang}] {config.LANG_NAMES.get(lang, lang)} -----")

    if lang == "lb" and not config.LB_ENABLED:
        print("LB pendiente de Liesmaschinn — hueco preparado, se salta (0 créditos).")
        return 0.0

    print("1) Guion (Groq)...")
    script = generate(lang)
    print(json.dumps(script, ensure_ascii=False, indent=2))

    if lang == "lb":
        print("AVISO: valida el texto LB con tu hablante nativo antes de publicar.")

    print("2) Montando película...")
    movie = build_movie(script, lang)

    if dry_run:
        print("[DRY-RUN] No se renderiza (0 créditos).")
        return 0.0

    print("3) Renderizando en JSON2Video...")
    url, duration = render_movie(movie)
    print(f"   MP4: {url}")
    print(f"   Duración: {duration:.1f} s -> {duration:.0f} créditos")

    with open(f"last_run_{lang}.json", "w", encoding="utf-8") as f:
        json.dump(
            {"lang": lang, "url": url, "duration_s": duration,
             "caption": script.get("caption"), "hashtags": script.get("hashtags")},
            f, ensure_ascii=False, indent=2,
        )
    return duration


def main():
    dry_run = "--dry-run" in sys.argv
    do_all = "--all" in sys.argv
    one_lang = _arg_value("--lang")

    if do_all:
        langs = config.LANGS
    elif one_lang:
        langs = [one_lang]
    else:
        langs = [config.DEFAULT_LANG]

    print(f"== Habliko Video == idiomas: {langs}"
          f"{'  (DRY-RUN)' if dry_run else ''}")

    total = 0.0
    rendered = 0
    for i, lang in enumerate(langs):
        total += run_one(lang, dry_run)
        if lang != "lb" or config.LB_ENABLED:
            rendered += 0 if dry_run else 1
        if i < len(langs) - 1:
            time.sleep(config.PAUSE_BETWEEN)

    # --- Informe agregado ---
    print("\n=========== RESUMEN ===========")
    print(f"Idiomas procesados: {len(langs)} | reels renderizados: {rendered}")
    if not dry_run and total > 0:
        print(f"Créditos gastados en esta tanda: {total:.0f} s")
        print(f"Tandas como esta que caben en GRATIS (600 s): "
              f"~{int(config.FREE_PLAN_SECONDS // total)}")
        print(f"Tandas como esta que caben en HOBBY (3000 s): "
              f"~{int(config.HOBBY_PLAN_SECONDS // total)}")
    elif dry_run:
        print("Modo dry-run: no se han gastado créditos.")


if __name__ == "__main__":
    main()
