import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class LinkChannels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn = sqlite3.connect("bot_data.db")
        self.c = self.conn.cursor()

    @app_commands.command(name="link_channels", description="Łączy kanały tekstowe ze sobą.")
    @app_commands.describe(
        local_channel="Channel on this guild",
        foreign_channel_id="Any channel id"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.checks.has_permissions(manage_channels=True)
    async def link_channels(
        self,
        interaction: discord.Interaction,
        local_channel: discord.TextChannel,
        foreign_channel_id: str
    ):
        try:
            _foreign_channel_id = int(foreign_channel_id)
        except ValueError:
            await interaction.response.send_message("❌ Invalid foreign channel id!", ephemeral=True)
            return

        local_channel_id = local_channel.id

        foreign_channel = self.bot.get_channel(_foreign_channel_id)
        if not foreign_channel:
            await interaction.response.send_message("❌ Couldn't find foreign channel! (Am I in that guild?)", ephemeral=True)
            return

        if isinstance(foreign_channel, (discord.ForumChannel, discord.abc.PrivateChannel, discord.CategoryChannel)):
            await interaction.response.send_message("❌ Unsupported type for foreign channel", ephemeral=True)
            return

        if not foreign_channel.permissions_for(foreign_channel.guild.me).send_messages:
            await interaction.response.send_message("❌ I don’t have permission to send messages in the foreign channel!", ephemeral=True)
            return

        member = foreign_channel.guild.get_member(interaction.user.id)
        if not member or not member.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You must have Manage Channels permission in the foreign channel’s guild.", ephemeral=True)
            return

        a, b = sorted([local_channel_id, _foreign_channel_id])

        existing = self.c.execute(
            "SELECT 1 FROM linked_text_channels WHERE channel_id_a=? AND channel_id_b=?",
            (a, b)
        ).fetchone()
        if existing:
            await interaction.response.send_message("⚠️ These channels are already linked.", ephemeral=True)
            return

        self.c.execute("INSERT INTO linked_text_channels(channel_id_a, channel_id_b) VALUES (?, ?)", (a, b))
        self.conn.commit()

        await interaction.response.send_message(f"✅ Successfully linked {local_channel.mention} with {foreign_channel.mention}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LinkChannels(bot))
