import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from typing import Optional, Any

def s_getattr( obj, attr, default = None ) -> Optional[Any]:
    return getattr(obj, attr, default)

def channelInfo(channel):
    return {
        "id": s_getattr(channel, "id"),
        "name": s_getattr(channel, "name"),
        "type": str(type(channel)),
        "category_id": s_getattr(channel, "category_id"),
        "position": s_getattr(channel, "position"),
        "nsfw": s_getattr(channel, "nsfw"),
        "guild": s_getattr(getattr(channel, "guild"), "id")
    }

def authorInfo(author):
    return {
        "id": author.id,
        "name": author.name,
        "nick": s_getattr(author, "nick"),
        "bot": author.bot,
        "guild": s_getattr(getattr(author, "guild"), "id")
    }

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
            "channel":     channelInfo(message.channel),
            "author":       authorInfo(message.author),
            "id":                      message.id,
            "pinned":                  message.pinned,
            "type":                    message.type.name,
            "content":                 message.content,
            "mention_everyone":        message.mention_everyone,
            "created_at":          str(message.created_at),
            "edited_at":           str(message.edited_at) if message.edited_at else None,
            "referenced_message":  str(message.reference) if message.reference else None,
            "flags":               int(message.flags.value) if message.flags else 0,
            "webhook_id":    s_getattr(message, "webhook_id"),
            "mentions":      [ user.id for user in message.mentions ],
            "mention_roles": [ role.id for role in message.role_mentions ],
            "embeds":        [ embed.to_dict() for embed in message.embeds ],
            "stickers":      [ sticker.name for sticker in message.stickers ],
            "attachments":   [ attachment.url for attachment in message.attachments ],
            "components":    [ component.to_dict() for component in message.components ],
            "reactions":     [ { "emoji": str(r.emoji), "count": r.count, "me": r.me } for r in message.reactions ]
        }

        await interaction.followup.send(f"```json\n{info}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageData(bot))
