from discord.ext import commands
from bot.core.llm.chat_service import generate_chat_response
from bot.utils.dicts.ia_prompt import IA_PROMPT

class Chat(commands.Cog):
    """Cog que provee un comando con prefijo para compatibilidad.

    Nota: el comportamiento principal de chat se realiza por el SlashCommand `/chat`.
    Aquí mantenemos un comando con prefijo `!chat` que delega en el servicio
    compartido para evitar duplicación de lógica.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chat")
    async def chat(self, ctx, *, prompt: str):
        """Delegar al mismo servicio que usa `/chat` (mantener compatibilidad)."""
        thinking = await ctx.send("🤔 Pensando...")

        try:

            messages = [
                IA_PROMPT.copy(),
                {"role": "user", "content": prompt},
            ]

            partes = await generate_chat_response(messages)
            for parte in partes:
                await ctx.send(parte)

        except Exception as e:
            await ctx.send("❌ Error al contactar a la IA.")
            print(f"❌ Error: {e}")

        finally:
            await thinking.delete()

    @commands.command(name="help_chat", help="Get help for chat command")
    async def help_chat(self, ctx):
        """Provide help information for the chat command."""
        help_message = (
            "- Usa `/chat <mensaje>` (recomendado) o `!chat <mensaje>` para compatibilidad.\n"
            "- `/chat` tiene autocompletado y mejor UI en Discord." 
        )
        await ctx.send(help_message)


async def setup(bot):
    await bot.add_cog(Chat(bot))
