from discord.ext import commands
import discord
from bot.core.config import DISCORD_TOKEN, PREFIX

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

async def setup_hook():
    async def safe_load(name: str) -> bool:
        try:
            await bot.load_extension(name)
            print(f"✅ Loaded extension {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to load extension {name}: {e}")
            return False

    # Load legacy (prefix) commands
    legacy_extensions = [
        "bot.commands.legacy.chat",
        "bot.commands.legacy.general", 
        "bot.commands.legacy.voice_channel",
        "bot.commands.legacy.smart_help",
    ]
    
    print("Loading legacy commands...")
    for ext in legacy_extensions:
        await safe_load(ext)
    
    # Load regular commands that are not in subdirectories
    regular_extensions = [
        "bot.commands.quick_actions",
    ]
    
    print("Loading regular commands...")
    for ext in regular_extensions:
        await safe_load(ext)
    
    # Load slash commands
    slash_extensions = [
        "bot.commands.slash.slash_info",
        "bot.commands.slash.slash_chat", 
        "bot.commands.slash.slash_music",
    ]
    
    print("Loading slash commands...")
    for ext in slash_extensions:
        await safe_load(ext)
    
    print("Discord slash commands loaded successfully.")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synced globally: {len(synced)} registered")
        if synced:
            command_names = [cmd.name for cmd in synced]
            print(f"📋 Registered commands: {command_names}")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")

def main():
    bot.setup_hook = setup_hook
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
