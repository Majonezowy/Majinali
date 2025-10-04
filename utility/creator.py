import discord

class ModalCreator(discord.ui.Modal):
    def __init__(self, data: dict) -> None:
        super().__init__(title=data.get("title", ""))
        
        for ti in data.keys():
            arg = data[ti]
            if not isinstance(arg, dict): continue
            try:
                self.add_item(discord.ui.TextInput(
                    label        = arg.get("label", ""),
                    placeholder  = arg.get("placeholder", ""),
                    style        = arg.get("style", discord.TextStyle.short),
                    required     = arg.get("required", False),
                    min_length   = arg.get("min_length", 1),
                    max_length   = arg.get("max_length", 4000),
                    default      = arg.get("default", ""),
                    row          = arg.get("row"),
                ))
            except Exception:
                continue


    