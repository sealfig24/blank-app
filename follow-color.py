import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import av

st.title("OpenCV detect color")

hue = st.slider("Hue", 0, 359, 120, 1)

# List to store the centers of detected green objects
centers = []

def video_callback(frame: av.VideoFrame) -> av.VideoFrame:
    # Conver the av.VideoFrame object to a bunch of pixels, a format that cv2 understands
    img = frame.to_ndarray(format="bgr24")
    img = cv2.flip(img, 1)
    
    # Define the lower and upper range for the color green in HSV
    central_hue = hue
    sensitivity = 50
    lower_green = np.array([(central_hue - sensitivity) / 2, 50, 50])   # Lower bound of green in HSV
    upper_green = np.array([(central_hue + sensitivity) / 2, 255, 255])  # Upper bound of green in HSV
    
    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create a mask that captures the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignore small contours (noise)
            # Get the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            # Calculate the center of the bounding box
            center = (x + w // 2, y + h // 2)
            
            # Append the center to the list
            centers.append(center)

    # Draw lines connecting the centers of the green objects
    if len(centers) > 1:
        for i in range(1, len(centers)):
            hsv_value = np.array([central_hue / 2, 100, 100], dtype=np.uint8)
            bgr_value = tuple([int(c) for c in cv2.cvtColor(np.reshape(hsv_value, (1, 1, 3)), cv2.COLOR_HSV2BGR)[0][0]])
            line_color = (0, 255, 0) # (int(.93 * 255), 255, 0) # TODO: Change the color of the marker. Blue is (255, 0, 0). Green is (0, 255, 0). You can use target hue with bgr_value.
            cv2.line(img, centers[i - 1], centers[i], line_color, 2)

    # Draw the current center as a small circle
    if centers:
        cv2.circle(img, centers[-1], 5, (0, 0, 255), -1)  # Red dot for the current center

    return av.VideoFrame.from_ndarray(img, format="bgr24")
   

webrtc_streamer(key="streamer", sendback_audio=False, video_frame_callback=video_callback)
