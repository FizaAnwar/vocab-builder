import streamlit as st
from vocab import fetch_word, parse_entry, save_flashcard, load_flashcards

st.set_page_config(page_title="Vocab Builder", page_icon="📚")
st.title("📚 Vocab Builder")

tab_lookup, tab_cards = st.tabs(["🔍 Look up", "🗂️ My flashcards"])

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