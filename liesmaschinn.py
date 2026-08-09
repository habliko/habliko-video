"""
Hueco preparado para la voz luxemburguesa (LB) vía Liesmaschinn (ZLS).

Azure no tiene luxemburgués, así que el LB no se genera con la voz de JSON2Video.
Este módulo es el ÚNICO punto que hay que implementar para activar el LB:
cuando 'synthesize()' devuelva una URL de audio hosteada, pon config.LB_ENABLED = True
y el bucle renderizará el LB usando un elemento de audio en cada escena.

Especificaciones conocidas de tu integración (para cuando lo implementes):
- Clave: LIESMASCHINN_TTS_KEY (ya está en el Worker shrill-unit-abd8).
- Auth por sesión; salida WAV a 22050 Hz; voces: 'claude', 'max', 'maxine'.
- Uso no comercial (encaja con el LB gratis para todos los usuarios).
- Preprocesado del texto: comillas rizadas -> rectas; normalizar a UTF-8 NFC.
- Flujo previsto: sintetizar el WAV -> subirlo a R2 (media.habliko.com)
  -> devolver aquí la URL pública para usarla como 'src' del elemento audio.

Mientras no esté implementado, 'synthesize()' devuelve None y el bucle salta el LB.
"""
from typing import Optional


def preprocess(text: str) -> str:
    """Comillas rizadas -> rectas y normalización NFC (según tu integración)."""
    import unicodedata
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    return unicodedata.normalize("NFC", text)


def synthesize(text: str, voice: str = "max") -> Optional[str]:
    """
    Debe devolver una URL pública (https) de un audio con la locución del `text`
    en luxemburgués, lista para usarse como 'src' de un elemento audio en JSON2Video.

    TODO (integración futura):
      1. text = preprocess(text)
      2. Abrir sesión y llamar a la API de Liesmaschinn con LIESMASCHINN_TTS_KEY.
      3. Recibir el WAV (22050 Hz), subirlo a R2 (media.habliko.com).
      4. return url_publica_del_wav

    Por ahora, sin implementar:
    """
    return None
