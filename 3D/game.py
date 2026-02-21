from direct.showbase.ShowBase import ShowBase
from mapmanager import MapManager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = MapManager()
        self.land.loadLand("land2.txt")
        base.camLens.setFov(90)
        self.hero = Hero((0, 0, 1), self.land.land)

game = Game() 
game.run()