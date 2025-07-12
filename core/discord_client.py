import discord
from discord.ext import commands
from core.config import DISCORD_TOKEN, DISCORD_CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

channel = None # cache de canal


@bot.event
async def on_ready():
    global channel
    print(f"✅ Bot conectado como {bot.user}")

    # Intentar obtener canal cacheado
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    print(f"🔍 Canal obtenido por caché: {channel}")

    if channel is None:
        try:
            channel = await bot.fetch_channel(DISCORD_CHANNEL_ID)
            print(f"📢 Canal obtenido por fetch: {channel}")
        except Exception as e:
            print(f"❌ Error al obtener canal por fetch: {e}")

def run_bot():
    bot.run(DISCORD_TOKEN)

