import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# ---- Page Config ----
st.set_page_config(layout='wide')

# ---- Sidebar ----
SideBarLinks()

# ------------------------------
#       PAGE STYLING
# ------------------------------

st.markdown("""
<style>
.section-box {
    background: #A0CFA0;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.2rem;
    color: black;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}
.checkbox-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 0.5rem;
}
.counter-box {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}
.counter-btn {
    background: #88B888;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    font-size: 1.4rem;
    font-weight: 700;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.chat-box {
    background: #A0CFA0;
    padding: 1rem;
    border-radius: 12px;
    height: 650px;
}
.chat-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
#     HERO SECTION
# ------------------------------

st.markdown(f"""
<div style="background: #A0CFA0; padding: 2rem; border-radius: 15px; margin-bottom: 1.5rem;">
    <h1 style="margin-bottom: 0.3rem;">🥗 Meal Preferences</h1>
    <p>Update your dietary preferences, delivery schedule, and meal quantity.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------
#     PAGE LAYOUT
# ------------------------------

left_col, mid_col, right_col = st.columns([1.1, 1.3, 1])

# ------------------------------
#     LEFT COLUMN — CHAT
# ------------------------------

with left_col:
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    st.markdown("<div class='chat-title'>Chat</div>", unsafe_allow_html=True)

    # Placeholder chat bubbles (decorative only)
    st.write("🟢 Hello! Let me know your meal preferences.")
    st.write("🟢 You can update dietary choices or delivery frequency anytime.")
    st.text_input("Send a message:", placeholder="Type here...")

    st.markdown("</div>", unsafe_allow_html=True)  # close chat-box


# ------------------------------
#     MIDDLE COLUMN — MEAL PREFS
# ------------------------------

with mid_col:
    # --- DIETARY PREFERENCES ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>DIETARY PREFERENCES</div>", unsafe_allow_html=True)

    dietary_options_col1 = [
        "Vegetarian",
        "Vegan",
        "Gluten Free",
    ]

    dietary_options_col2 = [
        "High Protein",
        "Dairy Free",
        "Nut Free"
    ]

    colA, colB = st.columns(2)

    with colA:
        veg = st.checkbox("Vegetarian")
        vegan = st.checkbox("Vegan")
        gf = st.checkbox("Gluten Free")

    with colB:
        hp = st.checkbox("High Protein")
        df = st.checkbox("Dairy Free")
        nf = st.checkbox("Nut Free")

    st.markdown("</div>", unsafe_allow_html=True)

    # --- DELIVERY PREFERENCES ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>DELIVERY PREFERENCES</div>", unsafe_allow_html=True)

    colC, colD = st.columns(2)

    with colC:
        once = st.checkbox("Once a week")
        other = st.checkbox("Every other week")
    with colD:
        twice = st.checkbox("Twice a week")
        monthly = st.checkbox("Monthly")

    st.markdown("</div>", unsafe_allow_html=True)

    # --- MEALS PER DELIVERY ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>AMOUNT OF MEALS PER DELIVERY</div>", unsafe_allow_html=True)

    count_col1, count_col2, count_col3 = st.columns([1, 1, 1])

    with count_col2:
        st.number_input("Meals per delivery", min_value=1, max_value=20, value=5, step=1, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------
#     RIGHT COLUMN — EXTRA INPUTS
# ------------------------------

with right_col:

    # --- Additional Info ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    add_info = st.text_input("Additional Information:")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- DATE PICKER ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Select Start Date</div>", unsafe_allow_html=True)
    date_selected = st.date_input("Start Date", format="MM/DD/YYYY")
    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------
#     SAVE BUTTON
# ------------------------------

st.divider()

save = st.button("💾 Save Preferences", use_container_width=True)

if save:
    st.success("Your meal preferences have been saved successfully!")


# ------------------------------
#     FOOTER
# ------------------------------

st.markdown("""
<div style="text-align:center; color:#555; margin-top: 2rem;">
    🍽️ Preferences updated — your meals will now be tailored to you.
</div>
""", unsafe_allow_html=True)
