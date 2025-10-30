import discord
from discord import app_commands
from discord.ext import commands
import requests

class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", help="Comprueba si el bot responde")
    async def ping(self, ctx: commands.Context):
        """Prefix compatibility for ping to help testing when slash commands aren't available."""
        latency_ms = round(self.bot.latency * 1000) if getattr(self.bot, "latency", None) is not None else "N/A"
        await ctx.send(f"🏓 Pong! Latencia: {latency_ms}ms")

    @commands.command(name="serverinfo", help="Información básica del servidor")
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        if not guild:
            await ctx.send("Este comando sólo funciona en servidores.")
            return
        embed = discord.Embed(title=f"Información - {guild.name}", color=0x00CCFF)
        embed.add_field(name="ID", value=str(guild.id), inline=True)
        embed.add_field(name="Miembros", value=str(guild.member_count), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", help="Información de un usuario")
    async def userinfo(self, ctx: commands.Context, user: discord.Member = None):
        target = user or ctx.author
        embed = discord.Embed(title=f"Usuario - {target.display_name}", color=0x88CCFF)
        embed.add_field(name="ID", value=str(target.id), inline=True)
        embed.add_field(name="Cuenta creada", value=str(target.created_at), inline=True)
        embed.add_field(name="Top role", value=str(target.top_role), inline=True)
        await ctx.send(embed=embed)

    @app_commands.command(
        name="clima",
        description="Muestra el clima de una lista de ciudades (separadas por comas)."
    )
    async def clima(self, interaction: discord.Interaction, cities: str | None = None):
        await interaction.response.defer()  # dar tiempo mientras se consulta la API

        if not cities:
            city_list = ['Medellin', 'Bello', 'Bogota', 'El Retiro, Antioquia']
        else:
            # aceptar lista separada por comas: "Medellin, Bogota, ...".
            city_list = [c.strip() for c in cities.split(',') if c.strip()]

        city_list = city_list[:5]  # limitar peticiones

        results = []
        for city in city_list:
            try:
                resp = requests.get(f'https://wttr.in/{city}?format=j1', timeout=6)
                if resp.status_code != 200:
                    results.append(f"{city.lower()} - ❌ no disponible")
                    continue

                j = resp.json()
                cur = j.get('current_condition', [{}])[0]
                temp_c = cur.get('temp_C')
                desc = cur.get('weatherDesc', [{}])[0].get('value', 'N/A')

                if temp_c is None:
                    temp = cur.get('temp_F', 'N/A')
                    unit = '°F' if temp != 'N/A' else ''
                else:
                    temp = temp_c
                    unit = '°C'

                results.append(f"{city.lower()} - {temp}{unit} - {desc.lower()}")
            except Exception as e:
                # logging simple por ahora
                print(f"❌ Error en clima(): {e}")
                results.append(f"{city.lower()} - ❌ error")

        await interaction.followup.send("\n".join(results))

    @app_commands.command(
        name="cls",
        description="Limpia mensajes del canal. Límite máximo 100."
    )
    async def cls(self, interaction: discord.Interaction, limit: int = 50):
        # permisos del usuario
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                '🚫 No tienes permisos para borrar mensajes.',
                ephemeral=True
            )
            return

        # validar y normalizar límite
        if limit < 1:
            await interaction.response.send_message(
                '🔢 Proporciona un número positivo de mensajes a borrar.',
                ephemeral=True
            )
            return
        if limit > 100:
            limit = 100

        # defer porque purge puede tomar tiempo
        await interaction.response.defer(ephemeral=True)
        try:
            channel = interaction.channel
            # incluir el mensaje del comando en la purga sumando 1
            deleted = await channel.purge(limit=limit + 1)
            deleted_count = len(deleted) - (1 if interaction.message in deleted else 0)
            await interaction.followup.send(
                f'🧹 Chat limpiado: {deleted_count} mensajes eliminados.',
                ephemeral=True
            )
        except Exception as e:
            print(f"❌ Error limpiando chat: {e}")
            await interaction.followup.send(
                '❌ Ocurrió un error al intentar limpiar el chat.',
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCommands(bot))
    print("Discord slash commands loaded successfully.")