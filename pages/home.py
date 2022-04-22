import streamlit as st
from models import *
import pages.experience_view

test = True

def app():
    st.title('Poupa')
    button = st.button('Nouvelle Campagne')
    if button:
        pages.experience_view.app()

