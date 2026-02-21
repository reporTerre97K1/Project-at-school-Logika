class MapManager:
    def __init__(self):
        self.model = "block"  # або "models/block"
        self.texture = "block.png"  # або "models/block.png"
        self.colors = [
            (0.5, 0.5, 0.5, 1),
            (0.1, 0.9, 0.3, 1),
            (0.9, 0.6, 0.2, 1),
            (0.3, 0.3, 0.3, 1),
        ]
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        return self.colors[-1]

    def addBlock(self, position):
        block = loader.loadModel(self.model)
        if not block:
            print(f"[ERROR] Модель {self.model} не знайдена!")
            return
        tex = loader.loadTexture(self.texture)
        if not tex:
            print(f"[ERROR] Текстура {self.texture} не знайдена!")
        block.setTexture(tex)
        block.setPos(position)
        block.setColor(self.getColor(int(position[2])))
        block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        try:
            with open(filename) as file:
                y = 0
                for line in file:
                    x = 0
                    line = line.strip().split()  # важливо!
                    for z in line:
                        height = int(z)
                        for z0 in range(height + 1):
                            self.addBlock((x, y, z0))
                        x += 1
                    y += 1
        except FileNotFoundError:
            print(f"[ERROR] Файл {filename} не знайдено!")
