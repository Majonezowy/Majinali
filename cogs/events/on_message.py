import discord
from discord.ext import commands
import sqlite3

class LinkedChannels(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.conn = sqlite3.connect("bot_data.db")
        self.c = self.conn.cursor()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        message_id = message.channel.id

        self.c.execute("SELECT * FROM linked_text_channels WHERE channel_id_a = ? OR channel_id_b = ?", (message_id, message_id))
        linked_text_channels: list[tuple] = self.c.fetchall()

        for linked_channel in linked_text_channels:
            linked_channel = list(linked_channel)
            linked_channel.remove(message_id)

            channel: discord.abc.GuildChannel | discord.Thread | discord.abc.PrivateChannel | None = self.bot.get_channel(linked_channel[0])
            if not isinstance(channel, (discord.ForumChannel, discord.abc.PrivateChannel, discord.CategoryChannel)) and channel:
                await channel.send(f"<@{message.author.id}>: {message.content}")

async def setup(bot):
    await bot.add_cog(LinkedChannels(bot))