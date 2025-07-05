import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import av

st.title("OpenCV detect color")

hue = st.slider("Hue", 0, 359, 120, 1)

def video_callback(frame: av.VideoFrame) -> av.VideoFrame:
    # Convert the av.VideoFrame object to a bunch of pixels, a format that cv2 understands
    img = frame.to_ndarray(format="bgr24")
    
    # Define the lower and upper range for the color green in HSV
    central_hue = hue
    sensitivity = 50
    lower_green = np.array([(central_hue - sensitivity) / 2, 50, 50])   # Lower bound of green in HSV
    upper_green = np.array([(central_hue + sensitivity) / 2, 255, 255])  # Upper bound of green in HSV
    
    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create a mask that captures the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Bitwise-AND the mask and original frame to isolate the green regions
    result = cv2.bitwise_and(img, img, mask=mask)

    return av.VideoFrame.from_ndarray(result, format="bgr24")
   

webrtc_streamer(key="streamer", sendback_audio=False, video_frame_callback=video_callback)
