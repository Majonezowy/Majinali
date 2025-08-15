import discord

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="A Green Button",
            custom_id="help_green_button"
        ))

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        label="Another Button",
        custom_id="help_blue_button"
    )
    async def another_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the blue button!", ephemeral=True)
