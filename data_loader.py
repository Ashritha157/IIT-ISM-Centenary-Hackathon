import os
import json
from bs4 import BeautifulSoup

BASE_DIRS = [
    os.path.join("news_articles", "dataset", "html"),
    os.path.join("website_crawls", "dataset", "html")
]
OUTPUT_FILE = "filtered_data.json"

KEYWORDS = [
    "history", "established", "1926", "legacy", "campus", 
    "diamond jubilee", "centenary", "mining", "petroleum", 
    "evolution", "achievement", "ranking", "president"
]

def extract_text_from_html(file_path):
    """Parses HTML and returns visible text."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return " ".join(soup.get_text().split())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def filter_content(text, source_name):
    text_lower = text.lower()
    found_keywords = [k for k in KEYWORDS if k in text_lower]
    
    if found_keywords:
        return {
            "source": source_name,
            "keywords": found_keywords,
            "content": text[:500] + "..." 
        }
    return None

def main():
    relevant_data = []
    
    print("Starting crawler...")
    
    for base_dir in BASE_DIRS:
        if not os.path.exists(base_dir):
            print(f"Skipping missing directory: {base_dir}")
            continue

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file == "index.html":
                    full_path = os.path.join(root, file)
                    folder_name = os.path.basename(root)
                    
                 
                    text = extract_text_from_html(full_path)
                    
                    
                    result = filter_content(text, folder_name)
                    
                    if result:
                        relevant_data.append(result)
                        print(f"Found match in: {folder_name}")

    
    print(f"Total relevant records: {len(relevant_data)}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(relevant_data, f, indent=4)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()