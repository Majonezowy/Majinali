import discord
from discord import app_commands, Colour
from discord.ext import commands
from typing import Optional

class Embed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="create_embed", description="Creates an embed.")
    @app_commands.describe(
        title="The title of the embed",
        description="The description of the embed",
        color="The color of the embed in HEX (e.g., #ff0000)",
        url="Optional URL for the embed"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.allowed_installs(guilds=False, users=True)
    async def create_embed(
        self, 
        interaction: discord.Interaction,
        title: Optional[str] = "",
        description: Optional[str] = "",
        color: Optional[str] = "#ffffff",
        url: Optional[str] = ""
    ):
        try:
            color = discord.Colour(int(color.lstrip('#'), 16)) # type: ignore
        except ValueError:
            await interaction.response.send_message("Invalid color format. Please use HEX format (e.g., #ff0000).", ephemeral=True)
            return
        
        if url and not url.startswith("http"):
            url = f"http://{url}"

        embed = discord.Embed(title=title, description=description, color=color, url=url) # type: ignore
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Embed(bot))
