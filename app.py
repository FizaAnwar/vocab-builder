import random
from datetime import date
import streamlit as st
from vocab import fetch_word, parse_entry, save_flashcard, load_flashcards, load_words

st.set_page_config(page_title="Vocab Builder", page_icon="📚")
st.title("📚 Vocab Builder")

tab_lookup, tab_cards, tab_review, tab_wotd = st.tabs(
    ["🔍 Look up", "🗂️ My flashcards", "🧠 Review", "🌟 Word of the Day"]
)

with tab_lookup:
    word = st.text_input("Enter a word").strip().lower()

    if st.button("Search") and word:
        data = fetch_word(word)
        if data is None:
            st.session_state["card"] = None
            st.error("Could not get that word. Check the spelling or try again later.")
        else:
            st.session_state["card"] = parse_entry(data)

    card = st.session_state.get("card")
    if card:
        st.subheader(f"{card['word']} ({card['part_of_speech']})")
        st.write(f"**Meaning:** {card['definition']}")
        st.write(f"**Example:** {card['example']}")

        saved_words = [c["word"].lower() for c in load_flashcards()]
        if card["word"].lower() in saved_words:
            st.info("Already in your flashcards.")
        elif st.button("💾 Save as flashcard"):
            save_flashcard(card)
            st.success("Saved!")

with tab_cards:
    cards = load_flashcards()
    if not cards:
        st.info("No flashcards yet. Look up a word and save it.")
    else:
        st.write(f"You have **{len(cards)}** flashcards.")
        for c in cards:
            with st.expander(f"{c['word']} ({c['part_of_speech']})"):
                st.write(f"**Meaning:** {c['definition']}")
                st.write(f"**Example:** {c['example']}")
with tab_review:
    cards = load_flashcards()
    if not cards:
        st.info("No flashcards yet. Save some words first.")
    else:
        i = st.session_state.get("review_index", 0) % len(cards)
        c = cards[i]
        st.caption(f"Card {i + 1} of {len(cards)}")
        st.markdown(f"## {c['word']}")
        if st.checkbox("Show meaning", key=f"reveal_{i}"):
            st.write(c["definition"])
            st.write(f"*Example:* {c['example']}")
        if st.button("Next card ➡️"):
            st.session_state["review_index"] = (i + 1) % len(cards)
            st.rerun()
with tab_wotd:
    words = load_words()
    if not words:
        st.info("words.txt not found.")
    else:
        if "wotd_offset" not in st.session_state:
            st.session_state["wotd_offset"] = 0

        if st.button("🎲 Another word", key="another_word"):
            st.session_state["wotd_offset"] = random.randrange(len(words))

        index = (date.today().toordinal() + st.session_state["wotd_offset"]) % len(words)
        word_of_day = words[index]

        data = fetch_word(word_of_day)
        if data is None:
            st.error(f"Could not load '{word_of_day}'. Try another word.")
        else:
            wcard = parse_entry(data)
            st.subheader(f"{wcard['word']} ({wcard['part_of_speech']})")
            st.write(f"**Meaning:** {wcard['definition']}")
            st.write(f"**Example:** {wcard['example']}")

            saved = [c["word"].lower() for c in load_flashcards()]
            if wcard["word"].lower() in saved:
                st.info("Already in your flashcards.")
            elif st.button("💾 Save as flashcard", key="save_wotd"):
                save_flashcard(wcard)
                st.success("Saved!")            