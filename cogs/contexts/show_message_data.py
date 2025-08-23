import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from typing import Optional

class MessageData(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(
            name="Get message data",
            callback=self.purger,
        )

        self.ctx_menu.allowed_contexts = app_commands.AppCommandContext(
            guild=True,
            dm_channel=True,
            private_channel=True
        )

        self.ctx_menu.allowed_installs = app_commands.AppInstallationType(
            guild=True,
            user=True
        )
        self.bot.tree.add_command(self.ctx_menu)

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def purger(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        info = {
            "id": message.id,
            "channel": {
                "id": getattr(message.channel, "id", None),
                "name": getattr(message.channel, "name", None),
                "type": str(type(message.channel)),
                "category_id": getattr(message.channel, "category_id", None),
                "position": getattr(message.channel, "position", None),
                "nsfw": getattr(message.channel, "nsfw", None),
                "guild": getattr(getattr(message.channel, "guild", None), "id", None)
            },
            "type": message.type.name,
            "author": {
                "id": message.author.id,
                "name": message.author.name,
                "nick": getattr(message.author, "nick", None),
                "bot": message.author.bot,
                "guild": getattr(getattr(message.author, "guild", None), "id", None)
            },
            "content": message.content,
            "embeds": [embed.to_dict() for embed in message.embeds],
            "attachments": [attachment.url for attachment in message.attachments],
            "stickers": [sticker.name for sticker in message.stickers],
            "flags": int(message.flags.value) if message.flags else None,
            "pinned": message.pinned,
            "mention_everyone": message.mention_everyone,
            "mentions": [user.id for user in message.mentions],
            "mention_roles": [role.id for role in message.role_mentions],
            "created_at": str(message.created_at),
            "edited_at": str(message.edited_at) if message.edited_at else None,
            "referenced_message": str(message.reference) if message.reference else None,
            "components": [component.to_dict() for component in message.components],
            "reactions": [
                {"emoji": str(reaction.emoji), "count": reaction.count, "me": reaction.me} 
                for reaction in message.reactions
            ],
            "webhook_id": getattr(message, "webhook_id", None)
        }

        await interaction.followup.send(f"```json\n{info}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageData(bot))
