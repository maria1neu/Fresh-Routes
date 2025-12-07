import streamlit as st
from modules.nav import SideBarLinks
from modules.chat_utils import load_chats, save_chats

st.set_page_config(layout="wide")
SideBarLinks()

st.title("📨 Customer Support Inbox")

chats = load_chats()

customers = list(chats["customers"].keys())

if not customers:
    st.info("No customer messages yet.")
    st.stop()

selected = st.selectbox("Select Customer:", customers)

st.subheader(f"Chat with {selected}")

# Show history
for entry in chats["customers"][selected]:
    speaker = entry["from"]
    message = entry["message"]
    if speaker == "customer":
        st.markdown(f"**{selected}:** {message}")
    else:
        st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {message}</div>", unsafe_allow_html=True)

# Admin response box
reply = st.text_input("Your reply:")

if st.button("Send Reply"):
    if reply.strip():
        chats["customers"][selected].append({
            "from": "admin",
            "message": reply
        })
        save_chats(chats)
        st.session_state["refresh"] = not st.session_state.get("refresh", False)


