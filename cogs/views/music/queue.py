import discord
from discord import ui

from utility.lang_manager import LangManager

class QueueView(discord.ui.LayoutView):
    def __init__(self, tracks, local_lang: str, langmanager: LangManager):
        super().__init__(timeout=None)
        self.lang: LangManager = langmanager
        
        title = ui.TextDisplay(self.lang.t(
                local_lang,
                "music.queue_title",
            )
        )
        
        container = ui.Container()
        container.add_item(title)

        if isinstance(tracks, str):
            container.add_item(ui.TextDisplay(tracks))
            self.add_item(container)
            return
        
        for i, track in enumerate(tracks):
            element = ui.TextDisplay(f"{i}. {track}")
            container.add_item(element)
            
        self.add_item(container)