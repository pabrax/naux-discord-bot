import re

def limpiar_respuesta(respuesta: str) -> str:
    # Quitar bloques <think>...</think>
    respuesta = re.sub(r"<think>.*?</think>", "", respuesta, flags=re.DOTALL)

    # También puedes quitar espacios extra
    return respuesta.strip()

def dividir_mensaje(texto, max_len=2000):
    partes = []
    while len(texto) > max_len:
        corte = texto.rfind('\n', 0, max_len)
        if corte == -1:
            corte = max_len
        partes.append(texto[:corte])
        texto = texto[corte:].lstrip()
    if texto:
        partes.append(texto)
    return partes
