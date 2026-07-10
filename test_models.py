import os
import google.generativeai as genai

# The key is fetched from your Render Environment Variables
# Ensure your Render 'API_KEY' variable is set correctly
api_key = os.environ.get("API_KEY")

if not api_key:
    print("Error: API_KEY environment variable not found.")
else:
    genai.configure(api_key=api_key)
    print("--- Available Models for your Key ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
    except Exception as e:
        print(f"Error accessing API: {e}")
