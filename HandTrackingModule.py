import cv2
import mediapipe as mp
import time
import mouse
import numpy as np
import screeninfo
import displayModule
import displayPlaneModule
import mousePositionModule

class handDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.maxHands = max_num_hands
        self.complexity = model_complexity
        self.detectionCon = min_detection_confidence
        self.trackCon = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.complexity, self.detectionCon, 0.9)
        # self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, lm.x, lm.y])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,1000)
    cap.set(4,1000)
    pTime = 0
    cTime = 0

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoParams = cv2.aruco.DetectorParameters_create()
    plane = displayPlaneModule.displayPlane()
    display = displayModule.display()
    detector = handDetector()

    while True:
        success, img = cap.read()

        (corners, ids, rejected) = cv2.aruco.detectMarkers(img, dictionary, parameters=arucoParams)

        plane.drowMarkers(img, corners)
        plane.setPositions(corners, ids)
        plane.drowArea(img)

        cv2.aruco.drawDetectedMarkers(img, corners)
        img = detector.findHands(img, False)
        lmList = detector.findPosition(img, 0, False)
        # if len(lmList) != 0:
        #     h, w, c = img.shape
        #     cx, cy = int(lmList[8][1] * w), int(lmList[8][2] * h)
        #     cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            # print(plane.test([cx, cy]))
            # display.moveMouse(lmList[8][1], lmList[8][2])
        cv2.imshow("Image2", img)
        cv2.waitKey(1)
        if len(lmList) != 0:
            h, w, c = img.shape
            cx, cy = int(lmList[8][1] * w), int(lmList[8][2] * h)
            if plane.test([cx, cy]):
                img = plane.gomografy(img)
                finger = plane.getTranspoint(img, cx, cy)
                display.moveMouse(finger[0]/w, finger[1]/h)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()