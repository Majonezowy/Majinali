import discord
from discord.ext import commands
from discord import app_commands

from utility.lang_manager import LangManager
from utility import logger

import time
import asyncio

class MoveAll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="move_all", description="Przenosi wszystkich uzytkownikow na inny kanal.")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.checks.has_permissions(move_members=True)
    async def move_all(
        self, 
        interaction: discord.Interaction, 
        before: discord.VoiceChannel, 
        after: discord.VoiceChannel
    ):
        await interaction.response.defer(ephemeral=True)

        locale = str(interaction.locale).split("-")[0]

        if before == after:
            return await interaction.followup.send(
                self.langManager.t(locale, "moderation.voice.move_all.members_moved",
                                   before=before.name, after=after.name, time="0s")
            )

        vc_members = list(before.members or [])
        if not vc_members:
            return await interaction.followup.send(
                self.langManager.t(locale, "moderation.voice.move_all.no_members", before=before.name)
            )

        st = time.time()

        tasks = [member.move_to(after) for member in vc_members]

        await asyncio.gather(*tasks, return_exceptions=True)

        et = time.time()

        return await interaction.followup.send(
            self.langManager.t(locale, "moderation.voice.move_all.members_moved",
                               before=before.name, after=after.name, time=f"{(et - st):.2f}s")
        )
    @move_all.error
    async def move_all_on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await logger.handle_error(interaction, error, self.langManager)

async def setup(bot: commands.Bot):
    await bot.add_cog(MoveAll(bot))
