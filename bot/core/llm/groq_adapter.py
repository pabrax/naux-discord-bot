import httpx
from bot.core.config import ia_settings


async def query_groq(messages):
    url = ia_settings.IA_API_URL

    headers = {
        "Authorization": f"Bearer {ia_settings.IA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": ia_settings.IA_MODEL_NAME,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 1024,
        "top_p": 0.95,
        "stream": False  # Si quieres streaming, lo ajustamos luego
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Error {e.response.status_code}: {e.response.text}")
            raise

        data = response.json()
        return data["choices"][0]["message"]["content"]
