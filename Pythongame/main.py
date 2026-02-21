import pygame
import random
import time

pygame.init()

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

speed = 5
pygame.mixer.init()

#jump_sound = pygame.mixer.Sound("phaseJump2.mp3")
running_sound = pygame.mixer.Sound("Pythongame\8a03cf93c00abc6.mp3")

def load_record_time():
    try:
        with open("timer.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def load_record():
    try:
        with open("record.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_record_time(timer):
    with open("timer.txt", "w") as file:
        file.write(str(timer))

def save_record(score):
    with open("record.txt", "w") as file:
        file.write(str(score))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, w, h):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bird(GameSprite):
    def __init__(self, x, y, w, h):
        super().__init__("Bird1.png", x, y, w, h)

    def move(self):
        self.rect.x -= speed
        if self.rect.x < 0:
            self.kill()

class Dino(GameSprite):
    def __init__(self, x, y, w, h):
        super().__init__("dino-removebg-preview.png", x, y, w, h)
        self.stand_image = pygame.transform.scale(pygame.image.load("dino-removebg-preview.png"), (w, h))
        self.sit_image = pygame.transform.scale(pygame.image.load("DinoDuck1.png"), (w, h))
        self.jump = False
        self.jump_count = 10
        self.initial_y = y
        self.is_running = False
        self.is_sitting = False 

    def sit_dino(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            if not self.is_sitting:
                self.is_sitting = True
                self.image = self.sit_image  
                self.rect.y = self.initial_y + 20 
        else:
            if self.is_sitting:
                self.is_sitting = False
                self.image = self.stand_image  
                self.rect.y = self.initial_y

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT] or keys[pygame.K_UP]) or keys[pygame.K_RSHIFT] and not self.jump:
            self.jump = True
            #jump_sound.play()

        if keys[pygame.K_RIGHT]:
            self.is_running = True
        else:
            self.is_running = False

        self.sit_dino()

        if self.jump:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10
                self.rect.y = self.initial_y
        #Трошки багованний звук
        #if self.is_running:
        #    if not running_sound.get_num_channels():
        #        running_sound.play(-1)
        #else:
        #    running_sound.stop()
        #Трошки багованний звук

class Obstacle(GameSprite):
    def __init__(self, x, y, w, h):
        super().__init__("images-removebg-preview.png", x, y, w, h)

    def move(self):
        self.rect.x -= speed
        if self.rect.x < 0:
            self.kill()

class Game:
    def __init__(self):
        self.dino = Dino(50, screen_height - 60, 50, 50)
        self.all_sprites = pygame.sprite.Group(self.dino)
        self.obstacles = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.score = 0
        self.record = load_record()
        self.best_time = load_record_time()
        self.start_time = time.time()
        self.lives = 3 
        self.font = pygame.font.SysFont("Arial", 30)
        self.spawn_delay = 30
        self.spawn_timer = 0

    def draw_text(self, text, pos, color=BLACK):
        rendered_text = self.font.render(text, True, color)
        screen.blit(rendered_text, pos)

    def draw_score(self):
        self.draw_text(f"Score: {self.score}", (10, 10))

    def draw_record(self):
        self.draw_text(f"Record: {self.record}", (10, 40))

    def draw_lives(self):
        self.draw_text(f"Lives: {self.lives}", (screen_width - 120, 10), RED)

    def draw_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.draw_text(f"Time: {elapsed_time}s", (10, 70))

    def spawn_obstacle_or_bird(self):
        if random.choice([True, False]):
            y_pos = screen_height - 50
            x_pos = screen_width + random.randint(200, 300)
            new_obstacle = Obstacle(x_pos, y_pos, 20, 40)
            if not any(abs(obstacle.rect.x - new_obstacle.rect.x) < 100 for obstacle in self.obstacles) and not any(abs(bird.rect.x - new_obstacle.rect.x) < 100 for bird in self.birds):
                self.all_sprites.add(new_obstacle)
                self.obstacles.add(new_obstacle)
        else:
            y_pos = screen_height - 100
            x_pos = screen_width + random.randint(200, 300)
            new_bird = Bird(x_pos, y_pos, 40, 40)
            if not any(abs(bird.rect.x - new_bird.rect.x) < 100 for bird in self.birds) and not any(abs(obstacle.rect.x - new_bird.rect.x) < 100 for obstacle in self.obstacles):
                self.all_sprites.add(new_bird)
                self.birds.add(new_bird)

    def increase_speed(self):
        global speed
        if self.score % 100 == 0:
            speed += 1

    def check_collision(self):
        return pygame.sprite.spritecollideany(self.dino, self.obstacles) or pygame.sprite.spritecollideany(self.dino, self.birds)

    def run(self):
        run_game = True
        while run_game:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False

            self.dino.move()

            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_obstacle_or_bird()
                self.spawn_timer = 0

            for obstacle in self.obstacles:
                obstacle.move()

            for bird in self.birds:
                bird.move()

            if self.check_collision():
                self.lives -= 1
                if self.lives <= 0:
                    if self.score > self.record:
                        save_record(self.score)
                    elapsed_time = int(time.time() - self.start_time)
                    if elapsed_time > self.best_time:
                        save_record_time(elapsed_time)
                    self.game_over()
                    run_game = False

            self.increase_speed()

            self.all_sprites.draw(screen)
            self.draw_score()
            self.draw_record()
            self.draw_lives()
            self.draw_timer()

            self.score += 1

            pygame.display.update()
            pygame.time.delay(25)

        pygame.quit()

    def game_over(self):
        screen.fill(WHITE)
        self.draw_text("Game Over!", (screen_width // 2 - 80, screen_height // 2 - 50), RED)
        self.draw_text(f"Final Score: {self.score}", (screen_width // 2 - 80, screen_height // 2))
        elapsed_time = int(time.time() - self.start_time)
        self.draw_text(f"Survived Time: {elapsed_time}s", (screen_width // 2 - 100, screen_height // 2 + 40))
        pygame.display.update()
        pygame.time.wait(3000)

game = Game()
game.run()
