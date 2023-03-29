import cv2
import mediapipe as mp
import time
import controller as cnt

# Initialize the video capture
video = cv2.VideoCapture(0)

# Wait for 2 seconds for the camera to warm up
time.sleep(2.0)

# Define the hand landmarks to track
tipIds = [4, 8, 12, 16, 20]

# Initialize the hand tracking module from MediaPipe
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# Initialize the LED controller
cnt.led(0)

# Main loop for hand tracking and finger counting
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        # Capture a frame from the camera
        ret, image = video.read()
        if not ret:
            break
        
        # Convert the image to RGB format for processing
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the hand landmarks using MediaPipe
        results = hands.process(image)
        
        # Convert the image back to BGR format for display
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Collect the landmark positions for finger counting
        lmList = []
        if results.multi_hand_landmarks:
            for myHand in results.multi_hand_landmarks: 
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, myHand, mp_hand.HAND_CONNECTIONS)
            
        # Count the fingers based on the landmark positions
        fingers = []
        if len(lmList) != 0:
            for offset in range(0,len(lmList),21):
                rightHand = (lmList[tipIds[0]][1]+offset>lmList[tipIds[4]][1]+offset)
                if not((lmList[tipIds[0]][1]+offset > lmList[tipIds[0] - 1][1]+offset) ^ (rightHand)):
                        fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList[tipIds[id]][2]+offset < lmList[tipIds[id] - 2][2]+offset:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            total = fingers.count(1)
            cnt.led(total)
            
            # Display the finger count on the screen
            cv2.rectangle(image, (20, 300), (110, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, str(total), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 5)
            #cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 5)
        
        # Display the image with finger count on the screen
        cv2.imshow("Frame", image)
        
        # Check if the user wants to quit
        if cv2.waitKey(1) == ord('q'):
            break

# Release the video capture, exit the LED controller, and close all windows
video.release()
cnt.led(-1)
cnt.board.exit()
cv2.destroyAllWindows()
