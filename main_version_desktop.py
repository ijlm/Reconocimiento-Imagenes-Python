import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import time

# Carga el modelo previamente entrenado
model = load_model('modelo/modelo.h5')  # Reemplaza 'ruta_del_modelo.h5' con la ruta real del archivo h5

# Función para procesar la imagen capturada por la cámara
def process_image(img,img_width,img_height):
    img = cv2.resize(img, (img_width, img_height))  # Ajusta el tamaño de la imagen según el modelo
    img = img.reshape(1, img_width, img_height, 3)  # Ajusta las dimensiones para el modelo
    img = img / 255.0  # Normaliza los valores de píxeles entre 0 y 1
    return img

# Configuración de la cámara
cap = cv2.VideoCapture(0)  # 0 indica que se utilizará la cámara predeterminada

while True:
    ret, frame = cap.read()  # Captura un frame desde la cámara

    # Procesa el frame capturado
    img = process_image(frame,224,224)

    # Realiza la predicción con el modelo
    prediction = model.predict(img)
    if prediction < 0.4:
        label = 'Normal'
        color = (0, 255, 0)
    else:
        label = 'Borracho'
        color = (0, 0, 255)

    # Muestra el resultado en la ventana
    frame = cv2.putText(frame, label + str(prediction), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Reconocimiento facial', frame)

    # Si se presiona la tecla 'q', se detiene el programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.5)
# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
