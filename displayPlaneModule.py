import cv2
import numpy as np


class displayPlane():
    def __init__(self):
        self.cornersPosition = [[], [], [], [], []]

    def drowMarkers(self, img, corners):
        for marker in corners:
            for pos in marker:
                for dot in pos:
                    x = int(dot[0])
                    y = int(dot[1])
                    cv2.circle(img, (x, y), 5, (255, 0, 255), cv2.FILLED)

    def setPositions(self, corners, ids):
        iterator = 0
        for marker in corners:
            id = int(ids[iterator] % 70)
            x = int(marker[0][0][0])
            y = int(marker[0][0][1])
            if len(self.cornersPosition[id]) != 0:
                if abs(self.cornersPosition[id][0] - x) <= 10:
                    x = self.cornersPosition[id][0]
                if abs(self.cornersPosition[id][1] - y) <= 10:
                    y = self.cornersPosition[id][1]
            self.cornersPosition[id] = [x, y]
            iterator += 1

    def drowArea(self, img):
        position = []
        for dot in self.cornersPosition:
            if len(dot) != 0:
                position.append(dot)
        position = np.array(position, np.int32)
        cv2.polylines(img, [position], True, (255, 0, 0))

    def getNotEmptyPositions(self):
        positions = []
        for dot in self.cornersPosition:
            if len(dot) != 0:
                positions.append(dot)
        return positions

    def gomografy(self, img):
        self.outPoints = np.float32([[0,0],[960, 0],[960,540], [0,540]])
        currentPoints = np.float32([self.cornersPosition[2], self.cornersPosition[3], self.cornersPosition[4],
                                    self.cornersPosition[1]])
        self.marix = cv2.getPerspectiveTransform(currentPoints, self.outPoints)
        img2 = cv2.warpPerspective(img, self.marix, (img.shape[1], img.shape[0]))
        return img2

    def getTranspoint(self, img, x, y):
        point = np.float32([[x, y]])
        secondPoint = cv2.perspectiveTransform(point[None, :, :], self.marix)
        cv2.circle(img, (int(secondPoint[0][0][0]), int(secondPoint[0][0][1])), 5, (255, 0, 255), cv2.FILLED)
        return [int(secondPoint[0][0][0]), int(secondPoint[0][0][1])]


    def test(self,point):
        a = self.isUpper([self.cornersPosition[1], self.cornersPosition[4]], point)
        b = self.isUpper([self.cornersPosition[2], self.cornersPosition[3]], point)
        c = self.isUpper([self.swap(self.cornersPosition[3]), self.swap(self.cornersPosition[4])], self.swap(point))
        d = self.isUpper([self.swap(self.cornersPosition[1]), self.swap(self.cornersPosition[2])], self.swap(point))
        if a == False and c == False and d == False and b == True:
            return True
        return False

    def isUpper(self, linePoints, point):
        line = self.getVector(linePoints[0], linePoints[1])

        helpVector = self.getVector(linePoints[0], point)
        skewProduct = self.skewProduct(line, helpVector)
        if skewProduct < 0:
            return False
        return True

    def getVector(self, firstPoint, secondPoint):
        return [secondPoint[0] - firstPoint[0], secondPoint[1] - firstPoint[1]]

    def skewProduct(self, firstVector, secondVector):
        return firstVector[0] * secondVector[1] - firstVector[1] * secondVector[0]

    def swap(self, arr):
        return [arr[1], arr[0]]
