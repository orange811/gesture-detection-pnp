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
                    lmList.append([id, cx, cy])#,lm.z])
                mp_draw.draw_landmarks(image, myHand, mp_hand.HAND_CONNECTIONS)
            
        # Count the fingers based on the landmark positions
        fingers = []
        if len(lmList):
            for offset in range(0,len(lmList),21):
                xPositions = [lmList[p][1] for p in range(offset, offset + 21)]
                yPositions = [lmList[p][2] for p in range(offset, offset + 21)]
                #print(lmList[tipIds[0]+offset][3]-lmList[tipIds[4]+offset][3])
                x0=min(xPositions)
                x1 = max(xPositions)
                #zDiff = lmList[xPositions.index(x0)][3]-lmList[xPositions.index(x1)][3]
                y0=min(yPositions)
                y1 = max(yPositions)
                rightHand = (lmList[tipIds[0]+offset][1]>lmList[tipIds[4]+offset][1])
                if not((lmList[tipIds[0]+offset][1] > lmList[tipIds[0] - 1+offset][1]) ^ (rightHand)):
                        fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList[tipIds[id]+offset][2] < lmList[tipIds[id] - 2+offset][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                cv2.rectangle(image, (x0, y0), (x1, y1), (255, 0,0), 1)
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
cnt.endProgram()
cv2.destroyAllWindows()
