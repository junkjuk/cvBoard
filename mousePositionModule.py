import displayModule
import mouse


class mousePosition():
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def move(self):
        mouse.move(self.x, self.y)

    def moveTo(self, x, y):
        self.x = x
        self.y = y
        mouse.move(self.x, self.y)

    @property
    def getX(self):
        return self.x

    @property
    def getY(self):
        return self.y

    def setX(self, newX):
        self.x = int(newX)

    def setY(self, newY):
        self.y = int(newY)

