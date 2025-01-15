# import streamlit as st

# from PIL import Image
# import numpy as np
# import cv2

# DEMO_IMAGE = 'stand.jpg'

# BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
#                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
#                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
#                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

# POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
#                ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
#                ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
#                ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
#                ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]


# width = 368
# height = 368
# inWidth = width
# inHeight = height

# net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")




# st.title("Human Pose Estimation OpenCV")

# st.text('Make Sure you have a clear image with all the parts clearly visible')

# img_file_buffer = st.file_uploader("Upload an image, Make sure you have a clear image", type=[ "jpg", "jpeg",'png'])

# if img_file_buffer is not None:
#     image = np.array(Image.open(img_file_buffer))

# else:
#     demo_image = DEMO_IMAGE
#     image = np.array(Image.open(demo_image))
    
# st.subheader('Original Image')
# st.image(
#     image, caption=f"Original Image", use_container_width=True
# ) 

# thres = st.slider('Threshold for detecting the key points',min_value = 0,value = 20, max_value = 100,step = 5)

# thres = thres/100

# @st.cache_data
# def poseDetector(frame):
#     frameWidth = frame.shape[1]
#     frameHeight = frame.shape[0]
    
#     net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    
#     out = net.forward()
#     out = out[:, :19, :, :]
    
#     assert(len(BODY_PARTS) == out.shape[1])
    
#     points = []
#     for i in range(len(BODY_PARTS)):
#         # Slice heatmap of corresponging body's part.
#         heatMap = out[0, i, :, :]

#         _, conf, _, point = cv2.minMaxLoc(heatMap)
#         x = (frameWidth * point[0]) / out.shape[3]
#         y = (frameHeight * point[1]) / out.shape[2]
#         points.append((int(x), int(y)) if conf > thres else None)
        
        
#     for pair in POSE_PAIRS:
#         partFrom = pair[0]
#         partTo = pair[1]
#         assert(partFrom in BODY_PARTS)
#         assert(partTo in BODY_PARTS)

#         idFrom = BODY_PARTS[partFrom]
#         idTo = BODY_PARTS[partTo]

#         if points[idFrom] and points[idTo]:
#             cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
#             cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
#             cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            
            
#     t, _ = net.getPerfProfile()
    
#     return frame


# output = poseDetector(image)


# st.subheader('Positions Estimated')
# st.image(
#        output, caption=f"Positions Estimated", use_container_width=True)
    
# st.markdown('''
#             # 
             
#             ''')



import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import mediapipe as mp

# Constants
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

# Load the pose estimation model
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

    # Draw the pose skeleton
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
st.sidebar.info("This Poject is created by Nikunj and is under progress")
