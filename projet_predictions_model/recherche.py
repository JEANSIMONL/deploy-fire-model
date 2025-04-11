# import streamlit as st
# import cv2
# from ultralytics import YOLO
# from playsound3 import playsound
# import threading
# import numpy as np

# model_feu = YOLO('/home/wecode-071/Téléchargements/Fire_predictions_dataset/feu.pt')
# alert_feu = '/home/wecode-071/Téléchargements/Fire_predictions_dataset/feu.mp3'

# model_smoke = YOLO('/home/wecode-071/Téléchargements/Fire_predictions_dataset/smoke.pt')
# alert_smoke = '/home/wecode-071/Téléchargements/Fire_predictions_dataset/smoke.mp3'

# model_accident = YOLO('/home/wecode-071/Téléchargements/Fire_predictions_dataset/accident.pt')
# alert_accident = '/home/wecode-071/Téléchargements/Fire_predictions_dataset/accident.mp3'

# def play_alert(path):
#     threading.Thread(target=playsound, args=(path,), daemon=True).start()

# if "camera_on" not in st.session_state:
#     st.session_state["camera_on"] = False

# st.title("🛑 Système de surveillance en temps réel")
# st.write("Activez la caméra pour une protection optimale.")

# if st.button("📷 Activer/Désactiver la caméra"):
#     st.session_state["camera_on"] = not st.session_state["camera_on"]

# st.write("📡 **État de la caméra :**", "✅ Active" if st.session_state["camera_on"] else "❌ Désactivée")

# uploaded_image = st.file_uploader("Télécharger une image pour la détection d'accident", type=["jpg", "jpeg", "png"])

# if uploaded_image is not None:
#     image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
    
#     st.image(image, channels="BGR", caption="Image téléchargée pour la détection d'accident", use_column_width=True)

#     results_accident = model_accident(image, conf=0.85)

#     if results_accident:
#         for result in results_accident:
#             if result.boxes:
#                 print("Accident détecté !")
#                 play_alert(alert_accident)
#                 break
    
#     annotated_image = results_accident[0].plot()
#     st.image(annotated_image, caption="Image avec détection d'accident", use_column_width=True)

# if st.session_state["camera_on"]:
#     cap = cv2.VideoCapture(0)
#     stframe = st.empty()

#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break
        
#         # Détection de feu
#         results_feu = model_feu(frame, conf=0.8)
#         if any(result.boxes for result in results_feu):
#             print("Feu détecté !")
#             play_alert(alert_feu)

#         # Détection de fumée
#         results_smoke = model_smoke(frame, conf=0.8)
#         if any(result.boxes for result in results_smoke):
#             print("Fumée détectée !")
#             play_alert(alert_smoke)


#         stframe.image(frame, channels="BGR", use_container_width=True)

#     cap.release()

# else:
#     st.write("🎥 **La caméra est désactivée.** Activez-la pour commencer la surveillance.")
