import tkinter as tk
from tkinter import SOLID
from PIL import Image, ImageTk
import cv2
import mediapipe as mp

# Initialize the main window
win = tk.Tk()
win.title('Sign Language Detection')
width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.geometry(f"{width}x{height}")
win.configure(bg="#FFFFF7")

# Declare global variables
global cap, label1, mpDraw, mpHands, hands, upCount

cap = None

# Create and pack the welcome label
welcome_label = tk.Label(
    win,
    text='Welcome to the Sign Language Application',
    font=('Helvetica', 18, 'italic'),
    bd=5,
    bg='orange',
    fg='white',
    relief=SOLID,
    width=200
)
welcome_label.pack(pady=15, padx=300)

# Create and pack the "Start Camera" button
def start_camera():
    initialize_video()
    detect_gesture()

start_button = tk.Button(
    win,
    text="Start Camera",
    font=('Helvetica', 16),
    bg='blue',
    fg='white',
    command=start_camera
)
start_button.pack(pady=15)

def initialize_video():
    global cap, mpDraw, mpHands, hands, label1, upCount

    # Define constants
    w, h = 500, 400

    # Release any previous video capture if it exists
    if cap:
        cap.release()

    # Create a Label widget for displaying the video feed
    label1 = tk.Label(win, width=w, height=h, bg="#FFFFF7")
    label1.place(x=40, y=200)

    # Initialize MediaPipe Hands module
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # Start video capture
    cap = cv2.VideoCapture(0)

    # Set up the text variable for displaying gesture recognition results
    upCount = tk.StringVar()
    status = tk.Label(win, textvariable=upCount, font=('Helvetica', 18, 'bold'), bd=5, bg='gray', width=50,
                      fg='#232224', relief=tk.GROOVE)
    status.place(x=400, y=700)
    crr = tk.Label(win, text='Current:', font=('Helvetica', 18, 'bold'), bd=5, bg='gray', width=15, fg='#232224',
                   relief=tk.GROOVE)
    crr.place(x=120, y=700)

def detect_gesture():
    global cap, mpDraw, mpHands, hands, label1, upCount

    # Capture frame from video
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        return

    # Resize and convert frame to RGB
    img = cv2.resize(img, (500, 400))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Hands
    results = hands.process(rgb)

    cshow = ''

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            lm_list = [lm for lm in hand.landmark]
            finger_tips = [8, 12, 16, 20]
            thumb_tip = 4
            finger_fold_status = []

            # Check finger fold status
            for tip in finger_tips:
                if lm_list[tip].x < lm_list[tip - 2].x:
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

            # Gesture recognition
            if all(finger_fold_status):  # Check if all fingers are folded
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y:
                    cshow = 'I Like it'
                elif lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
                    cshow = 'I don\'t like it'
            else:
                if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < lm_list[5].x:
                    cshow = 'STOP ! Don\'t move.'
                elif lm_list[4].y < lm_list[2].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < lm_list[5].x:
                    cshow = 'Perfect, You did a great job.'
                elif lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < lm_list[5].x:
                    cshow = 'Good to see you.'
                elif lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cshow = 'You Come here.'
                elif lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cshow = 'Yes, we won.'
                elif lm_list[4].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                        lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                    cshow = 'Move Left'
                elif lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                        lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                    cshow = 'Move Right'

            # Draw landmarks and text on the image
            mpDraw.draw_landmarks(rgb, hand, mpHands.HAND_CONNECTIONS)
            cv2.putText(rgb, cshow, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 255), 2)

            # Convert image for Tkinter
            image = Image.fromarray(rgb)
            finalImage = ImageTk.PhotoImage(image)
            label1.configure(image=finalImage)
            label1.image = finalImage

    # Repeat detect_gesture function to create continuous video feed
    win.after(1, detect_gesture)

# Start the Tkinter main loop
win.mainloop()
