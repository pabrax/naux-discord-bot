import discord
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.commands.quick_actions import QuickActions


class MenuView(discord.ui.View):
    def __init__(self, cog: 'QuickActions', author: discord.User, timeout: float = 30.0):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.author = author

        # Botones principales (emoji + label)
        self.add_item(MenuButton("🎵 Música", "music_menu"))
        self.add_item(MenuButton("🤖 Chat IA", "chat_menu"))
        self.add_item(MenuButton("🔧 Herramientas", "tools_menu"))
        self.add_item(MenuButton("❓ Ayuda", "help_menu"))
        self.add_item(MenuButton("📊 Estado", "status_menu"))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


class MenuButton(discord.ui.Button):
    def __init__(self, label: str, action: str):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.action = action

    async def callback(self, interaction: discord.Interaction):
        view: MenuView = self.view  # type: ignore
        cog = view.cog  # type: ignore

        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este menú. Solo quien lo invocó puede interactuar.", ephemeral=True)
            return

        await cog._handle_menu_action_interaction(interaction, self.action, view)


class BackCloseView(discord.ui.View):
    def __init__(self, cog: 'QuickActions', author: discord.User, timeout: float = 30.0):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.author = author

        self.add_item(BackButton())
        self.add_item(CloseButton())

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔙 Volver", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view: BackCloseView = self.view  # type: ignore
        cog = view.cog  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        await cog._show_main_menu(interaction)


class CloseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="❌ Cerrar", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        view: BackCloseView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        for child in view.children:
            child.disabled = True
        await interaction.response.edit_message(content="⏰ Menú cerrado", embed=None, view=view)


class MusicControlView(discord.ui.View):
    def __init__(self, bot: 'discord.Client', guild_id: int, author: discord.User, timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.guild_id = guild_id
        self.author = author

        self.add_item(PrevButton())
        self.add_item(PlayPauseButton())
        self.add_item(NextButton())
        self.add_item(RepeatButton())
        self.add_item(StopButton())

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


class PrevButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⏮️", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view: MusicControlView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este control.", ephemeral=True)
            return
        # For simplicity: skip to next (previous not implemented as we don't store history)
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message("No estoy en un canal de voz.", ephemeral=True)
            return
        from bot.utils.music_player import skip_current

        skip_current(vc)
        await interaction.response.send_message("⏭️ Saltando canción...", ephemeral=True)


class PlayPauseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⏯️", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view: MusicControlView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este control.", ephemeral=True)
            return
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message("No estoy en un canal de voz.", ephemeral=True)
            return
        from bot.utils.music_player import pause, resume

        if vc.is_playing():
            pause(vc)
            await interaction.response.send_message("⏸️ Pausado", ephemeral=True)
        elif vc.is_paused():
            resume(vc)
            await interaction.response.send_message("▶️ Reanudado", ephemeral=True)
        else:
            await interaction.response.send_message("No hay reproducción activa.", ephemeral=True)


class NextButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⏭️", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view: MusicControlView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este control.", ephemeral=True)
            return
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message("No estoy en un canal de voz.", ephemeral=True)
            return
        from bot.utils.music_player import skip_current

        skip_current(vc)
        await interaction.response.send_message("⏭️ Siguiente canción...")


class RepeatButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔁", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view: MusicControlView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este control.", ephemeral=True)
            return
        from bot.utils.music_player import get_manager

        new = get_manager().toggle_repeat(interaction.guild.id)
        await interaction.response.send_message(f"🔁 Repetición {'activada' if new else 'desactivada'}", ephemeral=True)


class StopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⏹️", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        view: MusicControlView = self.view  # type: ignore
        if interaction.user.id != view.author.id:
            await interaction.response.send_message("No puedes usar este control.", ephemeral=True)
            return
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message("No estoy en un canal de voz.", ephemeral=True)
            return
        from bot.utils.music_player import stop_and_clear

        stop_and_clear(vc, interaction.guild.id)
        await interaction.response.send_message("⏹️ Reproductor detenido y cola limpiada.", ephemeral=True)
