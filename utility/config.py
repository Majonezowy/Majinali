import json
import traceback
from typing import Optional

def load_config() -> dict:
    data = {}
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"{e}\n{traceback.format_exc()}")
    
    return data
