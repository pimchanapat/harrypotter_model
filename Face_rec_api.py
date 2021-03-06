from PIL import Image, ImageDraw
import face_recognition
import numpy as np
import pickle

import io
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

known_face_names, known_face_encodings = pickle.load(open('faces.p', 'rb'))

@app.post("/faces_recognition/")
async def faces_recognition(image_upload: UploadFile = File(...)):
    data = await image_upload.read()

    # Load an image
    image = Image.open(io.BytesIO(data))

    # Detect face(s) and encode them
    face_locations = face_recognition.face_locations(np.array(image))
    face_encodings = face_recognition.face_encodings(np.array(image), face_locations)

    draw = ImageDraw.Draw(image)
    face_names = []

    # Recognize face(s)
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = known_face_names[best_match_index]

        top, right, bottom, left = face_location
        draw.rectangle([left, top, right, bottom])
        draw.text((left, top), name)
        face_names.append(name)

    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='PNG')
    image_byte_arr = image_byte_arr.getvalue()
    return StreamingResponse(io.BytesIO(image_byte_arr), media_type='image/png')