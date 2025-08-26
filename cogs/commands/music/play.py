import discord
from discord.ext import commands
from discord import app_commands
from utils.music import MusicManager
import asyncio

from cogs.views.music.added_to_queue import AddedQueueView
from cogs.views.music.playing_now import PlayingNowView

class PlayMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore
        self.langManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="play", description="Odtwórz muzykę z linku (YouTube/SoundCloud)")
    @app_commands.describe(query="Nazwa lub URL piosenki")
    @app_commands.checks.cooldown(rate=1, per=6.75)
    async def play_music(self, interaction: discord.Interaction, query: str):
        guild = interaction.guild
        member = interaction.user
        locale = str(interaction.locale).split("-")[0]
        
        if guild is None:
            return

        member = guild.get_member(member.id)
        
        if not member or not member.voice or not member.voice.channel:
            return await interaction.response.send_message(
                self.langManager.t(locale, "music.not_in_voice"), ephemeral=True
            )

        await interaction.response.defer()

        vc = guild.voice_client
        
        if not vc:
            vc = await member.voice.channel.connect()
        else:
            await vc.move_to(member.voice.channel) # type: ignore

        if not query.startswith("http"):
            query_info = self.musicManager.fetch_video_url(query)
            if query_info:
                query = query_info
            else:
                await interaction.followup.send("Nie znalazlem niczego co pasuje do zapytania", ephemeral=True)
        
        self.musicManager.add_to_queue(guild.id, query)
        asyncio.create_task(self.musicManager.play_next(vc, guild.id)) # type: ignore
        queue_len = len(self.musicManager.queue.get(guild.id, []))
            
        metadata = await self.musicManager.fetch_metadata(query)
        query = metadata['title'] # type: ignore
        img = metadata.get("thumbnail", interaction.user.display_avatar.url)
        duration = metadata['duration']
        
        if not vc.is_playing() and queue_len == 1: # type: ignore
            view = PlayingNowView(
                img=img, # type: ignore
                title=query,
                duration=duration, # type: ignore
                local_lang=locale,
                langmanager=self.langManager
            )
            await interaction.followup.send(view=view)
        else:
            view = AddedQueueView(
                img=img, # type: ignore
                index=queue_len,
                title=query,
                duration=duration, # type: ignore
                local_lang=locale,
                langmanager=self.langManager
            )
            await interaction.followup.send(view=view)

    @play_music.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.errors.ConnectionClosed):
            return
        elif isinstance(error, app_commands.CommandOnCooldown):
            if interaction.response.is_done():
                await interaction.followup.send(str(error), ephemeral=True)
            else:
                await interaction.response.send_message(str(error), ephemeral=True)
        else:
            await interaction.followup.send(str(error))

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayMusic(bot))
