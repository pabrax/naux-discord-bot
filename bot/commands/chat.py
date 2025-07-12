from discord.ext import commands
from core.groq_model import query_groq
from utils.limpieza import limpiar_respuesta, dividir_mensaje

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chat")
    async def chat(self, ctx, *, prompt: str):
        thinking = await ctx.send("🤔 Pensando...")

        messages = [
            {"role": "system", "content": "Eres un asistente directo y útil. Evita rodeos innecesarios. Responde siempre en español. Eres un bot de Discord llamado Naux"},
            {"role": "user", "content": prompt}
        ]

        try:
            respuesta = await query_groq(messages)
            respuesta = limpiar_respuesta(respuesta)

            partes = dividir_mensaje(respuesta)
            for parte in partes:
                await ctx.send(parte)

        except Exception as e:
            await ctx.send("❌ Error al contactar a la IA.")
            print(f"❌ Error: {e}")
        finally:
            await thinking.delete()

    @commands.command(name='help_chat', help='Get help for chat command')
    async def help_chat(self, ctx):
        """Provide help information for the chat command."""
        help_message = (
            "- Use the `!chat <message>` command to chat with the AI model.\n"
            "- Example: `!chat Hello, how are you?`"
        )
        await ctx.send(help_message)

async def setup(bot):
    await bot.add_cog(Chat(bot))
