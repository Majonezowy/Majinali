import discord
from discord.ext import commands
from discord import app_commands
from collections import deque

from bs4 import BeautifulSoup
import aiohttp
import asyncio

from utils.music import MusicManager
from utils.lang_manager import LangManager
from utils import logger

class Soundboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="soundboard", description="Odtwarza dźwięk z myinstants")
    async def soundboard(self, interaction: discord.Interaction, url: str):
        member = interaction.user
        guild = interaction.guild
        locale = str(interaction.locale).split("-")[0]
        
        if not url.startswith("http"):
            return await interaction.response.send_message(self.langManager.t(locale, "soundboard.invalid_url"), ephemeral=True)
                
        if guild is None:
            return
        
        member = guild.get_member(member.id)
        
        if not member or not member.voice or not member.voice.channel:
            return await interaction.response.send_message(
                self.langManager.t(locale, "music.not_in_voice"), ephemeral=True
            )
        
        await interaction.response.defer(ephemeral=True)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:                                                     # type: ignore
                html = await resp.text(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                
                button = soup.find("button", attrs={"data-url": True})
                if not button:
                    return await interaction.followup.send(self.langManager.t(locale, "soundboard.sound_not_found"), ephemeral=True)

                sound_url = button.get("data-url", None) # type: ignore
                
                if not sound_url:
                    return await interaction.followup.send(self.langManager.t(locale, "soundboard.sound_not_found"), ephemeral=True)

                sound_url = f"https://www.myinstants.com/{sound_url}"
                
                vc = guild.voice_client
                
                if not vc:
                    vc = await member.voice.channel.connect()
                else:
                    await vc.move_to(member.voice.channel) # type: ignore
                
                if guild.id not in self.musicManager.queue:
                    self.musicManager.queue[guild.id] = deque()

                queue = self.musicManager.queue[guild.id]

                if len(queue) > 0:
                    queue.insert(1, sound_url)
                    
                    current_track = queue[0]
                    queue.insert(2, current_track)
                else:
                    queue.append(sound_url)

                if not vc.is_playing(): # type: ignore
                    asyncio.create_task(self.musicManager.play_next(vc, guild.id))  # type: ignore
                else:
                    await self.musicManager.skip_current(vc, guild.id) # type: ignore
                
                return await interaction.followup.send(self.langManager.t(locale, "soundboard.playing", url=url), ephemeral=True)

    @soundboard.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await logger.handle_error(interaction, error, self.langManager)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Soundboard(bot))
