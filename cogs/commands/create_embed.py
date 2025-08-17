import discord
from discord import app_commands, Colour
from discord.ext import commands
from typing import Optional
import re

def is_valid_url(link: str | None = None) -> bool:
    if link is None:
        return False
    return re.match(r"^https?:\/\/[^\s]+$", link) is not None

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
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.checks.cooldown(1, 5.0)
    async def create_embed(
        self, 
        interaction: discord.Interaction,
        title: Optional[str] = "",
        description: Optional[str] = "",
        thumbnail: Optional[str] = "",
        author: Optional[str] = "",
        author_icon: Optional[str] = "",
        footer: Optional[str] = "",
        footer_icon: Optional[str] = "",
        color: Optional[str] = "#ffffff",
        url: Optional[str] = ""
    ):
        try:
            color = discord.Colour(int(color.lstrip('#'), 16)) # type: ignore
        except ValueError:
            await interaction.response.send_message("Invalid color format. Please use HEX format (e.g., #ff0000).", ephemeral=True)
            return
        
        if url:
            if not is_valid_url(url):
                await interaction.response.send_message("Invalid url format.")
            if not url.startswith("http"):
                url = f"http://{url}"


        embed = discord.Embed(title=title, description=description, color=color, url=url) # type: ignore
        if is_valid_url(thumbnail):
            embed.set_thumbnail(url=thumbnail)

        if author:
            if is_valid_url(author_icon):
                embed.set_author(name=author, icon_url=author_icon)
            else:
                embed.set_author(name=author)

        if footer:
            if is_valid_url(footer_icon):
                embed.set_footer(text=footer, icon_url=footer_icon)
            else:
                embed.set_footer(text=footer)
        await interaction.response.send_message(embed=embed)

    @create_embed.error
    async def on_create_embed_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error))

async def setup(bot: commands.Bot):
    await bot.add_cog(Embed(bot))
