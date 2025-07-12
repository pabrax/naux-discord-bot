from fastapi import APIRouter, Request
from core.discord_client import bot
from core.config import DISCORD_CHANNEL_ID

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    repo = payload.get("repository", {}).get("full_name", "sin repositorio")

    print(f"📬 Webhook recibido para repo: {repo}")

    async def notificar():
        try:
            channel = await bot.fetch_channel(DISCORD_CHANNEL_ID)  # 👈 canal siempre válido
            await channel.send(f"📢 ¡Nuevo push en el repositorio `{repo}`!")
            print("✅ Notificación enviada a Discord.")
        except Exception as e:
            print(f"❌ Error al enviar a Discord: {e}")

    bot.loop.create_task(notificar())  # asíncrono y rápido
    return {"status": "ok"}