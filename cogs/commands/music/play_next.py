import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from utility.music import MusicManager
from utility.lang_manager import LangManager
from utility import logger

class SkipMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager # type: ignore
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="skip", description="Pomija obecną piosenkę")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
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

        vc: discord.VoiceClient = guild.voice_client # type: ignore
        
        if not vc:
            return await interaction.response.send_message(
                self.langManager.t(locale, "music.bot_not_in_voice"), ephemeral=True
            )

        asyncio.create_task(self._skip_logic(vc, guild.id, interaction))

    async def _skip_logic(self, vc: discord.VoiceClient, guild_id: int, interaction: discord.Interaction):
        await self.musicManager.skip_current(vc, guild_id)
        locale = str(interaction.locale).split("-")[0]
        
        await asyncio.sleep(0.1)

        queue = self.musicManager.queue.get(guild_id, [])
        next_title = None
        
        if queue and len(queue) > 0:
            next_title = queue[0]
            if next_title.startswith("http"):
                metadata = await self.musicManager.fetch_metadata(next_title)
            title = metadata['title']
            next_title = title
            
            await interaction.followup.send(self.langManager.t(locale, "music.track_skipped", next_title=next_title))
        else:
            await interaction.followup.send(self.langManager.t(locale, "music.track_skipped_end"))
            await vc.disconnect()
            
    @skip.error
    async def on_skip_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await logger.handle_error(interaction, error, self.langManager)

async def setup(bot: commands.Bot):
    await bot.add_cog(SkipMusic(bot))
