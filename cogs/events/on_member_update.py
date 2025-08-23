from discord.ext import commands
import discord

class BotNicknameChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.id == self.bot.user.id:
            return
        
        before.name

        if before.nick != after.nick:
            old_nick = before.nick
            try:
                await after.edit(nick=old_nick)
            except discord.Forbidden:
                return
            except discord.HTTPException:
                return

async def setup(bot):
    await bot.add_cog(BotNicknameChange(bot))
