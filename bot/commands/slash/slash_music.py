import asyncio
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import yt_dlp
from bot.utils.music_player import ensure_voice_for_interaction, extract_info
from bot.utils.music_player import get_manager, play_next
from bot.utils.ui_helpers import MusicControlView


class SlashMusic(commands.Cog):
    """Comandos de música en slash. /play conecta automáticamente al canal de voz del invocador."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _ensure_voice(self, interaction: discord.Interaction) -> Optional[discord.VoiceClient]:
        member = interaction.user
        if not isinstance(member, discord.Member) or not member.voice or not member.voice.channel:
            await interaction.followup.send("Debes estar en un canal de voz para usar este comando.", ephemeral=True)
            return None

        channel = member.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            try:
                voice_client = await channel.connect()
            except Exception as e:
                await interaction.followup.send(f"No pude conectar al canal de voz: {e}", ephemeral=True)
                return None
        else:
            # si está en otro canal, moverlo
            if voice_client.channel.id != channel.id:
                try:
                    await voice_client.move_to(channel)
                except Exception:
                    pass

        return voice_client

    async def _extract_audio_url(self, url: str) -> Optional[dict]:
        # Ejecutar la extracción de yt_dlp en un hilo para no bloquear el event loop
        loop = asyncio.get_running_loop()

        def extract():
            ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info

        try:
            info = await loop.run_in_executor(None, extract)
            return info
        except Exception:
            return None

    @app_commands.command(name="play", description="Reproducir audio; se conecta automáticamente al canal de voz")
    @app_commands.describe(url="URL o término a reproducir (youtube, stream)")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True)

        # Obtener o conectar al VC usando helpers centralizados
        voice_client = await ensure_voice_for_interaction(interaction)
        if not voice_client:
            return

        info = await extract_info(url)
        if not info:
            await interaction.followup.send("No pude extraer información del audio. Revisa la URL.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        # enqueue track
        get_manager().enqueue(guild_id, info)
        # Debug: log the resolved direct audio URL (useful to test ffmpeg/streaming)
        try:
            print(f"[music] Enqueued: {info.get('title')} | audio_url: {info.get('url')}")
        except Exception:
            pass

        # If nothing is playing, start playback
        if not interaction.guild.voice_client.is_playing() and not interaction.guild.voice_client.is_paused():
            title = await play_next(voice_client, guild_id)
            if title:
                view = MusicControlView(self.bot, guild_id, interaction.user)
                await interaction.followup.send(f"▶️ Reproduciendo: {title}", view=view)
                return
        # otherwise simply acknowledge queued
        await interaction.followup.send(f"➕ Encolado: {info.get('title','Audio')}", ephemeral=True)

    @app_commands.command(name="disconnect", description="Desconectar al bot del canal de voz")
    async def disconnect(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.response.send_message("Desconectado.")
        else:
            await interaction.response.send_message("No estoy conectado a ningún canal de voz.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SlashMusic(bot))
