import discord
from discord import ui

from utils.lang_manager import LangManager

class PlayingNowView(discord.ui.LayoutView):
    def __init__(self, img: str, title: str, duration: str, local_lang: str, langmanager: LangManager):
        super().__init__(timeout=None)
        self.lang: LangManager = langmanager
        
        thumbnail = ui.Thumbnail(media=img)
        
        view_title = ui.TextDisplay(self.lang.t(
                local_lang,
                "music.playing_now"
            )
        )
        
        track_title = ui.TextDisplay(self.lang.t(
                local_lang,
                "music.playing_now_title",
                title=title,
                duration=duration
            )
        )
        self.add_item(
            ui.Container(
                ui.Section(view_title, track_title, accessory=thumbnail)
            )
        )