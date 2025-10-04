import discord 
from discord.ext import commands
import yt_dlp
import asyncio

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
        voice_client = ctx.voice_client
        
        if not voice_client:
            await ctx.send("El bot no está conectado a un canal de voz.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True
        }
        
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
                title = info.get('title', 'Audio')

            source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
            voice_client.play(source)
            await ctx.send(f"Reproduciendo: {title}")
            
        except Exception as e:
            await ctx.send(f"Error al reproducir audio: {str(e)}")

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