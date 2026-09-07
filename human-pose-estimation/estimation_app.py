# Human Pose Estimation with OpenCV and MediaPipe Hands
# Maintained by Nikunj Maheshwari (https://www.linkedin.com/in/nikunjm111/)

import os
import tempfile
import cv2
import numpy as np
from PIL import Image
import streamlit as st
import mediapipe as mp

# Set Streamlit page config
st.set_page_config(
    page_title="Human Pose Estimation",
    page_icon="🤸",
    layout="wide"
)

# Body keypoint mapping for OpenPose MobileNet model
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


@st.cache_resource
def load_pose_net():
    """Loads the pre-trained TensorFlow pose estimation model."""
    # Look for model in current directory, assets, or parent paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "graph_opt.pb"),
        os.path.join(os.path.dirname(__file__), "assets", "graph_opt.pb"),
        "graph_opt.pb"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return cv2.dnn.readNetFromTensorflow(p)
    return None


@st.cache_resource
def load_hand_detector():
    """Initializes and caches MediaPipe Hands detector."""
    mp_hands = mp.solutions.hands
    return mp_hands, mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5
    )


def process_frame(frame, threshold=0.2, detect_hands=True):
    """
    Detects body pose and hand keypoints on the input frame.
    Expects and returns an RGB image (numpy array).
    """
    if frame is None:
        return None, 0, 0

    net = load_pose_net()
    if net is None:
        st.error("Pose model 'graph_opt.pb' could not be found.")
        return frame, 0, 0

    # Work on a copy to avoid mutating the original image
    processed = frame.copy()

    # Ensure 3-channel RGB
    if len(processed.shape) == 2:  # Grayscale
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    elif processed.shape[2] == 4:  # RGBA
        processed = cv2.cvtColor(processed, cv2.COLOR_RGBA2RGB)

    frame_height, frame_width = processed.shape[:2]

    # OpenPose MobileNet expects 368x368 blob
    blob = cv2.dnn.blobFromImage(
        processed, 1.0, (368, 368),
        (127.5, 127.5, 127.5),
        swapRB=True, crop=False
    )
    net.setInput(blob)
    out = net.forward()
    out = out[:, :19, :, :]

    points = []
    body_detected_count = 0
    for i in range(len(BODY_PARTS)):
        heat_map = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heat_map)
        x = int((frame_width * point[0]) / out.shape[3])
        y = int((frame_height * point[1]) / out.shape[2])
        if conf > threshold:
            points.append((x, y))
            body_detected_count += 1
        else:
            points.append(None)

    # Draw body skeleton
    for pair in POSE_PAIRS:
        part_from = pair[0]
        part_to = pair[1]
        id_from = BODY_PARTS[part_from]
        id_to = BODY_PARTS[part_to]

        if points[id_from] and points[id_to]:
            # Skeleton line (green)
            cv2.line(processed, points[id_from], points[id_to], (34, 197, 94), 3)
            # Joints (red/blue)
            cv2.circle(processed, points[id_from], 5, (239, 68, 68), cv2.FILLED)
            cv2.circle(processed, points[id_to], 5, (239, 68, 68), cv2.FILLED)

    hands_detected_count = 0
    if detect_hands:
        mp_hands, hand_detector = load_hand_detector()
        # MediaPipe expects RGB image
        result = hand_detector.process(processed)

        if result.multi_hand_landmarks:
            hands_detected_count = len(result.multi_hand_landmarks)
            for hand_landmarks in result.multi_hand_landmarks:
                for i in range(21):
                    landmark = hand_landmarks.landmark[i]
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    # Finger joint landmark (bright blue)
                    cv2.circle(processed, (x, y), 4, (59, 130, 246), -1)

                # Connect hand landmarks
                for connection in mp_hands.HAND_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    x1 = int(hand_landmarks.landmark[start_idx].x * frame_width)
                    y1 = int(hand_landmarks.landmark[start_idx].y * frame_height)
                    x2 = int(hand_landmarks.landmark[end_idx].x * frame_width)
                    y2 = int(hand_landmarks.landmark[end_idx].y * frame_height)
                    # Hand skeleton bone (yellow/cyan)
                    cv2.line(processed, (x1, y1), (x2, y2), (234, 179, 8), 2)

    return processed, body_detected_count, hands_detected_count


# --- Streamlit UI ---
st.title("🤸 Human Pose Estimation with Hands & Fingers")
st.markdown("Real-time deep learning pose detection using **OpenCV DNN (OpenPose)** and **MediaPipe Hands**.")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.selectbox("Choose Input Mode", ["Image", "Webcam", "Video"])

confidence_val = st.sidebar.slider("Confidence Threshold", min_value=0, max_value=100, value=20, step=5)
thres = confidence_val / 100.0

detect_hands_option = st.sidebar.checkbox("Detect Hands & Fingers (MediaPipe)", value=True)

st.sidebar.markdown("---")
st.sidebar.info("Developed by **Nikunj Maheshwari**  \n[LinkedIn Profile](https://www.linkedin.com/in/nikunjm111/)")

# Check model availability early
model_net = load_pose_net()
if model_net is None:
    st.error("⚠️ Model file `graph_opt.pb` was not found. Please ensure it is present in the repository.")

# 1. IMAGE MODE
if mode == "Image":
    st.subheader("📷 Image Pose Estimation")

    # Offer demo sample or upload
    sample_options = ["Upload your own image"]
    demo_image_path = None
    for p in ["stand.jpg", "run.jpg", os.path.join("assets", "stand.jpg")]:
        if os.path.exists(p):
            sample_options.append(f"Demo: {os.path.basename(p)}")
            if demo_image_path is None:
                demo_image_path = p

    img_choice = st.radio("Select Image Source:", sample_options, horizontal=True)

    input_image = None

    if img_choice == "Upload your own image":
        uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            input_image = np.array(Image.open(uploaded_file))
    else:
        chosen_filename = img_choice.replace("Demo: ", "")
        for candidate in [chosen_filename, os.path.join("assets", chosen_filename)]:
            if os.path.exists(candidate):
                input_image = np.array(Image.open(candidate))
                break

    if input_image is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Image**")
            st.image(input_image, use_container_width=True)

        with st.spinner("Estimating pose and landmarks..."):
            result_img, body_count, hand_count = process_frame(
                input_image, threshold=thres, detect_hands=detect_hands_option
            )

        with col2:
            st.markdown("**Pose Estimation Output**")
            st.image(result_img, use_container_width=True)

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Body Keypoints Detected", f"{body_count} / {len(BODY_PARTS)}")
        col_m2.metric("Hands Detected", f"{hand_count}")

# 2. WEBCAM MODE
elif mode == "Webcam":
    st.subheader("📹 Webcam Snapshot Pose Estimation")
    st.caption("Capture a photo using your webcam (works both locally and in Streamlit Cloud).")

    camera_photo = st.camera_input("Take a photo to analyze your pose")
    if camera_photo is not None:
        webcam_img = np.array(Image.open(camera_photo))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Captured Photo**")
            st.image(webcam_img, use_container_width=True)

        with st.spinner("Analyzing pose..."):
            result_img, body_count, hand_count = process_frame(
                webcam_img, threshold=thres, detect_hands=detect_hands_option
            )

        with col2:
            st.markdown("**Pose Detection**")
            st.image(result_img, use_container_width=True)

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Body Keypoints Detected", f"{body_count} / {len(BODY_PARTS)}")
        col_m2.metric("Hands Detected", f"{hand_count}")

# 3. VIDEO MODE
elif mode == "Video":
    st.subheader("🎥 Video Pose Estimation")
    video_file = st.file_uploader("Upload a Video (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        try:
            tfile.write(video_file.read())
            tfile.close()

            cap = cv2.VideoCapture(tfile.name)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            st.write(f"Total video frames: {total_frames}")
            start_btn = st.button("Start Processing Video")

            if start_btn:
                video_placeholder = st.empty()
                progress_bar = st.progress(0)
                frame_idx = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Convert BGR (from OpenCV VideoCapture) to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    result_frame, _, _ = process_frame(
                        frame_rgb, threshold=thres, detect_hands=detect_hands_option
                    )

                    video_placeholder.image(result_frame, channels="RGB", use_container_width=True)
                    frame_idx += 1
                    if total_frames > 0:
                        progress_bar.progress(min(frame_idx / total_frames, 1.0))

                cap.release()
                st.success("Video processing completed!")
        finally:
            if os.path.exists(tfile.name):
                os.remove(tfile.name)
