import logging
from typing import Optional
from bot.utils.dicts.command_db import command_db
from bot.utils.help_utils import (
    get_command_by_name_or_alias,
    find_similar_commands,
    build_general_help_embed,
    build_command_detail_embed,
    build_suggestions_embed,
    build_no_results_embed,
)

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class SmartHelp(commands.Cog):
    """Cog de compatibilidad que reutiliza las utilidades de ayuda.

    Este cog mantiene el comando por prefijo `!ayuda` para usuarios legacy, pero
    toda la lógica de búsqueda/embeds está centralizada en `utils.help_utils`.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.command_database = command_db

    @commands.command(name="help", aliases=["ayuda", "comandos", "help_smart"])
    async def smart_help(self, ctx: commands.Context, *, query: Optional[str] = None):
        try:
            if not query:
                embed = build_general_help_embed(self.command_database)
                # Check whether slash commands are available in this guild and add a note if missing
                try:
                    if ctx.guild:
                        remote = await self.bot.tree.fetch_commands(guild=discord.Object(id=ctx.guild.id))
                        if not remote:
                            embed.add_field(
                                name="⚠️ Comandos slash no disponibles",
                                value=(
                                    "Parece que los comandos slash no están registrados en este servidor. "
                                    "Para habilitarlos, re-invita el bot con scope `applications.commands` o contacta al administrador."
                                ),
                                inline=False,
                            )
                except Exception:
                    # Non-fatal: if fetching fails, don't block help delivery
                    logger.debug("No se pudo comprobar comandos slash: excepción silenciada")

                await ctx.send(embed=embed)
                return

            exact = get_command_by_name_or_alias(self.command_database, query)
            if exact:
                name, info = exact
                embed = build_command_detail_embed(name, info)
                await ctx.send(embed=embed)
                return

            suggestions = find_similar_commands(self.command_database, query)
            if suggestions:
                embed = build_suggestions_embed(query, suggestions)
                await ctx.send(embed=embed)
            else:
                embed = build_no_results_embed(query, self.command_database)
                await ctx.send(embed=embed)
        except Exception:
            logger.exception("Error en smart_help")
            await ctx.send("Ocurrió un error al obtener la ayuda. Intenta nuevamente más tarde.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        try:
            if isinstance(error, commands.CommandNotFound):
                content = getattr(ctx.message, "content", "") if ctx.message else ""
                prefix = getattr(ctx, "prefix", None) or getattr(self.bot, "command_prefix", "")
                attempted = content
                if prefix and isinstance(prefix, str) and content.startswith(prefix):
                    attempted = content[len(prefix) :].strip()
                failed = attempted.split()[0] if attempted else ""

                suggestions = find_similar_commands(self.command_database, failed)
                if suggestions:
                    embed = discord.Embed(
                        title="❓ Comando no encontrado",
                        description=f"No reconozco `{failed}`. ¿Te refieres a alguno de estos?",
                        color=0xFFAA00,
                    )
                    for s in suggestions[:3]:
                        cmd = s["command"]
                        info = s["info"]
                        embed.add_field(name=f"🔍 {cmd}", value=f"`{info.get('usage', '—')}`\n{info.get('description','—')}", inline=True)
                    embed.set_footer(text="💡 Usa `!help` o `/menu` para ver el menú rápido")
                    await ctx.send(embed=embed, delete_after=30)
                else:
                    logger.debug("No se encontraron sugerencias para comando perdido: %s", failed)
        except Exception:
            logger.exception("Error en on_command_error de SmartHelp")


async def setup(bot: commands.Bot):
    await bot.add_cog(SmartHelp(bot))