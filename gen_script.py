import json
import os
import google.generativeai as genai


GEMINI_API_KEY = "AIzaSyDbYm1zKV4Eiu7_61nbVfYC-tj7BcNT2Y4"

INPUT_FILE = "filtered_data.json"
OUTPUT_FILE = "video_plan.json"

def create_prompt(data):
    """
    Creates a prompt for Gemini to generate the script.
    """
    # We take the first 20 facts to ensure we cover enough history
    facts = [item['content'] for item in data[:20]]
    context = "\n".join(facts)

    prompt = f"""
    You are a documentary director creating a short video about the 'Legacy of IIT (ISM) Dhanbad'.
    
    Here is the raw data extracted from the archives:
    {context}

    INSTRUCTIONS:
    1. Create a compelling 5-segment script based ONLY on this data.
    2. Each segment must have a 'narration' (voiceover text) and an 'image_prompt' (for AI image generation).
    3. The 'image_prompt' must be descriptive (e.g., "Black and white photo of...", "Modern drone shot of...").
    4. Output strictly valid JSON format.

    JSON STRUCTURE:
    {{
        "segments": [
            {{
                "id": 1,
                "narration": "Text...",
                "image_prompt": "Prompt..."
            }}
        ]
    }}
    """
    return prompt

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Did you run data_loader.py?")
        return

    # 1. Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Use 'gemini-1.5-flash' for speed/efficiency, or 'gemini-pro'
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. Load Data
    print("Loading filtered data...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        print("No data found! Check your data_loader script.")
        return

    # 3. Generate Content
    print("Asking Gemini to write the script...")
    prompt = create_prompt(data)
    
    try:
        response = model.generate_content(prompt)
        content = response.text

        # 4. Clean formatting (Gemini often adds ```json ... ``` blocks)
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()

        # 5. Save Result
        script_json = json.loads(content)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(script_json, f, indent=4)
            
        print(f"Success! Video plan saved to {OUTPUT_FILE}")
        print("Preview of Segment 1:")
        print(script_json['segments'][0])

    except Exception as e:
        print(f"An error occurred: {e}")
        # Debugging: print raw response if JSON fails
        if 'content' in locals():
            print("Raw output was:", content)

if __name__ == "__main__":
    main()