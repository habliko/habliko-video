"""
Paso 1 — Genera el guion del reel con Groq (gratis).
Devuelve un dict con: scenes[], caption, hashtags.
Cada escena trae 'voice_text' (lo que se narra) y 'on_screen' (texto en pantalla).
"""
import json
import sys
import requests

import config


SYSTEM = (
    "Eres un guionista de reels verticales muy directos para redes sociales. "
    "Devuelves EXCLUSIVAMENTE un objeto JSON válido, sin markdown, sin explicaciones, "
    "sin ```."
)

PROMPT_TEMPLATE = """\
Escribe el guion de un reel vertical de ~30 segundos en {lang_name} sobre este tema:

{topic}

Marca: {brand} ({url}). Tono: cercano, motivador, nada agresivo.

Estructura obligatoria: exactamente 3 escenas (gancho, desarrollo, llamada a la acción).
- 'voice_text': lo que dice la voz en off (1-2 frases cortas, natural al hablar).
- 'on_screen': 3-6 palabras que aparecen en pantalla (NO repitas literalmente la voz).
La suma de la narración debe caber holgada en ~30 segundos.

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


def generate() -> dict:
    if not config.GROQ_API_KEY:
        print("ERROR: falta GROQ_API_KEY en el entorno.", file=sys.stderr)
        sys.exit(1)

    prompt = PROMPT_TEMPLATE.format(
        lang_name=config.LANG_NAMES.get(config.LANG, "español"),
        topic=config.TOPIC,
        brand=config.BRAND["name"],
        url=config.BRAND["url"],
    )

    payload = {
        "model": config.GROQ_MODEL,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        # Fuerza salida JSON en modelos compatibles con Groq.
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    r = requests.post(config.GROQ_URL, headers=headers, json=payload, timeout=60)
    if r.status_code != 200:
        print(f"ERROR Groq {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    content = r.json()["choices"][0]["message"]["content"].strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print(f"ERROR: Groq no devolvió JSON válido:\n{content}", file=sys.stderr)
        sys.exit(1)

    if "scenes" not in data or not data["scenes"]:
        print(f"ERROR: guion sin escenas: {data}", file=sys.stderr)
        sys.exit(1)

    return data


if __name__ == "__main__":
    print(json.dumps(generate(), ensure_ascii=False, indent=2))
