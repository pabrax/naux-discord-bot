import discord 
from discord.ext import commands
import yt_dlp
from bot.utils.music_player import extract_info, get_manager, play_next
from bot.utils.ui_helpers import MusicControlView

class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
            await ctx.send(f"Conectado a {channel.name}")
        else:
            await ctx.send("Debes estar en un canal de voz para usar este comando.")

    @commands.command()
    async def play(self, ctx, *, url):
        # Auto-conectar al canal de voz del autor si es necesario
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("Debes estar en un canal de voz para usar este comando.")
            return

        voice_client = ctx.voice_client
        if not voice_client:
            try:
                voice_client = await ctx.author.voice.channel.connect()
            except Exception as e:
                await ctx.send(f"No pude conectar al canal de voz: {e}")
                return

        info = await extract_info(url)
        if not info:
            await ctx.send("No pude extraer información del audio. Revisa la URL.")
            return

        guild_id = ctx.guild.id
        get_manager().enqueue(guild_id, info)
        try:
            print(f"[music] Enqueued: {info.get('title')} | audio_url: {info.get('url')}")
        except Exception:
            pass

        # If nothing is playing, start playback
        vc = ctx.guild.voice_client
        if not vc.is_playing() and not vc.is_paused():
            title = await play_next(vc, guild_id)
            if title:
                view = MusicControlView(self.bot, guild_id, ctx.author)
                await ctx.send(f"▶️ Reproduciendo: {title}", view=view)
                return

        await ctx.send(f"➕ Encolado: {info.get('title','Audio')}")

    @commands.command()
    async def disconnect(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("Desconectado del canal de voz.")
        else:
            await ctx.send("El bot no está conectado a un canal de voz.")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Reproducción detenida.")
        else:
            await ctx.send("No hay audio reproduciéndose actualmente.")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Reproducción reanudada.")
        else:
            await ctx.send("No hay audio pausado para reanudar.")
    
    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Reproducción pausada.")
        else:
            await ctx.send("No hay audio reproduciéndose actualmente.")

async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))