from discord.ext import commands
import discord

VOICE_CHANNEL_ID = 834685357207453706
CATEGORY_ID = 769973785184305181

class ModularVoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.own_channels: dict[discord.Member, int] = self.bot.own_channels

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is not None and self.own_channels.get(member, None) is not None:
            vc: discord.VoiceChannel = self.bot.get_channel(self.own_channels.get(member, None))

            self.own_channels.pop(member)
            await vc.delete()

        if after.channel is None:
            return

        guild = member.guild
        category = discord.utils.get(guild.categories, id=CATEGORY_ID)
        overwrites = {
            member: discord.PermissionOverwrite(manage_channels=True, connect=True, mute_members=True, move_members=True)
        }

        if after.channel.id == VOICE_CHANNEL_ID:
            vc = await guild.create_voice_channel(
                name=f"Kanał {member.display_name}",
                category=category,
                overwrites=overwrites # type: ignore
            )
            await member.move_to(vc)
            self.own_channels.update({member: vc.id})
async def setup(bot):
    await bot.add_cog(ModularVoiceChannels(bot))
