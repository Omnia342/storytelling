import streamlit as st
import requests
from story_logic import export_story_to_pdf

st.set_page_config(page_title="📖 Storytelling Chatbot", layout="centered")
st.title("🎭 Interactive Storytelling Bot")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a creative storyteller. Write engaging interactive stories."}
    ]
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# Select role and genre
role = st.text_input("Enter your role (e.g., Hero, Villain, Time Traveler, etc.):")
bot_role = st.text_input("Enter the bot's role (e.g., Knight, Storyteller, Sidekick, etc.):")
genre = st.selectbox("Choose story genre:", ["Fantasy", "Romantasy", "Sci-Fi", "Mystery", "Post-apocalyptic", "Horror", "Romance", "Romantic Comedy"])
user_input = st.text_input("What do you do next?")

# Continue the story
if st.button("Continue Story"):
    if user_input:
        res = requests.post(
            "http://localhost:8000/story",
            json={
                "role": role,
                "genre": genre,
                "history": st.session_state.chat_history,
                "user_input": user_input,
                "inventory": st.session_state.inventory
            }
        )
        if res.status_code == 200:
            data = res.json()
            reply = data["response"]
            st.session_state.inventory = data.get("inventory", [])

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

            st.markdown("### 📜 Story so far:")
            for msg in st.session_state.chat_history[1:]:
                icon = "👤" if msg["role"] == "user" else "🧙‍♂️"
                st.markdown(f"{icon} {msg['content']}")
        else:
            st.error("Backend error!")
    else:
        st.warning("Please write something to continue the story.")

# Inventory Display
if st.session_state.inventory:
    st.markdown("### 🧰 Inventory Collected:")
    for item in st.session_state.inventory:
        st.markdown(f"🔹 {item}")

# Export to PDF
if st.button("📄 Download My Story"):
    story_text = "\n\n".join([m["content"] for m in st.session_state.chat_history if m["role"] != "system"])
    export_story_to_pdf(story_text)
    with open("story.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="my_story.pdf")
