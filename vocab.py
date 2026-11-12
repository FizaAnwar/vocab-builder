import json
import os
import time
import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
FLASHCARD_FILE = "flashcards.json"


def fetch_word(word, retries=3):
    """Fetch a word's data from the dictionary API. Returns None if not found or unavailable."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(API_URL + word, timeout=10)
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json()

        # Server problem (500, 502, 503...): wait and retry
        print(f"Server error {response.status_code}. Retrying ({attempt}/{retries})...")
        time.sleep(2)

    print("The dictionary service is unavailable right now. Please try again later.")
    return None


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


def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        with open(FLASHCARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_flashcard(card):
    cards = load_flashcards()
    if any(c["word"].lower() == card["word"].lower() for c in cards):
        print("Already in your flashcards.")
        return
    cards.append(card)
    with open(FLASHCARD_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
    print("Saved to flashcards.json")


def review_flashcards():
    cards = load_flashcards()
    if not cards:
        print("No flashcards yet.")
        return
    for card in cards:
        input(f"\nWhat does '{card['word']}' mean? (press Enter to reveal)")
        print(card["definition"])
        print("Example:", card["example"])


def show_card(card):
    print(f"\nWord: {card['word']} ({card['part_of_speech']})")
    print(f"Meaning: {card['definition']}")
    print(f"Example: {card['example']}\n")


def main():
    while True:
        word = input("Enter a word (or 'q' to quit): ").strip().lower()
        if word == "q":
            break
        if not word:
            continue
        data = fetch_word(word)
        if data is None:
            print("Could not get that word. Check the spelling or try again later.")
            continue
        card = parse_entry(data)
        show_card(card)
        if input("Save as flashcard? (y/n): ").strip().lower() == "y":
            save_flashcard(card)


if __name__ == "__main__":
    main()