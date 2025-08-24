import os
import json
from collections import defaultdict
from typing import Any

class LangManager:
    def __init__(self, base_path: str = None, default_lang: str = "en"):
        self.cache: dict[str, dict[str, str]] = {}
        self.default_lang = default_lang
        self.base_path = base_path or os.path.join(os.path.dirname(__file__), "..", "data", "lang")

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
        data: dict[str, Any] = self.load(lang)

        for part in key.split("."):
            if isinstance(data, dict):
                data = data.get(part)
            else:
                data = None
                break

        text = data if isinstance(data, str) else None

        if text is None and lang != self.default_lang:
            return self.t(self.default_lang, key, **kwargs)
        if text is None:
            text = key  # fallback, gdy brak tłumaczenia

        return text.format_map(defaultdict(str, **kwargs))

