from discord.ext import commands
from core.config import DISCORD_TOKEN, PREFIX
from bot.commands.voice_channel import setup as setup_voice_channel
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.event
async def setup_hook():
    print("Setting up hooks...")
    await bot.load_extension("bot.commands.chat")
    await bot.load_extension("bot.commands.discord_commands")
    await bot.load_extension("bot.commands.voice_channel")

def main():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
