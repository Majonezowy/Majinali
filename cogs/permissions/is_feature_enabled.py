import discord
from discord import app_commands

guild_settings: dict[int, dict[str, bool]] = {
    1388501467626868808: {
        "music": True
    }
}

class FeatureDisabled(app_commands.CheckFailure):
    pass

def is_feature_enabled(feature_name: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            raise FeatureDisabled("Guild-only command")

        guild_id = interaction.guild_id or 0
        guild_config = guild_settings.get(guild_id, {})
        is_enabled = guild_config.get(feature_name, False)

        if not is_enabled:
            embed = discord.Embed(
                title="Feature Disabled",
                description=f"The feature `{feature_name}` is disabled on this server.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            raise FeatureDisabled(f"Feature `{feature_name}` is disabled.")

        return True

    return app_commands.check(predicate)
