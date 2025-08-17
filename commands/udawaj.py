import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./../.env")

dev_id = os.getenv("dev_id")
if not dev_id:
    raise ValueError("dev_id environment variable not set.")


class Udawaj(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="udawaj", description="Udawaj innego użytkownika.")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    async def udawaj(self, interaction: discord.Interaction, member: discord.Member, message: str = ""):
        if member is None:
            await interaction.response.send_message("❌ Nie podano użytkownika", ephemeral=True)
            return

        if not message:
            await interaction.response.send_message("❌ Nie podano wiadomosci", ephemeral=True)
            return

        channel = interaction.channel
        if isinstance(channel, discord.TextChannel):
            webhook = await channel.create_webhook(name=f"{member.name}")
            await webhook.send(
                content=message,
                username=member.display_name,
                avatar_url=member.display_avatar.url
            )

            await interaction.response.send_message("✅ Wiadomość wysłana przez webhooka!", ephemeral=True)
            await webhook.delete(reason="Automated webhook deletion")
        else:
            await interaction.response.send_message("❌ Ten kanał nie obsługuje webhooków", ephemeral=True)

    @udawaj.error
    async def udawaj_on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("Nastąpił błąd przy wykonywaniu komeny!" + f" {str(error)}" if interaction.user.id == dev_id else "", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Udawaj(bot))

