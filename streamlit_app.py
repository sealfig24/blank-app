import streamlit as st
import cv2
import numpy as np

enabled = st.checkbox("Enable camera")
flip_image = st.checkbox("Flip image", True)
img_file_buffer = st.camera_input("Take a picture", disabled=not enabled)

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if flip_image:
        # Flip image and reassign variable to this new image
        cv2_img = cv2.flip(cv2_img, 1)
    
    color_converted = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Show the converted image
    st.image(color_converted)