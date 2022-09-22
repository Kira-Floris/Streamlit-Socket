import face_recognition
import numpy as np
import cv2
import json

f = open('encodings.json')
encodings_json = json.load(f)
# print(encodings_json['encodings'])

def face_encoding_save(image_path, name):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]

    encodings = encodings_json['encodings']
    names = encodings_json['names']
    temp_names  = encodings_json['names']

    if name in temp_names:
        return 'person already exists'

    encoding_float = []
    for i in encoding:
        encoding_float.append(float(i))
    encodings.append(encoding_float)
    names.append(name)

    temp = dict()
    temp['encodings'] = encodings
    temp['names'] = names

    with open('encodings.json', 'w') as outfile:
        json.dump(temp, outfile)

def face_comparison(frame):
    rgb_frame = frame[:,:,::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    known_face_encodings = encodings_json['encodings']
    known_face_names = encodings_json['names'] 

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = 'Unknown'

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        return name
    
    return None


