import discord
from discord import ui
from cogs.views.ticket_category_select_view import TicketCategoryView

class HelpView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        button = discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="Stworz ticket",
            custom_id="create_ticket_button"
        )
        button.callback = self.create_ticket_button_callback
        textinput = ui.TextDisplay("# Wybierz kategorie")
        self.add_item(ui.Container(button))

    async def create_ticket_button_callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Wybierz kategorię:")
        await interaction.response.send_message(embed=embed, view=TicketCategoryView(), ephemeral=True)
