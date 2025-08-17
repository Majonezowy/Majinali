import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import sqlite3

class UnlinkChannels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn = sqlite3.connect("bot_data.db")
        self.c = self.conn.cursor()

    @app_commands.command(name="unlink_channels", description="Rozłącza kanał/y tekstowe ze sobą.")
    @app_commands.describe(
        local_channel="Channel on this guild",
        foreign_channel_id="Any channel id (optional)"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlink_channels(
        self,
        interaction: discord.Interaction,
        local_channel: discord.TextChannel,
        foreign_channel_id: Optional[str] = None
    ):
        local_channel_id = local_channel.id
        deleted = 0

        if foreign_channel_id:
            try:
                _foreign_channel_id = int(foreign_channel_id)
            except ValueError:
                await interaction.response.send_message("❌ Invalid foreign channel id!", ephemeral=True)
                return

            self.c.execute(
                "DELETE FROM linked_text_channels WHERE (channel_id_a=? AND channel_id_b=?) OR (channel_id_a=? AND channel_id_b=?)",
                (local_channel_id, _foreign_channel_id, _foreign_channel_id, local_channel_id)
            )
            deleted = self.c.rowcount
        else:
            self.c.execute(
                "DELETE FROM linked_text_channels WHERE channel_id_a=? OR channel_id_b=?",
                (local_channel_id, local_channel_id)
            )
            deleted = self.c.rowcount

        self.conn.commit()

        if deleted == 0:
            await interaction.response.send_message("⚠️ No link found to remove.", ephemeral=True)
        else:
            msg = f"✅ Successfully unlinked {local_channel.mention}"
            if foreign_channel_id:
                msg += f" and <#{_foreign_channel_id}>"
            await interaction.response.send_message(msg, ephemeral=True)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(UnlinkChannels(bot))
