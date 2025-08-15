import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from typing import Optional

class PurgeUntil(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(
            name="Purge until this message",
            callback=self.purger,
        )

        self.ctx_menu.allowed_contexts = app_commands.AppCommandContext(
            guild=True,
            dm_channel=False,
            private_channel=False
        )

        self.ctx_menu.allowed_installs = app_commands.AppInstallationType(
            guild=True,
            user=False
        )
        self.bot.tree.add_command(self.ctx_menu)

    @app_commands.checks.has_permissions(manage_messages=True)
    async def purger(self, interaction: discord.Interaction, message: discord.Message):
        channel = message.channel
        TARGET_ID = message.id

        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                "🚫 You can only purge messages in guild text channels.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        last_id = None
        total_deleted = 0

        while True:
            history = channel.history(limit=100, before=discord.Object(id=last_id) if last_id else None)
            messages = [msg async for msg in history]

            if not messages:
                break

            if any(msg.id <= TARGET_ID for msg in messages):
                messages_to_delete = [msg for msg in messages if msg.id > TARGET_ID]
            else:
                messages_to_delete = messages

            try:
                await channel.delete_messages(messages_to_delete)
                total_deleted += len(messages_to_delete)
            except discord.HTTPException:
                for msg in messages_to_delete:
                    try:
                        await msg.delete()
                        total_deleted += 1
                        await asyncio.sleep(1)
                    except Exception:
                        pass

            if any(msg.id <= TARGET_ID for msg in messages):
                break

            last_id = messages[-1].id

        await interaction.followup.send(f"✅ Purged {total_deleted} messages.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PurgeUntil(bot))
