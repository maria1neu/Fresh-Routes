import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# ---- Page Config (must be first) ----
st.set_page_config(layout='wide')

# ---- Sidebar ----
SideBarLinks()

# ---- Styling (matches your app theme) ----
st.markdown("""
<style>
.chat-hero {
    background: linear-gradient(135deg, #E8F4FF, #F3FAFF);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
}

.chat-box {
    background: white;
    border-radius: 18px;
    padding: 2rem;
    box-shadow: 0 12px 25px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---- Header Section ----
st.markdown(f"""
<div class="chat-hero">
    <h1>💬 Customer Support Chat</h1>
    <p>Hi {st.session_state['first_name']}, how can we help you today?</p>
</div>
""", unsafe_allow_html=True)

# ---- Initialize Chat History ----
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ---- Chat Display Container ----
with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Support:** {content}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Message Input ----
user_input = st.text_input("Type your message here:", placeholder="Ask us anything...")

# ---- Send Button ----
if st.button("Send Message", use_container_width=True):

    if user_input.strip() != "":
        # Save user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })

        # Fake automated reply (you can replace later with real AI/API)
        bot_reply = "Thanks for your message! Our support team will get back to you shortly."

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        # Clear input & refresh
        st.rerun()

# ---- Footer ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding: 1rem;">
    💙 We're here to help you, and your diet, 24/7.
</div>
""", unsafe_allow_html=True)

