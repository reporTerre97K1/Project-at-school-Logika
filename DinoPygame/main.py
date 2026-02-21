import pygame
import random

pygame.init()

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

speed = 5

pygame.mixer.init()

jump_sound = pygame.mixer.Sound("phaseJump2.mp3")
running_sound = pygame.mixer.Sound("8a03cf93c00abc6.mp3")

def load_record():
    try:
        with open("record.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

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

class Dino(GameSprite):
    def __init__(self, x, y, w, h):
        super().__init__("dino-removebg-preview.png ", x, y, w, h)
        self.velocity = 10
        self.jump = False
        self.jump_count = 10
        self.initial_y = y
        self.is_running = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jump:
            self.jump = True
            jump_sound.play()
        if keys[pygame.K_RIGHT]:
            self.is_running = True
        else:
            self.is_running = False

        if self.jump:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10
                self.rect.y = self.initial_y

        if self.is_running:
            if not pygame.mixer.get_busy():
                running_sound.play(-1)
        else:
            running_sound.stop()

class Obstacle(GameSprite):
    def __init__(self, x, y, w, h):
        super().__init__("images-removebg-preview.png", x, y, w, h)

    def move(self):
        self.rect.x -= speed
        if self.rect.x < 0:
            self.rect.x = screen_width + random.randint(50, 200)
            self.rect.y = screen_height - 50

class Game:
    def __init__(self):
        self.dino = Dino(50, screen_height - 60, 50, 50)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.dino)
        self.obstacles = pygame.sprite.Group()
        self.score = 0
        self.record = load_record()
        self.spawn_delay = 30
        self.spawn_timer = 0
        self.game_over = False
        self.lives = 3
        self.font = pygame.font.SysFont("Arial", 30)

    def draw_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, BLACK)
        screen.blit(score_text, (10, 10))
        
    def draw_record(self):
        record_text = self.font.render("Record: " + str(self.record), True, BLACK)
        screen.blit(record_text, (10, 40))
        
    def draw_lives(self):
        lives_text = self.font.render("Lives: " + str(self.lives), True, RED)
        screen.blit(lives_text, (screen_width - 120, 10))

    def spawn_obstacle(self):
        y_pos = screen_height - 50
        x_pos = screen_width + random.randint(50, 200)
        new_obstacle = Obstacle(x_pos, y_pos, 20, 40)

        for obstacle in self.obstacles:
            if abs(obstacle.rect.x - new_obstacle.rect.x) < 60: 
                return  

        self.all_sprites.add(new_obstacle)
        self.obstacles.add(new_obstacle)

    def increase_speed(self):
        global speed
        if self.score % 100 == 0:
            speed += 1

    def check_collision(self):
        if pygame.sprite.spritecollide(self.dino, self.obstacles, False):
            return True
        return False

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
                self.spawn_obstacle()
                self.spawn_timer = 0

            for obstacle in self.obstacles:
                obstacle.move()

            if self.check_collision():
                self.lives -= 1
                if self.lives <= 0:
                    if self.score > self.record:
                        save_record(self.score)
                    run_game = False

            self.increase_speed()

            self.all_sprites.draw(screen)
            self.draw_score()
            self.draw_record()
            self.draw_lives()

            self.score += 1

            pygame.display.update()
            pygame.time.delay(30)

        pygame.quit()

game = Game()
game.run()
