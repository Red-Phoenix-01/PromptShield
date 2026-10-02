import json
from pathlib import Path


def load_attacks():
    file_path = Path(__file__).parent.parent / "tests" / "prompt_injection.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)