import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.dicts.command_db import command_db
from bot.utils.help_utils import build_general_help_embed
from bot.utils.ui_helpers import MenuView, MenuButton, BackCloseView, BackButton, CloseButton

class QuickActions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reaction_timeout = 30.0  # tiempo de expiración para vistas
        # Mapear acciones a métodos (útil si quieres extender)
        self.emoji_actions = {
            "music_menu": self._create_music_embed,
            "chat_menu": self._create_chat_embed,
            "tools_menu": self._create_tools_embed,
            "help_menu": self._create_help_embed,
            "status_menu": self._create_status_embed,
        }

    # Slash command
    @app_commands.command(name="menu", description="Menú rápido de Naux con acceso por botones")
    async def menu(self, interaction: discord.Interaction):
        """Envía el menú principal como un slash command usando Buttons"""
        await self._show_main_menu(interaction)

    # Prefix compatibility: allow legacy users to call !menu
    @commands.command(name="menu")
    async def menu_prefix(self, ctx: commands.Context):
        """Enviar el menú principal con prefijo para compatibilidad."""
        embed = discord.Embed(
            title="🚀 Menú Rápido de Naux",
            description="Pulsa un botón para acceder rápidamente:",
            color=0x00ff00
        )

        embed.add_field(name="🎵 Música", value="Comandos de reproducción", inline=True)
        embed.add_field(name="🤖 Chat IA", value="Conversar con Naux", inline=True)
        embed.add_field(name="🔧 Herramientas", value="Scripts y servicios", inline=True)
        embed.add_field(name="❓ Ayuda", value="Comandos disponibles", inline=True)
        embed.add_field(name="📊 Estado", value="Estado del bot", inline=True)
        embed.set_footer(text=f"⏱️ Este menú expira en {self.reaction_timeout} segundos")

        view = MenuView(self, ctx.author, timeout=self.reaction_timeout)
        await ctx.send(embed=embed, view=view)

    async def _show_main_menu(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🚀 Menú Rápido de Naux",
            description="Pulsa un botón para acceder rápidamente:",
            color=0x00ff00
        )

        embed.add_field(name="🎵 Música", value="Comandos de reproducción", inline=True)
        embed.add_field(name="🤖 Chat IA", value="Conversar con Naux", inline=True)
        embed.add_field(name="🔧 Herramientas", value="Scripts y servicios", inline=True)
        embed.add_field(name="❓ Ayuda", value="Comandos disponibles", inline=True)
        embed.add_field(name="📊 Estado", value="Estado del bot", inline=True)
        embed.set_footer(text=f"⏱️ Este menú expira en {self.reaction_timeout} segundos")

        view = MenuView(self, interaction.user, timeout=self.reaction_timeout)

        # Si interaction no ha respondido aún, usamos response.send_message; si ya respondió, editamos.
        if not interaction.response.is_done():
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.edit_original_response(embed=embed, view=view)

    async def _handle_menu_action_interaction(self, interaction: discord.Interaction, action: str, parent_view: discord.ui.View):
        """
        Maneja la acción seleccionada desde un botón. Edita el mensaje con el embed correspondiente
        y añade botones de 'volver' y 'cerrar'.
        """
        # Obtener el creador del embed desde el mapeo
        creator = self.emoji_actions.get(action)
        if not creator:
            await interaction.response.send_message("Acción desconocida.", ephemeral=True)
            return

        embed = creator()  # crear embed correspondiente
        # Set footer con info de expiración para consistencia
        embed.set_footer(text=f"⏱️ Este menú expira en {self.reaction_timeout} segundos")

        # Vista con botones de volver y cerrar
        back_view = BackCloseView(self, parent_view.author if hasattr(parent_view, "author") else interaction.user, timeout=self.reaction_timeout)

        # Editar el mensaje original en respuesta a la interacción del botón
        await interaction.response.edit_message(embed=embed, view=back_view)

    # --- Creadores de embeds (refactorizados) ---
    def _create_music_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🎵 Comandos de Música",
            description="Comandos disponibles para reproducción:",
            color=0xff6b6b
        )
        commands_list = [
            ("🎶 `!play <url>`", "Reproducir o añadir a la cola"),
            ("⏭️ `!skip`", "Saltar canción actual"),
            ("📜 `!queue`", "Mostrar cola"),
            ("🎧 `!np`", "Mostrar canción actual"),
            ("🔊 `!volume <0-100>`", "Ajustar volumen"),
            ("🧹 `!clear`", "Vaciar cola"),
            ("🔁 `!loop`", "Alternar repetición"),
            ("🔗 `!connect`", "Conectar a tu canal de voz"),
            ("📤 `!disconnect`", "Desconectar del canal")
        ]
        for emoji_cmd, desc in commands_list:
            embed.add_field(name=emoji_cmd, value=desc, inline=False)
        embed.set_footer(text="💡 Tip: Debes estar en un canal de voz para usar música")
        return embed

    def _create_chat_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🤖 Chat con IA",
            description="Formas de conversar con Naux:",
            color=0x4ecdc4
        )
        embed.add_field(
            name="💬 Comando clásico",
            value="`!chat <tu mensaje>`\n*Ejemplo: !chat Hola, ¿cómo estás?*",
            inline=False
        )
        embed.add_field(
            name="⚡ Comando slash (recomendado)",
            value="`/naux <mensaje>`\n*Tiene autocompletado y mejor interfaz*",
            inline=False
        )
        embed.add_field(
            name="🎯 Ejemplos útiles",
            value="• `!chat Explícame Python en 3 líneas`\n• `!chat Dame ideas para mi proyecto`\n• `!chat ¿Qué tiempo hace hoy?`",
            inline=False
        )
        return embed

    def _create_tools_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🔧 Herramientas y Scripts",
            description="Ejecutar acciones y servicios:",
            color=0xf39c12
        )
        embed.add_field(
            name="🛠️ Acciones externas",
            value="`/automate <servicio>`\n*Ejecuta flujos/webhooks configurados*",
            inline=False
        )
        embed.add_field(
            name="📜 Ejecutar local",
            value="`!exec <script>`\n*Ejecuta scripts o acciones locales (seguridad requerida)*",
            inline=False
        )
        embed.add_field(
            name="📋 Servicios disponibles",
            value="• deploy\n• backup\n• status\n• update_dependencies",
            inline=True
        )
        embed.add_field(
            name="📄 Scripts disponibles",
            value="• backup_data.py\n• update_system.py\n• cleanup_logs.py\n• health_check.py",
            inline=True
        )
        embed.set_footer(text="💡 Tip: Los comandos / tienen autocompletado")
        return embed

    def _create_help_embed(self) -> discord.Embed:
        # Reuse the shared help embed builder to avoid duplication
        return build_general_help_embed(command_db)

    def _create_status_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="📊 Estado del Bot",
            description="Información del sistema:",
            color=0x2ecc71
        )
        # Evitar errores si bot.user no está disponible
        bot_name = self.bot.user.name if self.bot.user else "Desconocido"
        bot_id = self.bot.user.id if self.bot.user else "N/A"
        prefix = getattr(self.bot, "command_prefix", "N/A")

        embed.add_field(
            name="🤖 Bot Info",
            value=f"**Nombre:** {bot_name}\n**ID:** {bot_id}\n**Prefix:** `{prefix}`",
            inline=True
        )
        embed.add_field(
            name="📈 Estadísticas",
            value=f"**Servidores:** {len(self.bot.guilds)}\n**Comandos cargados:** {len(self.bot.commands)}\n**Latencia:** {round(self.bot.latency * 1000)}ms",
            inline=True
        )
        embed.add_field(
            name="🔧 Servicios",
            value="**IA (Groq):** ✅ Activo\n**Música:** ✅ Disponible\n**Scripts:** ✅ Listos",
            inline=True
        )
        embed.add_field(
            name="💡 Comandos útiles",
            value="`!ping` - Verificar latencia\n`/menu` - Menú rápido\n`!status` - Estado de servicios",
            inline=False
        )
        return embed

async def setup(bot: commands.Bot):
    await bot.add_cog(QuickActions(bot))
