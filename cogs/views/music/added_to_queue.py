import discord
from discord import ui

from utils.lang_manager import LangManager

class AddedQueueView(discord.ui.LayoutView):
    def __init__(self, img: str, index: int, title: str, duration: str, local_lang: str, langmanager: LangManager):
        super().__init__(timeout=None)
        self.lang: LangManager = langmanager
        
        thumbnail = ui.Thumbnail(media=img)
        
        added_to_queue = ui.TextDisplay(self.lang.t(
                local_lang,
                "music.added_to_queue",
                index=index,
                duration=duration
            )
        )
        track_title = ui.TextDisplay(self.lang.t(
                local_lang,
                "music.added_to_queue_title",
                title=title
            )
        )
        self.add_item(ui.Container(ui.Section(added_to_queue, track_title, accessory=thumbnail)))