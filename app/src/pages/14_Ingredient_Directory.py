import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd

# Initialize sidebar
SideBarLinks()

st.title("Ingredient Directory")

# API endpoint
API_URL = "http://web-api:4000"

response = requests.get(f"{API_URL}/recipe")

if response.status_code == 200:
    all_recipes = response.json()
    recipes = all_recipes[:6]
else:
    st.error("Could not load recipes")
    recipes = []


row1 = st.columns(3)
row2 = st.columns(3)

all_cols = row1 + row2

for row, col in enumerate(all_cols):
    tile = col.container(height=150)

    if row < len(recipes): 
        r = recipes[row]

        tile.subheader(r["name"])
        tile.write(r["description"])
        tile.write(f"⭐ Popularity: {r['popularityScore']}")
    else:
        # Empty tile placeholder
        tile.write("")


