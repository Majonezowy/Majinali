import discord

class GifSelect(discord.ui.Select):
    def __init__(self, target_message: discord.Message):
        self.target_message = target_message 

        options = [ # value może miec max 100 znaków
            discord.SelectOption(label="Co ty pierdolisz", value="https://tenor.com/view/co-ty-pierdolisz-posluchaj-co-ty-pierdolisz-gif-26936388"),
            discord.SelectOption(label="That's just porn", value="https://tenor.com/bmJgyhB8fbj.gif"),
            discord.SelectOption(label="I'm gonna jerk off to that", value="https://tenor.com/bYBe2.gif")
        ]

        super().__init__(
            placeholder="Wybierz GIF...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await self.target_message.reply(self.values[0])
        except discord.errors.Forbidden:
            await interaction.response.send_message(f"{self.values[0]}")
            return
        await interaction.response.send_message(f"✅ GIF wysłany: {self.values[0]}", ephemeral=True)

class GifView(discord.ui.View):
    def __init__(self, target_message: discord.Message):
        super().__init__(timeout=300)
        self.add_item(GifSelect(target_message))