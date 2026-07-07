import json
import os
import requests

CHAR_FILE = "/home/JoHn123Paul/MAAE-Core/database/characters.json"
EPI_FILE = "/home/JoHn123Paul/MAAE-Core/database/episodes.json"

OPENROUTER_API_KEY = ""

def generate_script(episode_id):
    if not os.path.exists(CHAR_FILE) or not os.path.exists(EPI_FILE):
        return {"error": "Missing database files."}

    with open(CHAR_FILE, 'r') as f:
        characters = json.load(f)
    with open(EPI_FILE, 'r') as f:
        episodes = json.load(f)

    if episode_id not in episodes:
        return {"error": f"Episode {episode_id} not found."}

    episode = episodes[episode_id]

    profile_summary = ""
    for char_id in episode["characters"]:
        if char_id in characters:
            c = characters[char_id]
            profile_summary += f"- {c['name']} ({c['role']}): Personality is {c['personality']}. Voice style is {c['voice']}.\n"

    prompt = f"""
You are an expert comedic scriptwriter specializing in funny Ghanaian short skits.
Write a short comedy script based on the setup below.

EPISODE TITLE: {episode['title']}
SETTING: {episode['setting']}
PROMPT VISUAL STYLE: {episode['prompt_style']}

CHARACTERS INVOLVED:
{profile_summary}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        if 'choices' in res_data:
            script_content = res_data['choices'][0]['message']['content']
            return {"success": True, "script": script_content}
        else:
            return {"error": f"OpenRouter Error Details: {json.dumps(res_data)}"}
    except Exception as e:
        return {"error": f"Network Call failed: {str(e)}"}

if __name__ == "__main__":
    print("🎬 Testing AI Script Writer for EP001...")
    result = generate_script("EP001")
    if "success" in result:
        print("\n--- GENERATED SCRIPT ---\n")
        print(result["script"])
    else:
        print("\n❌ Error Debug Info:")
        print(result["error"])
