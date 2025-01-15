Human Pose Estimation Using Machine Learning
# Overview
This project implements a real-time human pose estimation system using machine learning. The system detects and visualizes human body keypoints and hand landmarks in images, videos, and live streams. Built using OpenCV, MediaPipe, and Streamlit, it provides an interactive interface for easy usage.


# Features
- Real-time pose estimation for images, videos, and live webcam streams.
- Detection and visualization of body keypoints and hand landmarks.
- Adjustable confidence threshold for pose detection.


# Installation
To run this project, follow these steps:

Clone the repository:

bash

git clone https://github.com/your-username/human-pose-estimation.git
cd human-pose-estimation
Install the required dependencies:

bash

pip install -r requirements.txt
Run the application:

bash

streamlit run estimation_app.py


# Project Structure

human-pose-estimation/  
├── assets/  
│   └── stand.jpg         # Sample demo image  
├── models/  
│   └── graph_opt.pb      # TensorFlow model file  
├── estimation_app.py     # Main application script  
├── requirements.txt      # Dependencies  
├── README.md             # Project documentation  
└── LICENSE (optional)    # License information  


# Requirements
Dependencies required for the project:

streamlit
opencv-python
mediapipe
numpy
pillow

Install them using the requirements.txt file provided.


# Future Improvements
- Integrate advanced models like MoveNet for improved accuracy.
- Optimize performance for low-resource devices.
- Add functionality for group pose detection.


# Author
Developed by Your Nikunj Maheshwari 
- https://github.com/markstone111/side_end.dev/new/main/human-pose-estimation

