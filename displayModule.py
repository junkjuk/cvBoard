import mousePositionModule as mpm
import math
class display():
    def __init__(self, width=1920, height=1080, startX=0, startY=0):
        self.width = width
        self.height = height
        self.startX = startX
        self.startY = startY
        self.deltX = int(self.width * 0.01)
        self.deltY = int(self.height * 0.01)
        self.mouse = mpm.mousePosition()

    def moveMouse(self, x, y):
        delX = x * self.width - self.mouse.getX
        delY = y * self.height - self.mouse.getY
        delX = (1 - self.gouseFunc(delX, 0.01)) * delX
        delY = (1 - self.gouseFunc(delY, 0.01)) * delY
        self.mouse.setX(self.mouse.getX + delX)
        self.mouse.setY(self.mouse.getY + delY)
        # if abs(self.mouse.getX - self.width*x) >= self.deltX:
        #     self.mouse.setX(self.width*x)
        # if abs(self.mouse.getY - self.height*y) >= self.deltY:
        #     self.mouse.setY(self.height*y)
        self.mouse.move()

    def gouseFunc(self, x, k=1):
        fn = -1 * k * x * x
        res = math.exp(fn)
        return res

