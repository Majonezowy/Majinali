import discord
from discord.ext import commands
import sqlite3

class ReactionRoleAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("bot_data.db")
        self.c = self.conn.cursor()
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        message_id = payload.message_id
        channel = payload.channel_id
        guild = payload.guild_id
        emoji = str(payload.emoji)
        user = payload.user_id

        self.c.execute("""
        SELECT role_id FROM reaction_roles WHERE guild_id = ? AND channel_id = ? AND message_id = ? AND emoji = ?
                       """, (guild, channel, message_id, emoji))
        result = self.c.fetchone()

        if not result:
            return
        
        role_id = result[0]
        guild = self.bot.get_guild(guild)

        if guild is None:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            return
        
        member = guild.get_member(user)
        if member is None:
            return
        
        await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoleAdd(bot))