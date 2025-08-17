import discord
from cogs.modals.test import Test

class TicketCategorySelect(discord.ui.Select):
    def __init__(self):

        options = [ # value może miec max 100 znaków
            discord.SelectOption(label="Discord", value="discord"),
            discord.SelectOption(label="Youtube", value="yotube"),
            discord.SelectOption(label="Minecraft", value="minecraft")
        ]

        super().__init__(
            placeholder="Wybierz kategorie",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Test(self.values[0]))

class TicketCategoryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketCategorySelect())