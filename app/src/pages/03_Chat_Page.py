import streamlit as st
from datetime import datetime
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Customer Chat")
SideBarLinks()

# ---- Styling ----
st.markdown("""
<style>
.chat-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.chat-header h1 {
    color: white;
    margin: 0;
}

.chat-header p {
    color: #a0a0a0;
    margin: 0.5rem 0 0 0;
}

.chat-message {
    padding: 0.75rem 1rem;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    max-width: 80%;
}

.chat-customer {
    background: #007bff;
    color: white;
    margin-left: auto;
}

.chat-admin {
    background: #f1f3f4;
    color: #333;
}

.chat-timestamp {
    font-size: 0.7rem;
    opacity: 0.7;
    margin-top: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown(f"""
<div class="chat-header">
    <h1>💬 Customer Support Chat</h1>
    <p>Talk with an admin, {st.session_state.get('first_name', 'Customer')}!</p>
</div>
""", unsafe_allow_html=True)

# ---- Get customer ID ----
customer_id = st.session_state.get('customer_id')

if not customer_id:
    st.error("No customer ID found. Please log in again.")
    if st.button("Return to Home"):
        st.switch_page("Home.py")
    st.stop()

# API BASE
API_BASE = f"http://web-api:4000/d/customer/{customer_id}"

# ---- Fetch messages ----
@st.cache_data(ttl=10)
def fetch_messages(customer_id):
    try:
        response = requests.get(f"http://web-api:4000/d/customer/{customer_id}/customermessages")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching messages: {e}")
        return []

messages = fetch_messages(customer_id)

# ---- Chat History ----
st.subheader("Message History")

with st.container():
    if messages:
        for msg in messages:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 0.5rem;">
                <div class="chat-message chat-customer">
                    <div>{msg.get('content', '')}</div>
                    <div class="chat-timestamp">📅 {msg.get('timestamp', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No messages yet. Start a conversation below!")

st.markdown("---")

# ---- Send Message ----
st.subheader("Send a Message to Admin")

with st.form("send_msg_form", clear_on_submit=True):
    content = st.text_area("Your Message:", placeholder="Type your message here...", height=100)
    submitted = st.form_submit_button("📤 Send Message", use_container_width=True)

    if submitted and content.strip():
        try:
            message_id = int(datetime.now().timestamp() * 1000) % 2147483647

            response = requests.post(
                f"http://web-api:4000/d/customer/{customer_id}/customermessages",
                json={
                    "messageID": message_id,
                    "timestamp": datetime.now().strftime('%Y-%m-%d'),
                    "content": content.strip()
                }
            )

            if response.status_code == 201:
                st.success("Message sent successfully! 🎉")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(f"Failed to send message: {response.text}")

        except Exception as e:
            st.error(f"Error sending message: {e}")

# ---- Quick Messages ----
st.markdown("**Quick Messages:**")

quick_cols = st.columns(3)
quick_messages = [
    "I need help with my order",
    "Something is missing from my delivery",
    "Can I change my delivery time?"
]

for idx, qmsg in enumerate(quick_messages):
    with quick_cols[idx]:
        if st.button(qmsg, key=f"quick_{idx}", use_container_width=True):
            try:
                message_id = int(datetime.now().timestamp() * 1000) % 2147483647

                response = requests.post(
                    f"http://web-api:4000/d/customer/{customer_id}/customermessages",
                    json={
                        "messageID": message_id,
                        "timestamp": datetime.now().strftime('%Y-%m-%d'),
                        "content": qmsg
                    }
                )

                if response.status_code == 201:
                    st.success("Quick message sent!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Failed to send")
            except Exception as e:
                st.error(f"Error: {e}")

# ---- Footer ----
st.divider()
col_back, col_refresh = st.columns([1, 1])

with col_back:
    if st.button("← Back to Customer Home"):
        st.switch_page("pages/11_Customer_Home.py")

with col_refresh:
    if st.button("🔄 Refresh Messages"):
        st.cache_data.clear()
        st.rerun()
