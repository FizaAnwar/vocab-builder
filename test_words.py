from vocab import fetch_word, parse_entry, load_words

for w in load_words()[:10]:
    data = fetch_word(w)
    print(w, "->", parse_entry(data)["definition"] if data else "not found")