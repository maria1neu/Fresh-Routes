import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# creating tabs
col1, col2 = st.tabs(['Meal Preferences', 'Meal Planning'])

with col1: 
  if st.button("Meal Preferences", use_container_width=True):
      st.switch_page("pages/01_Customer_Preferences.py")

with col2: 
  if st.button("Meal Planning", use_container_width=True):
      st.switch_page('pages/02_Meal_Plan.py')

"""# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if st.button('View Meal Preferences', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Customer_Preferences.py')

if st.button('View Meal Plan', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Meal_Plan.py')"""