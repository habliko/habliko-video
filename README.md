# habliko-video

Fábrica de reels para Habliko, misma filosofía que tus repos de blog:
**Groq (guion, gratis) → JSON2Video (voz Azure + render) → YouTube/TikTok**.

Ahora en **8 idiomas en bucle**. Reels cortos (~13-15 s) para máximo volumen.

## Idiomas

| Idioma | Voz | Estado |
|--------|-----|--------|
| es, en, fr, de, it, pt, nl | Azure (gratis, incluida) | ✅ activo |
| lb (luxemburgués) | Liesmaschinn (ZLS) | 🔌 hueco preparado, deferido |

El LB no tiene voz en Azure. Se salta automáticamente hasta que integres tu
Liesmaschinn en `liesmaschinn.py` y pongas `LB_ENABLED = True` en `config.py`.

## Uso

```bash
python main.py                  # un idioma (config.DEFAULT_LANG = es)
python main.py --lang fr        # un idioma concreto
python main.py --all            # los 8 idiomas en bucle
python main.py --all --dry-run  # genera los 8 guiones SIN renderizar (0 créditos)
```

Desde GitHub: pestaña **Actions → Habliko Video PoC → Run workflow**, y elige en el
desplegable *mode*: solo español, los 8 idiomas, o dry-run de los 8 (0 créditos).

Al terminar verás, por idioma, la URL del MP4 y los segundos = créditos, más un
**resumen agregado** de cuántas tandas caben en gratis y en Hobby. Cada idioma deja
su registro en `last_run_<lang>.json` (se suben como artefacto).

## Consumo de referencia

Con reels de ~13 s: una tanda de 7 idiomas (LB deferido) ≈ **90 s**.
→ ~6 tandas completas en el plan gratis (600 s), ~33 en Hobby (3.000 s).

## Ajustes

Todo en `config.py`: marca y colores (`BRAND`), lista de idiomas (`LANGS`),
voces Azure (`VOICES`), tema (`TOPIC`), flag `LB_ENABLED`, ritmo entre idiomas.

## Pendiente (siguientes fases)

- Integrar Liesmaschinn para el LB (`liesmaschinn.py` → `synthesize()`).
- Subida a YouTube Shorts (`upload_youtube.py`, ya listo, OAuth una vez).
- Publicación en TikTok (modo borrador sin auditoría, o API auditada de terceros).
- Enchufar tu Foxi / logo desde `media.habliko.com` (`BRAND["logo_url"]`).
