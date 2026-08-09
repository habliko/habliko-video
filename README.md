# habliko-video

Fábrica de reels para Habliko, misma filosofía que tus repos de blog:
**Groq (guion, gratis) → JSON2Video (voz Azure + render) → YouTube Shorts**.

8 idiomas en bucle. Reels cortos (~13 s) para máximo volumen.

## Idiomas

| Idioma | Voz | Estado |
|--------|-----|--------|
| es, en, fr, de, it, pt, nl | Azure (gratis, incluida) | activo |
| lb (luxemburgués) | Liesmaschinn (ZLS) | hueco preparado, deferido |

## Uso

```bash
python main.py                   # un idioma (config.DEFAULT_LANG = es)
python main.py --lang fr         # un idioma concreto
python main.py --all             # los 8 idiomas (sin subir)
python main.py --all --publish   # los 8 idiomas + subir a YouTube Shorts (privado)
python main.py --all --dry-run   # solo guiones, sin renderizar (0 créditos)
```

Desde GitHub: Actions -> Habliko Video PoC -> Run workflow, elige el modo.
Cada idioma deja last_run_<lang>.json (URL del MP4, del Short y metadatos).

## Publicación en YouTube (configuración única)

La API de YouTube exige autorizar OAuth UNA vez. Después el cron sube solo con un
refresh token guardado como secret. Pasos resumidos:

1. Google Cloud: crea un proyecto y activa YouTube Data API v3.
2. Pantalla de consentimiento OAuth (Externo): añade tu cuenta como test user y
   PUBLICA la app ("In production") para que el refresh token NO caduque a los 7
   días. Scope: .../auth/youtube.upload
3. Credenciales -> OAuth client tipo "Web application". En Authorized redirect URIs
   añade https://developers.google.com/oauthplayground . Copia Client ID y Secret.
4. Consigue el refresh token (una vía):
   - OAuth Playground (sin Python): rueda dentada -> "Use your own OAuth credentials",
     pega ID y Secret; escribe el scope de youtube.upload, Authorize APIs, inicia
     sesión con la cuenta del canal, Exchange authorization code for tokens -> copia
     el refresh token.
   - En local: python auth_youtube.py (necesita client_secret.json).
5. GitHub -> Secrets: añade YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
6. Lanza el modo "8 idiomas + subir a YouTube (--all --publish)".

Las subidas van en PRIVADO por defecto (config.PUBLISH_PRIVACY): revisas y luego
las pasas a público o las programas. Los verticales < 60 s son Shorts (se añade #Shorts).

## Consumo de referencia

Tanda de 7 idiomas (~13 s c/u) ~= 92 créditos -> ~6 tandas en gratis, ~32 en Hobby.

## Pendiente

- Integrar Liesmaschinn para el LB (liesmaschinn.py -> synthesize()).
- Publicación en TikTok (borrador sin auditoría, o API auditada de terceros).
- Enchufar Foxi / logo desde media.habliko.com (BRAND["logo_url"]).
