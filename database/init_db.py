import json
import os

# Define the path for our character storage
db_file = "database/characters.json"

# Master data profile for MAAE Core Phase 1
initial_characters = {
    "MA001": {
        "name": "Mama Akos",
        "role": "Mother",
        "personality": "Strict, Funny, Protective, Very dramatic",
        "voice": "Ghanaian Female",
        "status": "Main"
    },
    "PK001": {
        "name": "Papa Kofi",
        "role": "Father",
        "personality": "Calm, Funny, Always laughing",
        "voice": "Ghanaian Male",
        "status": "Main"
    },
    "KF001": {
        "name": "Kofi",
        "role": "Son",
        "personality": "Funny, Curious, Stubborn",
        "voice": "Young Ghanaian Male",
        "status": "Main"
    }
}

# Write data to the file safely
with open(db_file, "w", encoding="utf-8") as f:
    json.dump(initial_characters, f, indent=4)

print("✔ Character database successfully initialized!")
print(f"✔ Location: {db_file}")
