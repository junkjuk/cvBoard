import mousePositionModule as mpm

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
        if abs(self.mouse.getX - self.width*x) >= self.deltX:
            self.mouse.setX(self.width*x)
        if abs(self.mouse.getY - self.height*y) >= self.deltY:
            self.mouse.setY(self.height*y)
        # print("get points")
        print(y)
        print(self.height*y)
        # print(self.width, self.height)
        # print(self.mouse.getX, self.mouse.getY)
        self.mouse.move()

