import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

# ---- Page Config ----
st.set_page_config(layout='wide')

# ---- Sidebar ----
SideBarLinks()

# ===============================
#       CUSTOM STYLING
# ===============================
st.markdown("""
<style>

.meal-header {
    font-size: 2.2rem;
    font-weight: 700;
    padding: 0.8rem 1rem;
    background: #A0CFA0;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

.day-title {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.meal-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.7rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    position: relative;
}

.meal-name {
    font-size: 1.1rem;
    font-weight: 700;
}

.remove-btn {
    position: absolute;
    top: 6px;
    right: 8px;
    font-size: 1.2rem;
    cursor: pointer;
}

.recipe-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    height: 230px;
    border-left: 5px solid #5FA45F;
}

.recipe-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.recipe-body {
    color: #444;
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
}

</style>
""", unsafe_allow_html=True)


# ===============================
#        HERO SECTION
# ===============================

st.markdown("""
<div class="meal-header">MEALS</div>
""", unsafe_allow_html=True)


# ===============================
#   MEAL PLAN STATE (SESSION)
# ===============================

if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {
        "Monday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Tuesday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Wednesday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Thursday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Friday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Saturday": {"Breakfast": None, "Lunch": None, "Dinner": None},
        "Sunday": {"Breakfast": None, "Lunch": None, "Dinner": None},
    }

# ===============================
#         WEEK GRID
# ===============================

week_days = list(st.session_state.meal_plan.keys())
cols = st.columns(7)

for i, day in enumerate(week_days):
    with cols[i]:
        st.markdown(f"<div class='day-title'>{day[:3].upper()}</div>", unsafe_allow_html=True)

        for meal in ["Breakfast", "Lunch", "Dinner"]:
            with st.container():
                st.markdown("<div class='meal-card'>", unsafe_allow_html=True)

                # Remove button
                remove_key = f"remove-{day}-{meal}"
                if st.button("✖", key=remove_key):
                    st.session_state.meal_plan[day][meal] = None

                st.markdown(f"<div class='meal-name'>{meal}</div>", unsafe_allow_html=True)

                current = st.session_state.meal_plan[day][meal]
                if current:
                    st.write(current)
                else:
                    st.write("Name")

                st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ===============================
#     RECIPE SELECTION SECTION
# ===============================

st.subheader("Available Recipes")

recipe_cols = st.columns(5)

# Updated recipe list with real data + emojis + short headers
recipes = [
    {
        "emoji": "🍋",
        "name": "Lemon Herb Chicken",
        "short": "Bright lemon-garlic chicken.",
        "desc": "A bright, refreshing high-protein chicken dish marinated in lemon, garlic, and herbs.",
        "ingredients": "Chicken • Lemon • Garlic • Parsley • Olive Oil"
    },
    {
        "emoji": "🥦",
        "name": "Veggie Stir-Fry",
        "short": "Colorful soy-ginger stir-fry.",
        "desc": "A colorful plant-based stir-fry tossed in a soy-ginger glaze.",
        "ingredients": "Broccoli • Bell Peppers • Carrots • Soy Sauce • Ginger"
    },
    {
        "emoji": "🍝",
        "name": "Pasta Primavera",
        "short": "Light pasta with veggies.",
        "desc": "A classic Italian pasta tossed with seasonal vegetables and garlic.",
        "ingredients": "Pasta • Zucchini • Tomatoes • Garlic • Parmesan"
    },
    {
        "emoji": "🥗",
        "name": "Quinoa Bowl",
        "short": "Protein-packed quinoa bowl.",
        "desc": "A nourishing bowl of quinoa, roasted veggies, chickpeas, and lemon-tahini sauce.",
        "ingredients": "Quinoa • Sweet Potato • Spinach • Chickpeas • Tahini"
    },
    {
        "emoji": "🍛",
        "name": "Tofu Coconut Curry",
        "short": "Creamy coconut tofu curry.",
        "desc": "A creamy coconut curry with tofu, vegetables, and warm spices.",
        "ingredients": "Tofu • Coconut Milk • Curry Paste • Carrots • Basil"
    },
]


# We only display the top emoji/title/short description here
for idx, col in enumerate(recipe_cols):
    recipe = recipes[idx]
    with col:

        # TOP CARD — White with yellow footer (your style)
        st.markdown("""
        <div style="
            background-color: white;
            border-radius: 14px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem;">""" + recipe["emoji"] + """</div>
            <div style="font-weight: 700; font-size: 1.1rem; margin-top: 0.4rem;">""" + recipe["name"] + """</div>
            <div style="font-size: 0.85rem; color: #444;">""" + recipe["short"] + """</div>
        </div>
        """, unsafe_allow_html=True)

        # SELECT button (same)
        if st.button("SELECT", key=f"select-recipe-top-{idx}"):
            st.session_state["selected_recipe"] = recipe["name"]
            st.success(f"Selected: {recipe['name']}")

st.divider()

# ===============================
#   ASSIGN SELECTED RECIPE TO MEAL
# ===============================

st.subheader("Assign Selected Recipe to a Meal")

selected_recipe = st.session_state.get("selected_recipe", None)

if not selected_recipe:
    st.info("Select a recipe above to assign it to a meal.")
else:
    day = st.selectbox("Day", week_days)
    meal = st.selectbox("Meal", ["Breakfast", "Lunch", "Dinner"])

    if st.button("Assign Recipe"):
        st.session_state.meal_plan[day][meal] = selected_recipe
        st.success(f"Assigned '{selected_recipe}' to {meal} on {day}!")

