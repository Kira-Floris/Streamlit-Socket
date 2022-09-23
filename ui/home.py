import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd 
from PIL import Image
import cv2
import os
import pickle
import time

from utils import face_recognition

def home():
    
    st.header('Home')
    FRAME_WINDOW = st.image([])
    while True:
        try:
            with open('stream', 'rb') as fp:
                frame = pickle.load(fp)
            FRAME_WINDOW.image(frame, caption='None', width=700)
            
        except:
            continue
    # read the list while appending 


    