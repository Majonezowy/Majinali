import discord
from discord import app_commands
from discord.ext import commands

class ForwardMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(
            name="Forward message content",
            callback=self.forward_message
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def forward_message(self, interaction: discord.Interaction, message: discord.Message):
        content = message.content
        if isinstance(interaction.channel, discord.ForumChannel):
            await interaction.response.send_message("Cannot forward messages in a forum channel.", ephemeral=True)
            return
        await interaction.channel.send( # type: ignore
            f"📩 Forwarded message from {message.author}:\n{content}"
        ) 
        await interaction.response.send_message("✅ Message forwarded!", ephemeral=True) 


async def setup(bot: commands.Bot):
    await bot.add_cog(ForwardMessage(bot))
