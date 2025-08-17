import discord
from discord import ui
from string import ascii_letters
from random import sample

class Test(discord.ui.Modal, title="Test"):
    def __init__(self, selected_category):
        super().__init__()
        self.selected_category = selected_category

    description = ui.TextInput(label="Opis problemu", placeholder="Nie działa ...", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("This command cannot be used in DMs.", ephemeral=True)
            return
        guild: discord.Guild = interaction.guild

        rand_str = "".join(sample(ascii_letters, 5))
        channel_name = f"Ticket-{self.selected_category}-{rand_str}"
        channel = await guild.create_text_channel(
            channel_name,
            overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=True)}
        )

        await channel.send(f"Kategoria: **{self.selected_category}**\nOpis problemu: **{self.description}**")
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)