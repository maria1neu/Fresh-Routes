import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Driver, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View + Edit Calendar',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Availability_Calendar.py')

if st.button('Plan Your Route',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Route_Planner.py')


