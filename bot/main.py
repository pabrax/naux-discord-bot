from discord.ext import commands
from core.config import DISCORD_TOKEN
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
@bot.event
async def setup_hook():
    print("Setting up hooks...")
    await bot.load_extension("bot.commands.chat")  # Load the chat command
    await bot.load_extension("bot.commands.discord_commands")  # Load the discord commands

def run_bot():
    bot.run(DISCORD_TOKEN)