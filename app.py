import streamlit as st
from vocab import fetch_word, parse_entry

st.set_page_config(page_title="Vocab Builder", page_icon="📚")
st.title("📚 Vocab Builder")

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