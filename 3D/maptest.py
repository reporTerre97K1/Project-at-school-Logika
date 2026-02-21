import random

filename = "maptest.txt"

def openfile(self, filename):
    with open(filename, 'w') as file:
        for i in range(10):
            line = ' '.join(str(random.randint(0, 5)) for _ in range(10))
            file.write(line + '\n')
openfile(None, filename)

class MapManager():
    def __init__(self):
        self.model = "block"
        self.texture = "block.png"
        self.colors = [(0.5, 0.5, 0.5, 1),
                       (0.1, 0.9, 0.3, 1),
                       (0.9, 0.6, 0.2, 1),
                       (0.3, 0.3, 0.3, 1),]

        self.startNew()

    def startNew(self):
       self.land = render.attachNewNode("Land") 

    def getColor(self, z):
       if z < len(self.colors):
           return self.colors[z]
       else:
           return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
       self.block = loader.loadModel(self.model)
       self.block.setTexture(loader.loadTexture(self.texture))
       self.block.setPos(position)
       self.color = self.getColor(int(position[2]))
       self.block.setColor(self.color)
       self.block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
       self.clear()
       with open(filename) as file:
           y = 0
           for line in file:
               x = 0
               line = line.split(' ')
               for z in line:
                   for z0 in range(int(z)+1):
                       block = self.addBlock((x, y, z0))
                   x += 1
               y += 1
