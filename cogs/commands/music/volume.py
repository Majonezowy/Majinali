import discord
from discord.ext import commands
from discord import app_commands
from utils.music import MusicManager

class SetVolume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore

    @app_commands.command(name="volume", description="Ustawia głośność od 0 do 100")
    async def volume(self, interaction: discord.Interaction, value: int):
        if value < 0 or value > 100:
          return await interaction.response.send_message("❌ Głośność musi być 0–100.", ephemeral=True)
        
        guild = interaction.guild
        vc = guild.voice_client # type: ignore
        if vc and vc.is_playing(): # type: ignore
            self.musicManager.set_volume(value, vc=vc) # type: ignore
        else:
            self.musicManager.set_volume(value)

        await interaction.response.send_message(f"🔊 Ustawiono głośność na {value}%", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SetVolume(bot))
