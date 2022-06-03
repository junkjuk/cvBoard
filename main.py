import cv2
import mediapipe as mp
import time
import mouse
import screeninfo
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0
cursor = htm.mousePosition(0, 0)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    # print(mouse.get_position())
    if len(lmList) != 0:
        print(lmList[8])
        cursor.move(lmList[8][1], lmList[8][2])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)