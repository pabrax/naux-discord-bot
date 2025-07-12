import discord
from discord.ext import commands
import requests

class DiscordCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 Pong!")

    @commands.command()
    async def hola(self, ctx):
        await ctx.send('Hello World')

    @commands.command()
    async def poke(self, ctx, pokemon: str = None):
        if not pokemon:
            await ctx.send("❗ Debes escribir el nombre de un Pokémon")
            return
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}')
            if response.status_code != 200:
                await ctx.send('❌ Pokémon no encontrado')
                return

            data = response.json()
            await ctx.send(data['sprites']['front_default'])
        except Exception as e:
            print(f"❌ Error en poke(): {e}")
            await ctx.send('❌ Ocurrió un error')

    @commands.command()
    async def cls(self, ctx):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send('🚫 No tienes permisos para borrar mensajes.', delete_after=5)
            return
        await ctx.channel.purge()
        await ctx.send('🧹 Chat limpiado', delete_after=3)

# 👇 Esto es lo que permite cargar esta clase como extensión
async def setup(bot):
    await bot.add_cog(DiscordCommands(bot))
    print("Discord commands loaded successfully.")