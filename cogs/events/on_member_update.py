from discord.ext import commands
import discord

class BotNicknameChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.id == self.bot.user.id:
            return

        if before.nick != after.nick and after.nick is not None:
            try:
                await after.edit(nick=None)
            except discord.Forbidden:
                return
            except discord.HTTPException:
                return

async def setup(bot):
    await bot.add_cog(BotNicknameChange(bot))
