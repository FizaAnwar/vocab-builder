import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def fetch_word(word):
    """Fetch a word's data from the dictionary API. Returns None if not found."""
    try:
        response = requests.get(API_URL + word, timeout=10)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

def parse_entry(data):
    """Pull out the word, part of speech, definition and an example."""
    entry = data[0]
    first = entry["meanings"][0]
    definition = first["definitions"][0]["definition"]
    example = None
    for meaning in entry["meanings"]:
        for d in meaning["definitions"]:
            if d.get("example"):
                example = d["example"]
                break
        if example:
            break
    return {
        "word": entry["word"],
        "part_of_speech": first["partOfSpeech"],
        "definition": definition,
        "example": example or "No example available",
    }

if __name__ == "__main__":
    word_data = fetch_word("hello")
    if word_data:
        print(parse_entry(word_data))
    else:
        print("Word not found.")