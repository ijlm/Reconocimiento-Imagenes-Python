import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import time
import streamlit as st
from PIL import Image

model = load_model('modelo/modelo.h5') 

def process_image(img, img_width, img_height):
    img = cv2.resize(img, (img_width, img_height))
    img = img.reshape(1, img_width, img_height, 3)
    img = img / 255.0
    return img

def main():
    st.title("Reconocimiento Facial Borrachos")
    st.write("Presiona el botón 'Iniciar' para comenzar el reconocimiento facial.")

    cap = cv2.VideoCapture(0)
    detener = st.checkbox("Detener")    
    image_placeholder = st.empty()

    if st.button("Iniciar"):
        while not detener:
            ret, frame = cap.read()
            img = process_image(frame, 224, 224)
            prediction = model.predict(img)

            if prediction < 0.4:
                label = 'Normal'
                color = (0, 255, 0)
            else:
                label = 'Borracho'
                color = (0, 0, 255)

            frame = cv2.putText(frame, label + str(prediction), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            pil_image = Image.fromarray(frame)
            image_placeholder.image(pil_image)

            time.sleep(0.5)
            
        cap.release()

if __name__ == "__main__":
    main()
