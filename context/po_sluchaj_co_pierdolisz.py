import discord
from discord import app_commands
from discord.ext import commands

class PierdolenieGif(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Global context menu
        self.ctx_menu = app_commands.ContextMenu(
            name="Posłuchaj co pierdolisz",
            callback=self.forward_message
        )
        self.bot.tree.add_command(self.ctx_menu)  # no guild specified → global
        

    async def forward_message(self, interaction: discord.Interaction, message: discord.Message):
        

        # Send the GIF
        # Use followup in case interaction.channel.send fails
        await interaction.response.send_message(
            "✅ GIF forwarded!", ephemeral=True
        )
        await interaction.followup.send(
            "https://tenor.com/view/co-ty-pierdolisz-posluchaj-co-ty-pierdolisz-gif-26936388"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(PierdolenieGif(bot))
