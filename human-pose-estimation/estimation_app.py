# Hello side-end-devs, use and try the below code and please contribute to it according to your ideas and let me know on linkedin https://www.linkedin.com/in/nikunjm111/ , thanks.

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import mediapipe as mp

#Constants
BODY_PARTS = {
    "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
    "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
    "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
    "LEye": 15, "REar": 16, "LEar": 17, "Background": 18
}

POSE_PAIRS = [
    ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
    ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"],
    ["Neck", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"],
    ["Neck", "Nose"], ["Nose", "REye"], ["REye", "REar"],
    ["Nose", "LEye"], ["LEye", "LEar"]
]

# Load the model
net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")

# Initialize MediaPipe for hand landmarks
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Streamlit App
st.title("Real-Time Human Pose Estimation with Hands and Fingers")
mode = st.sidebar.selectbox("Choose Mode", ["Image", "Webcam", "Video"])
thres = st.sidebar.slider("Detection Confidence Threshold", 0, 100, 50, 5) / 100

@st.cache_data
def process_frame(frame):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    # Process body pose estimation
    net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]

    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatMap)
        x = int((frameWidth * point[0]) / out.shape[3])
        y = int((frameHeight * point[1]) / out.shape[2])
        points.append((x, y) if conf > thres else None)

    # draw the pose skeleon
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv2.ellipse(frame, points[idFrom], (5, 5), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            cv2.ellipse(frame, points[idTo], (5, 5), 0, 0, 360, (0, 0, 255), cv2.FILLED)

    # Process hand landmarks using MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for i in range(21):
                landmark = hand_landmarks.landmark[i]
                x = int(landmark.x * frameWidth)
                y = int(landmark.y * frameHeight)
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)  # Draw the finger landmarks

            # Optionally, connect the hand landmarks to form the hand skeleton
            for connection in mp_hands.HAND_CONNECTIONS:
                start = connection[0]
                end = connection[1]
                x1, y1 = int(hand_landmarks.landmark[start].x * frameWidth), int(hand_landmarks.landmark[start].y * frameHeight)
                x2, y2 = int(hand_landmarks.landmark[end].x * frameWidth), int(hand_landmarks.landmark[end].y * frameHeight)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)  # Connect finger landmarks

    return frame

if mode == "Image":
    img_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if img_file:
        img = np.array(Image.open(img_file))
        st.image(img, caption="Uploaded Image", use_container_width=True)
        result_img = process_frame(img)
        st.image(result_img, caption="Pose Estimation with Fingers", use_container_width=True)

elif mode == "Webcam":
    st.write("Turn on your webcam for real-time pose and finger detection.")
    run = st.button("Start Webcam")
    if run:
        placeholder = st.empty()
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to access the webcam.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result_frame = process_frame(frame)
            placeholder.image(result_frame, channels="RGB", use_container_width=True)

        cap.release()

elif mode == "Video":
    video_file = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        cap = cv2.VideoCapture(tfile.name)

        placeholder = st.empty()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result_frame = process_frame(frame)
            placeholder.image(result_frame, channels="RGB", use_container_width=True)

        cap.release()
        os.remove(tfile.name)

st.sidebar.markdown("---")
# change the name below
st.sidebar.info("This Poject is created by nikunj and is under progress")


