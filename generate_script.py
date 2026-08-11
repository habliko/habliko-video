"""
Paso 1 — Genera el guion del reel, con CACHÉ para ahorrar tokens de Groq.

Lógica:
  1. Si hay guion cacheado y fresco (< CACHE_DAYS) -> se reutiliza (0 tokens).
  2. Si no, se pide a Groq y se guarda en caché.
  3. Si Groq falla (p. ej. rate-limit 429) pero hay caché aunque sea vieja -> se usa
     esa en vez de romper la tanda.

Para forzar guiones nuevos: variable de entorno REFRESH_GUION=1.
La caché son archivos cache/guion_<lang>.json (el workflow los va guardando).
"""
import json
import os
import sys
import time
import requests

import config

CACHE_DIR = getattr(config, "CACHE_DIR", "cache")
CACHE_DAYS = float(getattr(config, "CACHE_DAYS", 30))

SYSTEM = (
    "Eres un guionista de reels verticales muy directos para redes sociales. "
    "Devuelves EXCLUSIVAMENTE un objeto JSON válido, sin markdown, sin explicaciones, "
    "sin ```."
)

PROMPT_TEMPLATE = """\
Escribe el guion de un reel vertical de ~15 segundos en {lang_name} sobre este tema:

{topic}

Marca: {brand} ({url}). Tono: cercano, motivador, nada agresivo.

Estructura obligatoria: exactamente 3 escenas (gancho, desarrollo, llamada a la acción).
- 'voice_text': lo que dice la voz en off (1 frase corta y natural al hablar).
- 'on_screen': 3-6 palabras que aparecen en pantalla (NO repitas literalmente la voz).
- La escena 3 (llamada a la acción) debe invitar a la persona a convertirse en
  PROMOTOR/embajador de Habliko: transmite que "buscamos promotores" y anima a
  visitar habliko.com. El 'on_screen' de la escena 3 debe ser tipo "Buscamos promotores".
Todo el texto (voz, on_screen, caption, hashtags) debe estar en {lang_name}.

Devuelve SOLO este JSON:
{{
  "scenes": [
    {{"voice_text": "...", "on_screen": "..."}},
    {{"voice_text": "...", "on_screen": "..."}},
    {{"voice_text": "...", "on_screen": "..."}}
  ],
  "caption": "texto para la descripción del post (1-2 frases)",
  "hashtags": ["#...", "#...", "#..."]
}}
"""


def _cache_path(lang):
    return os.path.join(CACHE_DIR, f"guion_{lang}.json")


def _load_cache(lang, max_age_days=None):
    p = _cache_path(lang)
    if not os.path.exists(p):
        return None
    try:
        data = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    if max_age_days is not None:
        age_days = (time.time() - data.get("_ts", 0)) / 86400.0
        if age_days > max_age_days:
            return None
    return data.get("script")


def _save_cache(lang, script):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(_cache_path(lang), "w", encoding="utf-8") as f:
        json.dump({"_ts": time.time(), "lang": lang, "script": script},
                  f, ensure_ascii=False, indent=2)


def _call_llm(lang):
    """Genera el guion probando los proveedores en orden (Cerebras -> Groq).
    Si uno da 429 (cupo), salta al siguiente. Solo usa los que tengan key."""
    prompt = PROMPT_TEMPLATE.format(
        lang_name=config.LANG_NAMES.get(lang, "español"),
        topic=config.TOPIC, brand=config.BRAND["name"], url=config.BRAND["url"],
    )
    active = [p for p in config.AI_PROVIDERS if p.get("key")]
    if not active:
        raise RuntimeError("falta al menos una API key (CEREBRAS_API_KEY / GROQ_API_KEY)")

    last_err = None
    for prov in active:
        payload = {
            "model": prov["model"], "temperature": 0.7,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        }
        headers = {"Authorization": f"Bearer {prov['key']}",
                   "Content-Type": "application/json"}
        try:
            r = requests.post(prov["url"], headers=headers, json=payload, timeout=60)
        except Exception as e:
            last_err = e
            continue
        if r.status_code == 429:
            print(f"   {prov['name']} dio 429; pruebo el siguiente...", file=sys.stderr)
            last_err = RuntimeError(f"{prov['name']} 429")
            continue
        if r.status_code != 200:
            last_err = RuntimeError(f"{prov['name']} {r.status_code}: {r.text[:180]}")
            continue
        content = r.json()["choices"][0]["message"]["content"].strip()
        data = json.loads(content)
        if "scenes" not in data or not data["scenes"]:
            raise RuntimeError("guion sin escenas")
        if prov is not active[0]:
            print(f"   (respaldo: {prov['name']})")
        return data
    raise last_err or RuntimeError("Fallo la generacion en todos los proveedores")


def generate(lang: str, force: bool = False) -> dict:
    force = force or os.environ.get("REFRESH_GUION") == "1"

    # 1) Caché fresca (salvo que forcemos)
    if not force:
        cached = _load_cache(lang, CACHE_DAYS)
        if cached:
            print(f"   guion en caché (0 tokens Groq) [{lang}]")
            return cached

    # 2) Pedir a la IA (Cerebras -> Groq)
    try:
        script = _call_llm(lang)
        _save_cache(lang, script)
        print(f"   guion nuevo generado y cacheado [{lang}]")
        return script
    except Exception as e:
        # 3) Red de seguridad: usar caché aunque sea vieja
        cached = _load_cache(lang, None)
        if cached:
            print(f"   [aviso] Groq falló ({e}); uso guion en caché [{lang}]",
                  file=sys.stderr)
            return cached
        print(f"ERROR Groq y sin caché para [{lang}]: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else config.DEFAULT_LANG
    print(json.dumps(generate(lang), ensure_ascii=False, indent=2))
