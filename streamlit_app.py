import streamlit as st
import cv2
import numpy as np

st.title("🎈 My new app")
st.write(
    "let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

st.write(
    '''
test
    '''
)

# Initialize the webcam (0 is the default camera)
cap = st.camera_input("Take a picture")

# Define the lower and upper range for the color green in HSV
central_hue = 120
sensitivity = 50
lower_green = np.array([(central_hue - sensitivity) / 2, 50, 50])   # Lower bound of green in HSV
upper_green = np.array([(central_hue + sensitivity) / 2, 255, 255])  # Upper bound of green in HSV

while True:
    if not cap:
        continue
    # Capture frame-by-frame
    ret, frame = cap.getvalue()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask that captures the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Bitwise-AND the mask and original frame to isolate the green regions
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Display the original frame and the result (masked green areas)
    cv2.imshow('Original', cv2.flip(frame, 1))
    cv2.imshow('Green Detection', cv2.flip(result, 1))
    
    # Exit the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
# cv2.destroyAllWindows()
