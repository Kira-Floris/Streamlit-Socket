import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd 
from PIL import Image
import cv2
import os

from utils import face_encoding_save

def register():
    st.header('Registration Form for Students')
    with st.form('Student Registration Form'):
        profile = st.file_uploader("Upload a passport photo", type=['png', 'jpeg', 'jpg'])
        name = st.text_input('Enter your names')
        reg = st.text_input('Enter your registration number')

        submitted = st.form_submit_button("Register")
        if submitted:
            data = pd.read_csv('./data/db.csv')
            if name in list(data['name']):
                st.write('Student with this name already exists. Try another one.')
                return
            
            if profile is not None:
                with open(os.path.join('images',name+'.jpeg'),'wb') as f:
                    f.write(profile.getbuffer())

                profile_path = 'images/'+name+'.jpeg'
                data = data.append({'name':name, 'image':profile_path, 'reg':reg}, ignore_index=True)
                data.to_csv('./data/db.csv')
                face_encoding_save(profile_path, name)


                

    