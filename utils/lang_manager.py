import os
import json
from collections import defaultdict

class LangManager:
    def __init__(self, base_path: str = None, default_lang: str = "en"):
        self.cache: dict[str, dict[str, str]] = {}
        self.default_lang = default_lang
        self.base_path = base_path or os.path.join(os.path.dirname(__file__), "..", "lang")

    def load(self, lang: str) -> dict[str, str]:
        if lang not in self.cache:
            path = os.path.join(self.base_path, f"{lang}.json")
            if not os.path.exists(path):
                if lang != self.default_lang:
                    return self.load(self.default_lang)
                return {}
            with open(path, "r", encoding="utf-8") as f:
                self.cache[lang] = json.load(f)
        return self.cache[lang]

    def t(self, lang: str, key: str, **kwargs) -> str:
        text = self.load(lang).get(key)
        if text is None and lang != self.default_lang:
            text = self.load(self.default_lang).get(key, key)
        elif text is None:
            text = key

        return text.format_map(defaultdict(str, **kwargs))
