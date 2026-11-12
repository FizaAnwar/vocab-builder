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

if __name__ == "__main__":
    print(fetch_word("hello"))