import discord
from discord.ext import commands
from discord import app_commands
from utils.db.db import DatabaseClient

class TestDb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: DatabaseClient = bot.db

    @app_commands.command(name="test_db", description="Testuje połączenie do bazy danych")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def test_db(self, interaction: discord.Interaction):
        result = await self.db.fetchone("SELECT name FROM sqlite_master WHERE type='table';")
        await interaction.response.send_message(str(result))
    
async def setup(bot):
    await bot.add_cog(TestDb(bot))
