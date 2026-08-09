# habliko-video (prueba de concepto)

Fábrica de reels para Habliko, misma filosofía que tus repos de blog:
**Groq (guion, gratis) → JSON2Video (voz Azure + render) → YouTube/TikTok**.

Esta versión está calibrada para el **plan gratuito de JSON2Video** (600 s = 10 min/mes)
y su único objetivo es **medir el consumo real de créditos** con tu plantilla y tu duración.

## Flujo

| Paso | Archivo | Coste |
|------|---------|-------|
| 1. Guion del reel | `generate_script.py` (Groq `gpt-oss-120b`) | 0 € |
| 2. Montaje de la película | `build_movie.py` (1080×1920 vertical) | 0 € |
| 3. Render + voz | `render.py` (JSON2Video, voz Azure incluida) | seg. de vídeo |
| 4. Subida (siguiente fase) | `upload_youtube.py` | 0 € |

## Puesta en marcha (test gratis)

1. Crea una cuenta gratis en JSON2Video y copia tu **API key**.
2. En GitHub → *Settings → Secrets and variables → Actions*, añade:
   - `GROQ_API_KEY` (tu clave Groq de siempre)
   - `JSON2VIDEO_API_KEY` (la del plan gratis)
3. (Opcional) prueba en local:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env      # rellena tus claves
   export $(grep -v '^#' .env | xargs)
   python main.py --dry-run  # solo guion, 0 créditos
   python main.py            # genera el reel de verdad
   ```
4. O lánzalo desde la pestaña **Actions** con *Run workflow* (manual).

Al terminar, la consola te dice:
- la URL del MP4,
- los **segundos = créditos** que ha costado,
- cuántos reels como ese caben en el plan gratis y en Hobby.

## Notas

- **Resolución:** 1080×1920 vertical = tarifa base (1 crédito/segundo). Nunca 4K.
- **Voz:** Azure (gratis, incluida). Cubre ES/EN/FR/DE/IT/PT/NL.
  El **luxemburgués** se resolverá aparte con tu Liesmaschinn (pista de audio propia).
- **TikTok:** el módulo de publicación se añade en la siguiente fase
  (borrador sin auditoría, o API auditada de terceros).
- Todo lo que quieras cambiar (marca, colores, idioma, tema) está en `config.py`.
