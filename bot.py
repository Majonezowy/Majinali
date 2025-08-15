import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from setup_db import setup_database

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def setup_hook():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("__"):
            print(f"\033[34mLoading command: {filename[:-3]}")
            await bot.load_extension(f"commands.{filename[:-3]}")
    
    for filename in os.listdir("./events"):
        if filename.endswith(".py") and not filename.startswith("__"):
            print(f"\033[33mLoading event: {filename[:-3]}")
            await bot.load_extension(f"events.{filename[:-3]}")
    
    for filename in os.listdir("./context"):
        if filename.endswith(".py") and not filename.startswith("__"):
            print(f"\033[36mLoading context: {filename[:-3]}")
            await bot.load_extension(f"context.{filename[:-3]}")

    print("\033[32mAll cogs loaded successfully.\033[0m")

@bot.tree.context_menu(name="Forward message content2")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
@app_commands.allowed_installs(guilds=False, users=True)
async def forward_message2(interaction: discord.Interaction, target: discord.Message):
    await interaction.response.send_message("✅ Message forwarded!", ephemeral=True)

@bot.event
async def on_ready():
    assert bot.user is not None, "Bot user is not set."
    await bot.tree.sync()
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
    bot.run(TOKEN)