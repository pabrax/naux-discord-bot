import threading
import uvicorn
from fastapi import FastAPI
from core.discord_client import run_bot
from api.webhook import router as webhook_router
import bot.commands  # importa para registrar comandos

app = FastAPI()
app.include_router(webhook_router)

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=start_fastapi, daemon=True).start()
    run_bot()




# # main.py

# import os
# import threading
# import asyncio
# import discord
# from discord.ext import commands
# from fastapi import FastAPI, Request
# import uvicorn
# from dotenv import load_dotenv

# # ------------------ Cargar variables de entorno ------------------
# load_dotenv()
# TOKEN = os.getenv("DISCORD_TOKEN")
# DISCORD_CHANNEL_ID = 1393377609991196798  # Reemplaza con el ID correcto

# # ------------------ Inicializar Discord Bot ------------------
# intents = discord.Intents.default()
# intents.message_content = True

# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     global channel
#     channel = bot.get_channel(DISCORD_CHANNEL_ID)
#     print(f"✅ Bot conectado como {bot.user}")

# @bot.command()
# async def ping(ctx):
#     await ctx.send("🏓 Pong!")
#     loop = asyncio.get_running_loop()
#     print(f"👀 Loop actual (Discord): {loop}")

# # ------------------ Inicializar FastAPI ------------------
# app = FastAPI()

# @app.post("/webhook/github")
# async def github_webhook(request: Request):
#     payload = await request.json()
#     repo = payload.get("repository", {}).get("full_name", "sin repositorio")

#     async def notificar():
#         try:
#             channel = await bot.fetch_channel(DISCORD_CHANNEL_ID)
#             await channel.send(f"📢 ¡Nuevo push en el repositorio `{repo}`!")
#         except Exception as e:
#             print(f"❌ Error al enviar mensaje a Discord: {e}")
    
#     # conocer el loop de fastapi
#     loop = asyncio.get_event_loop()
#     print(f"👀 Loop actual (FastAPI): {loop}")

#     bot.loop.create_task(notificar())  # Ejecuta sin bloquear el webhook
#     return {"status": "ok"}

# # ------------------ Ejecutar FastAPI en paralelo ------------------
# def start_fastapi():
#     print("🚀 Iniciando FastAPI en http://0.0.0.0:8000")
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # ------------------ Entrypoint ------------------
# if __name__ == "__main__":
#     # Ejecutar FastAPI en otro hilo
#     threading.Thread(target=start_fastapi, daemon=True).start()
#     # Iniciar el bot de Discord
#     bot.run(TOKEN)
