# from IPython.display import clear_output
import socket
import sys
import cv2
import matplotlib.pyplot as plt
import pickle
import numpy as np
import struct ## new
import zlib
from PIL import Image, ImageOps
# import streamlit as st
import face_recognition
import imutils
from datetime import datetime, date
import pandas as pd
import pickle

from utils import face_comparison

HOST='127.0.0.1'
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

# FRAME_WINDOW = st.image([])
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

student = pd.read_csv('./data/db.csv')

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        if not data:
            cv2.destroyAllWindows()
            conn,addr=s.accept()
            continue

    # receive image row data form client socket
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    # unpack image using pickle 
    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # detect face in the video
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    name = face_comparison(frame)

    # check if person exists in database
    if name is not None and name!='Unknown':
        attendance = pd.read_csv('./data/attendance.csv')
        if len(attendance)==0:
            attendance = attendance.append({'name':name, 'entrance_time':datetime.now(),'entrance_date':date.today()}, ignore_index=True).reset_index(drop=True)
            attendance.to_csv('./data/attendance.csv')

        per = attendance.loc[attendance['name']==name]
        if len(per)!=0:
            tail = per.tail(1)
            dt = str(list(tail['entrance_date'])[0]).split('-')
            if int(dt[0])!=int(datetime.now().year) and int(dt[1])!=int(datetime.now().month) and int(dt[2])!=int(datetime.now().day):
                attendance = attendance.append({'name':name, 'entrance_time':datetime.now(),'entrance_date':date.today()}, ignore_index=True).reset_index(drop=True)
                attendance.to_csv('./data/attendance.csv')
        else:
            attendance = attendance.append({'name':name, 'entrance_time':datetime.now(),'entrance_date':date.today()}, ignore_index=True).reset_index(drop=True)
            attendance.to_csv('./data/attendance.csv')
        
    # adding a rectangle to face detected and name
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,255,0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        if name is not None:
            cv2.putText(frame, name, (x+6,h-6), font, 1.0,(255,255,255),1)
    # FRAME_WINDOW.image(frame, caption=name, width=700)

    with open('stream','wb') as fp:
        pickle.dump(frame, fp)

    

video.release()



