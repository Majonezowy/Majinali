import discord
from discord.ext import commands
from collections import deque

class MusicManager:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.queue: dict[int, deque] = self.bot.queue  # type: ignore

    def add_to_queue(self, guild_id: int, stream_url: str):
        if guild_id not in self.queue:
            self.queue[guild_id] = deque()
        self.queue[guild_id].append(stream_url)

    def get_next_from_queue(self, guild_id: int):
        if guild_id in self.queue and self.queue[guild_id]:
            return self.queue[guild_id].popleft()
        return None

    async def play_next(self, vc: discord.VoiceClient, guild_id: int):
        next_song = self.get_next_from_queue(guild_id)
        if next_song:
            source = discord.FFmpegPCMAudio(source=next_song, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",options="-vn")
            vc.play(
                source,
                after=lambda e: self.bot.loop.create_task(self.play_next(vc, guild_id))
            )
        else:
            await vc.disconnect()

    def stop(self, vc: discord.VoiceClient, guild_id: int):
        if guild_id in self.queue:
            self.queue[guild_id].clear()
        if vc.is_playing():
            vc.stop()
