import json
import os

episodes_file = "database/episodes.json"

initial_episodes = {
    "EP001": {
        "title": "Mama Akos Finds the Missing Money",
        "setting": "Living Room / Kitchen",
        "characters": ["MA001", "KF001"],
        "status": "Planned",
        "prompt_style": "High-drama, traditional Ghanaian household setting, intense facial expressions."
    },
    "EP002": {
        "title": "Papa Kofi Tries to Cook",
        "setting": "Kitchen Chaos",
        "characters": ["PK001", "MA001", "KF001"],
        "status": "Draft",
        "prompt_style": "Comedic, messy kitchen layout, vibrant cinematic colors."
    }
}

with open(episodes_file, "w", encoding="utf-8") as f:
    json.dump(initial_episodes, f, indent=4)

print("✔ Episode database module successfully initialized!")
print(f"✔ Location: {episodes_file}")
