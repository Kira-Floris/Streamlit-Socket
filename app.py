import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go

from ui.register import register
from ui.home import home

st.set_page_config(page_title='Face Recognition Attendance System')

selected = option_menu(
    menu_title="Stroke Prediction AI", # required
    options=['Home','Register'],
    default_index = 0,
    orientation = 'horizontal',
    styles={
        "container": {"padding":"0!important", "background-color":"write",},
        "nav-link":{
            "font-size":"18px",
            "text-align":"left",
            "margin":"0px",
            },
        "nav-link-selected":{"background-color":"gray"}, 
            },
)

if selected == 'Home':
    home()

if selected == 'Register':
    register()