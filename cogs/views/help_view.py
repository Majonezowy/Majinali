import discord
from views.ticket_category_select_view import TicketCategoryView

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        button = discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="Stworz ticket",
            custom_id="create_ticket_button"
        )
        button.callback = self.create_ticket_button_callback
        self.add_item(button)

    async def create_ticket_button_callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Wybierz kategorię:")
        await interaction.response.send_message(embed=embed, view=TicketCategoryView(), ephemeral=True)
