import discord
from discord import app_commands
from discord.ext import commands
from bot.core.llm.chat_service import generate_chat_response
from bot.utils.dicts.ia_prompt import IA_PROMPT

class SlashChat(commands.Cog):
    """Comando /chat usando el servicio centralizado de LLM (core.llm.chat_service)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chat", description="Chatea con la IA integrada")
    @app_commands.describe(prompt="Mensaje o pregunta para la IA")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        # Defer the response because LLM calls can take time
        await interaction.response.defer(thinking=True)
        try:
            # Import inside handler to avoid cycles during startup

            messages = [
                IA_PROMPT.copy(),
                {"role": "user", "content": prompt},
            ]

            partes = await generate_chat_response(messages)

            # Send as followups after the deferred response
            for parte in partes:
                await interaction.followup.send(parte)

        except Exception as e:
            await interaction.followup.send("❌ Error al contactar la IA. Intenta de nuevo más tarde.")
            self.bot.loop.call_soon_threadsafe(print, f"Error en /chat: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(SlashChat(bot))
