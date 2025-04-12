import streamlit as st
import cv2
from ultralytics import YOLO
from playsound3 import playsound
import threading

model_feu = YOLO('/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/feu.pt')
model_fumee = YOLO('/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/smoke.pt')
model_accident = YOLO('/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/accident.pt')

alert_feu = '/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/feu.mp3'
alert_fumee = '/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/smoke.mp3'
alert_accident = '/home/wecode-071/Rendu/C-DAT-900-ABJ-2-2-ecp-simon.lokoklounon/projet_predictions_model/accident.mp3'

st.title("🛑 Système de Surveillance Intelligent")
st.write("Choisissez le mode de détection souhaité, puis activez la caméra.")

mode = st.radio("🎯 Mode de surveillance", ["🔥 Feu + Fumée", "💥 Accident"])

if "camera_on" not in st.session_state:
    st.session_state["camera_on"] = False

if st.button("📷 Activer/Désactiver la caméra"):
    st.session_state["camera_on"] = not st.session_state["camera_on"]

st.write("📡 Caméra :", "✅ Active" if st.session_state["camera_on"] else "❌ Désactivée")

if st.session_state["camera_on"]:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Erreur : impossible d'accéder à la caméra.")
            break

        if mode == "🔥 Feu + Fumée":
            # Détection de feu
            results_feu = model_feu(frame, conf=0.8)
            if results_feu and results_feu[0].boxes:
                st.warning("🔥 Feu détecté !")
                threading.Thread(target=playsound, args=(alert_feu,), daemon=True).start()

            # Détection de fumée
            results_fumee = model_fumee(frame, conf=0.8)
            if results_fumee and results_fumee[0].boxes:
                st.warning("💨 Fumée détectée !")
                threading.Thread(target=playsound, args=(alert_fumee,), daemon=True).start()

        elif mode == "💥 Accident":
            # Détection d'accident
            results_accident = model_accident(frame, conf=0.9)
            if results_accident and results_accident[0].boxes:
                st.error("💥 Accident détecté !")
                threading.Thread(target=playsound, args=(alert_accident,), daemon=True).start()

        stframe.image(frame, channels="BGR", use_container_width=True)

    cap.release()
else:
    st.info("🎥 La caméra est désactivée. Cliquez sur le bouton ci-dessus pour la lancer.")
