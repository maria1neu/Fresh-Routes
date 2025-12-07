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

# gets the most popular recipe 
response = requests.get(f"{API_URL}/f/recipe")

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

# graphs predictions 

st.title("Ingredient Popularity Predictions")

try:
    produce_response = requests.get(f"{API_URL}/f/produce")
    produce_response.raise_for_status()
    produce_list = produce_response.json()
except Exception as e:
    st.error(f"Could not load produce list: {e}")
    st.stop()

ingredient_names = []
current_values = []
predicted_values = []

for item in produce_list:
    produceID = item["produceID"]
    name = item["name"]
    ingredient_names.append(name)

    try:
        demand_response = requests.get(f"{API_URL}/demand/produce/{produceID}")
        if demand_response.status_code == 200:
            predicted_values.append(demand_response.json()["predictedDemand"])
        else:
            predicted_values.append(None)
    except:
        predicted_values.append(None)

    current_values.append(80)

df = pd.DataFrame({
    "Ingredient": ingredient_names,
    "Current": current_values,
    "Predicted": predicted_values
})


fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Ingredient"], y=df["Current"],
    mode="lines+markers",
    name="Current",
    line=dict(color="#2ecc71")
))

fig.add_trace(go.Scatter(
    x=df["Ingredient"], y=df["Predicted"],
    mode="lines+markers",
    name="Predicted (3 months)",
    line=dict(color="#2980b9", dash="dot")
))

fig.update_layout(
    title="Ingredient Popularity Predictions",
    yaxis_title="Popularity Score",
    xaxis_title="Ingredient",
    height=400
)

st.plotly_chart(fig, use_container_width=True)
