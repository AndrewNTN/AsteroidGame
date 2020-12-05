import pygame
import random
import math

# Initialization of pygame and its font module
pygame.init()
pygame.font.init()

FPS = 60
WIN_HEIGHT = 800
WIN_WIDTH = 500
SCORE_FONT = pygame.font.SysFont("TrebuchetMSBold", 40)
show_hitbox = True

pygame.display.set_caption("Asteroids")
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

"""
Load images from imgs folder
"""
# Set Icon
icon = pygame.image.load("imgs/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg_img = pygame.image.load("imgs/bg.jpg").convert_alpha()

hole_imgs = [pygame.transform.scale(pygame.image.load("imgs/hole1.png"), (70, 20)).convert_alpha(),
             pygame.transform.scale(pygame.image.load("imgs/hole2.png"), (128, 20)).convert_alpha()]
asteroid_img = pygame.transform.scale(pygame.image.load("imgs/asteroid.png"), (30, 50)).convert_alpha()
asteroid_img = asteroid_img.convert_alpha()
player_img = pygame.image.load("imgs/player.png").convert_alpha()

# Set icon
pygame.display.set_icon(icon)


class Player:
    def __init__(self):
        self.x = 210
        self.y = 100
        self.speed = 0
        self.state = "ready"    # ready = ready to drop asteroid, unready = asteroid is already dropped
        self.img = player_img

    def move_left(self):
        self.speed = -5

    def move_right(self):
        self.speed = 5

    def stop_move(self):
        self.speed = 0

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Hole:
    def __init__(self, x, y, imgnum):
        self.x = x
        self.y = y
        self.imgs = hole_imgs[imgnum]           # Image which is chosen by random.randint() for varying hole sizes
        self.h = self.imgs.get_height()
        self.w = self.imgs.get_width()
        self.hitbox = (self.x, self.y, self.w, self.h)          # Four int values that declare the rectangular hitbox

    def draw(self):
        self.hitbox = (self.x, self.y, self.w, self.h)
        screen.blit(self.imgs, (self.x, self.y))

    def collide(self, asteroid):
        # If the asteroid is between the start and the end of the black hole horizontally
        if asteroid.x <= self.x + self.w and asteroid.x + 32 >= self.x:
            # If the asteroid is between the start and the end of the black hole vertically
            if asteroid.y + 32 > self.y and asteroid.y - 32 < self.y + self.h:
                return True

            return False


class Asteroid:
    def __init__(self):
        self.x = 0
        self.y = 200
        self.speed = 10
        self.img = asteroid_img
        self.h = asteroid_img.get_height()
        self.w = asteroid_img.get_width()
        self.hitbox = (self.x + 16, self.y - 5, self.w, self.h)    # Four int values that declare the rectangular hitbox


def drop_asteroid(x, y, ast):
    screen.blit(asteroid_img, (x + 16, y - 5))
    ast.hitbox = (ast.x + 16, ast.y - 5, ast.w, ast.h)
    # Show asteroid hitbox
    if show_hitbox:
        pygame.draw.rect(screen, (255, 0, 0), ast.hitbox, 2)


def main():
    player = Player()
    ast = Asteroid()
    hole_num = 7
    combo = 0
    holes = [Hole(random.randint(1, 500 - 130), random.randint(300, 760), random.choice([0, 1])) for x in
             range(hole_num)]
    score = 0
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            # Checking for keystrokes for player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.move_left()
                if event.key == pygame.K_d:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    if player.state == "ready":
                        ast.x = player.x
                        player.state = "unready"
                        drop_asteroid(ast.x, ast.y, ast)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop_move()

        # Draws the background
        screen.blit(bg_img, (0, 0))

        # Draws the score
        score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draws the black holes
        for hole in holes:
            hole.draw()

        # Draws the player
        player.draw()

        # Player Boundaries
        player.x += player.speed
        if player.x <= 0:
            player.x = 0
        if player.x >= 436:
            player.x = 436

        # Check for collision
        for x, hole in enumerate(holes):
            if hole.collide(ast):
                # More points from hitting multiple holes with one asteroid
                score += 1 + combo
                combo += 1
                holes.pop(x)

        # Resets the asteroid once it reaches the edge of the screen
        if ast.y >= 800:
            ast.y = 200
            combo = 0
            player.state = "ready"

        # Asteroid movement
        if player.state is "unready":
            player.state = "unready"
            drop_asteroid(ast.x, ast.y, ast)
            ast.y += ast.speed

        # Show black hole hitbox
        if show_hitbox:
            for hole in holes:
                pygame.draw.rect(screen, (255, 0, 0), hole.hitbox, 2)

        # Restarts the game if all of the black holes are gone
        if len(holes) == 0:
            main()

        pygame.display.update()


main()
