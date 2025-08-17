import json

class LangManager:
    def __init__(self):
        self.cache = {}

    def load(self, lang: str):
        if lang not in self.cache:
            with open(f"../lang/{lang}.json", "r", encoding="utf-8") as f:
                self.cache[lang] = json.load(f)
        return self.cache[lang]

    def t(self, lang: str, key: str, **kwargs):
        return self.load(lang).get(key, key).format(**kwargs)
