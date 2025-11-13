import asyncio
from typing import Optional, Dict, List
import discord
import yt_dlp


class Track:
    def __init__(self, info: dict):
        self.info = info
        self.title = info.get("title", "Audio")
        self.url = info.get("url")


class MusicManager:
    """Simple per-guild music queue manager."""

    def __init__(self):
        # guild_id -> queue(list[Track])
        self.queues: Dict[int, List[Track]] = {}
        # guild_id -> repeat flag
        self.repeat: Dict[int, bool] = {}

    def enqueue(self, guild_id: int, info: dict):
        self.queues.setdefault(guild_id, []).append(Track(info))

    def get_queue(self, guild_id: int) -> List[Track]:
        return self.queues.get(guild_id, [])

    def clear(self, guild_id: int):
        self.queues[guild_id] = []

    def set_repeat(self, guild_id: int, value: bool):
        self.repeat[guild_id] = value

    def toggle_repeat(self, guild_id: int) -> bool:
        cur = self.repeat.get(guild_id, False)
        self.repeat[guild_id] = not cur
        return self.repeat[guild_id]


_manager = MusicManager()


def get_manager() -> MusicManager:
    return _manager


async def ensure_voice_for_interaction(interaction: discord.Interaction) -> Optional[discord.VoiceClient]:
    """Ensure the bot is connected to the invoking user's voice channel.

    Returns the VoiceClient or None on failure (and sends an ephemeral message).
    """
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
        if voice_client.channel.id != channel.id:
            try:
                await voice_client.move_to(channel)
            except Exception:
                # ignore move errors
                pass

    return voice_client


async def extract_info(url: str) -> Optional[dict]:
    """Run yt_dlp extraction in a thread to avoid blocking the event loop."""
    loop = asyncio.get_running_loop()

    def _extract():
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    try:
        info = await loop.run_in_executor(None, _extract)
        return info
    except Exception:
        return None


def create_ffmpeg_source(audio_url: str) -> discord.FFmpegPCMAudio:
    ffmpeg_options = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }
    return discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
async def _play_source(voice_client: discord.VoiceClient, track: Track, guild_id: int):
    """Internal: play a track and register after callback to play next."""
    audio_url = track.url
    if not audio_url:
        return False

    source = create_ffmpeg_source(audio_url)

    # capture the running loop from the main thread so we can schedule coroutines from the audio thread
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # fallback to get_event_loop (older py versions); still OK to use for call_soon_threadsafe
        loop = asyncio.get_event_loop()

    def _after(err=None):
        # schedule next on the main event loop from the audio thread
        if err:
            loop.call_soon_threadsafe(print, f"Error in playback: {err}")
        # schedule coroutine creation safely
        loop.call_soon_threadsafe(asyncio.create_task, _play_next_if_available(voice_client, guild_id))

    try:
        # stop existing and play
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(source, after=_after)
        return True
    except Exception as e:
        print(f"Failed to play source: {e}")
        return False


async def _play_next_if_available(voice_client: discord.VoiceClient, guild_id: int):
    mgr = get_manager()
    queue = mgr.get_queue(guild_id)
    if not queue:
        return

    # If repeat is enabled, keep the current track at front
    track = queue.pop(0)
    if mgr.repeat.get(guild_id, False):
        # re-append a copy (keep playing loop)
        mgr.enqueue(guild_id, track.info)

    await _play_source(voice_client, track, guild_id)


async def play_next(voice_client: discord.VoiceClient, guild_id: int) -> Optional[str]:
    mgr = get_manager()
    queue = mgr.get_queue(guild_id)
    if not queue:
        return None
    track = queue.pop(0)
    success = await _play_source(voice_client, track, guild_id)
    return track.title if success else None


def skip_current(voice_client: discord.VoiceClient):
    try:
        if voice_client.is_playing():
            voice_client.stop()
    except Exception:
        pass


def stop_and_clear(voice_client: discord.VoiceClient, guild_id: int):
    try:
        if voice_client.is_playing():
            voice_client.stop()
    except Exception:
        pass
    get_manager().clear(guild_id)


def pause(voice_client: discord.VoiceClient):
    try:
        if voice_client.is_playing():
            voice_client.pause()
    except Exception:
        pass


def resume(voice_client: discord.VoiceClient):
    try:
        if voice_client.is_paused():
            voice_client.resume()
    except Exception:
        pass
