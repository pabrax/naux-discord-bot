from typing import Optional, List
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.dicts.command_db import command_db
from bot.utils.help_utils import (
    build_general_help_embed,
    get_command_by_name_or_alias,
    find_similar_commands,
    build_command_detail_embed,
    build_suggestions_embed,
    build_no_results_embed,
)


class SlashInfo(commands.Cog):
    """Comandos de información básicos: /help, /ping, /serverinfo, /userinfo"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _autocomplete_help(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        if not current:
            return []
        results = find_similar_commands(command_db, current)[:25]
        choices = []
        for r in results:
            name = r["command"]
            desc = r["info"].get("description", "")
            choices.append(app_commands.Choice(name=f"{name} — {desc[:50]}", value=name))
        return choices

    @app_commands.command(name="help", description="Ayuda inteligente de Naux")
    @app_commands.describe(query="Comando o palabra clave")
    @app_commands.autocomplete(query=_autocomplete_help)
    async def help(self, interaction: discord.Interaction, query: Optional[str] = None):
        # Prefer ephemeral responses for help
        if not query:
            embed = build_general_help_embed(command_db)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        exact = get_command_by_name_or_alias(command_db, query)
        if exact:
            name, info = exact
            embed = build_command_detail_embed(name, info)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        suggestions = find_similar_commands(command_db, query)
        if suggestions:
            embed = build_suggestions_embed(query, suggestions)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = build_no_results_embed(query, command_db)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Verifica la latencia del bot")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latencia: {latency_ms}ms", ephemeral=True)

    @app_commands.command(name="serverinfo", description="Información básica del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Este comando sólo funciona en servidores.", ephemeral=True)
            return
        embed = discord.Embed(title=f"Información - {guild.name}", color=0x00CCFF)
        embed.add_field(name="ID", value=str(guild.id), inline=True)
        embed.add_field(name="Miembros", value=str(guild.member_count), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="Información de un usuario")
    @app_commands.describe(user="Usuario a inspeccionar (opcional)")
    async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        target = user or interaction.user
        embed = discord.Embed(title=f"Usuario - {target.display_name}", color=0x88CCFF)
        embed.add_field(name="ID", value=str(target.id), inline=True)
        embed.add_field(name="Cuenta creada", value=str(target.created_at), inline=True)
        embed.add_field(name="Top role", value=str(target.top_role), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SlashInfo(bot))
