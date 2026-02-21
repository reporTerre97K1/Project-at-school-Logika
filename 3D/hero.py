class Hero:
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)

        self.cameraBind()
        self.cameraOn = True
        self.accept_events()
        self.mode = True

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 1, 1)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def accept_events(self):
        base.accept('n', self.turn_left)
        base.accept('n-repeat', self.turn_left)
        base.accept('c', self.changeView) 
        base.accept('w', self.forward)
        base.accept('s', self.back)
        base.accept('a', self.left)
        base.accept('d', self.right)
        base.accept('c-repeat', self.changeView) 
        base.accept('w-repeat', self.forward)
        base.accept('s-repeat', self.back)
        base.accept('a-repeat', self.left)
        base.accept('d-repeat', self.right)
        base.accept('arrow_up', self.go_up)
        base.accept('arrow_up-repeat', self.go_up)  

        #камера вниз
        base.accept('arrow_down', self.go_down)
        base.accept('arrow_down-repeat', self.go_down)
        
        #камера вліво
        base.accept('arrow_left', self.go_left)
        base.accept('arrow_left-repeat', self.go_left)  

        #камера вправо
        base.accept('arrow_right', self.go_right)
        base.accept('arrow_right-repeat', self.go_right)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        self.move_to(angle)

    def move_to(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        angle = angle % 360
        if 0 <= angle < 45:
            return 0, -1
        elif 45 <= angle < 135:
            return 1, 0
        elif 135 <= angle < 225:
            return 0, 1
        elif 225 <= angle < 315:
            return -1, 0
        else:
            return 0, -1

    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() - 90) % 360
        self.move_to(angle)
        
    def go_up(self):
        self.hero.setP(self.hero.getP() + 2)

    def go_down(self):
        self.hero.setP(self.hero.getP() - 2)

    def go_left(self):
        self.hero.setH(self.hero.getH() + 2)

    def go_right(self):
        self.hero.setH(self.hero.getH() - 2)
        
        