from typing import List

from bot.utils.limpieza import limpiar_respuesta, dividir_mensaje
from .groq_adapter import query_groq

async def generate_chat_response(messages: List[dict]) -> List[str]:

    """Genera una respuesta usando el adaptador LLM y devuelve una lista de partes.

    - Llama a query_groq (u otro adaptador en el futuro)
    - Limpia la respuesta
    - La divide en partes de hasta 2000 caracteres
    """
    # Llamada al LLM
    raw = await query_groq(messages)

    # Limpieza y división
    cleaned = limpiar_respuesta(raw)
    parts = dividir_mensaje(cleaned)

    # Asegurar que devolvemos al menos una cadena
    if not parts:
        return [""]
    return parts
