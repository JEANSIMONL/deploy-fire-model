import streamlit as st
import cv2
from ultralytics import YOLO
from playsound3 import playsound
import time

# Charger les modèles individuellement
model_feu = YOLO('/workspaces/deploy-fire-model/projet_predictions_model/feu.pt')
alert_feu = '/workspaces/deploy-fire-model/projet_predictions_model/feu.mp3'

model_smoke = YOLO('/workspaces/deploy-fire-model/projet_predictions_model/smoke.pt')
alert_smoke = '/workspaces/deploy-fire-model/projet_predictions_model/smoke.mp3'

model_accident = YOLO('/workspaces/deploy-fire-model/projet_predictions_model/accident.pt')
alert_accident = '/workspaces/deploy-fire-model/projet_predictions_model/accident.mp3'

if "camera_on" not in st.session_state:
    st.session_state["camera_on"] = False

st.title("🛑 Système de surveillance en temps réel")
st.write("Activez la caméra pour une protection optimale.")

if st.button("📷 Activer/Désactiver la caméra"):
    st.session_state["camera_on"] = not st.session_state["camera_on"]

# Affichage de l'état de la caméra
st.write("📡 **État de la caméra :**", "✅ Active" if st.session_state["camera_on"] else "❌ Désactivée")

if st.session_state["camera_on"]:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Détection de feu
        results_feu = model_feu(frame, conf =0.8 )
        for result in results_feu:
            if result.boxes:
                print("Feu détecté !")
                playsound(alert_feu)
                break

        # Détection de fumée
        results_smoke = model_smoke(frame,  conf =0.75 )
        for result in results_smoke:
            if result.boxes:
                print("Fumée détectée !")
                playsound(alert_smoke)
                break

        # Détection d'accident
        results_accident = model_accident(frame,  conf = 0.9 )
        for result in results_accident:
            if result.boxes:
                print("Accident détecté !")
                playsound(alert_accident)
                break

        stframe.image(frame, channels="BGR", use_container_width=True)

    cap.release()

else:
    st.write("🎥 **La caméra est désactivée.** Activez-la pour commencer la surveillance.")
