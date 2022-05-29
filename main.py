import pygame, sys
import random

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [500, 550]
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.centerx >= 10:
            self.rect.centerx -= 8
        if key[pygame.K_RIGHT] and self.rect.centerx <= 990:
            self.rect.centerx += 8
        if pygame.sprite.spritecollide(self, meteor_group, True):
            self.kill()
    def create_laser(self):
        return Laser(self.rect.centerx,550)

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        global score
        self.image = pygame.image.load("img/laserBlue01.png")
        self.image = pygame.transform.scale(self.image, (10, 5))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        pygame.mixer.music.load("img/laser_shooting_sfx.wav")
    #    pygame.mixer.music.play()
    def update(self):
        global score
        self.rect.y -= 3
        if self.rect.y <= -50:
            self.kill()
        if pygame.sprite.spritecollide(self, meteor_group, True):
            self.kill()
            score +=1 

class Meteor(pygame.sprite.Sprite):
    def __init__(self, picture_path, m_x, m_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [m_x, m_y]
    def update(self):
        global n, collide
        self.rect.y += 2 
        if pygame.sprite.spritecollide(self, space_group, True):
            self.create_ship()
        if self.rect.y >= 700:
            self.kill()
    def create_ship(self):
        space_group.add(Spaceship("img/playerLife1_blue.png"))
    
class Life(pygame.sprite.Sprite):
    def __init__(self, picture_path, x_pos, y_pos):
        super().__init__()
        global collide
        self.image =pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]
    def update(self):
        pass

class Menu():
    def menu(self, start):
        men = True
        global count
        while men:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        men = False
                        count += 1
            pygame.display.update()
            self.image1 = pygame.Surface((screen_width, screen_height))
            self.image1.fill((100, 100, 100))
            screen.blit(self.image1, (0, 0))
            pygame.draw.rect(screen, (255, 255, 255), start)
            clock.tick(60)

class Run():
    def __init__(self):
        screen1.fill((100, 0, 100))
        screen.blit(screen1, (0, 0))
        screen.blit(img, (10, -100))
        if click:
            menu_page.menu(start)
        if count == 1:
            screen.blit(background, (0, 0))
            laser_group.draw(screen)
            laser_group.update()
            space_group.draw(screen)
            space_group.update()
            meteor_group.draw(screen)
            meteor_group.update()
            draw_text(screen, "SCORE", 16, 40, 10, (255, 255, 255))
            draw_text(screen, score, 16, 80, 10, (255, 255, 255))
            draw_text(screen, "LIVES", 16, 37, 30, (255, 255, 255))

#General setup
pygame.init()
clock = pygame.time.Clock()

#Screen
screen_width, screen_height = 1000, 600
score, n = 0, 3
click = False
count = 0
collide = 0
menu_page = Menu()
screen = pygame.display.set_mode((screen_width, screen_height))
screen1 = pygame.Surface((screen_width, screen_height))
img = pygame.image.load("img/pixil-frame-2.png")
img = pygame.transform.scale(img, (1000, 800))
rect = img.get_rect()
background = pygame.image.load("img/blue.png")
background = pygame.transform.scale(background,(screen_width, screen_height))
start = pygame.Rect(screen_width//2 - 50, screen_height//2 - 25, 100, 50)

#Spaceship
space_ship = Spaceship("img/playerLife1_blue.png")
space_group = pygame.sprite.Group()
space_group.add(space_ship)

#Laser
laser_group = pygame.sprite.Group()

#Meteor
meteor_group = pygame.sprite.Group()
metor_list = ["img/meteorBrown_big1.png","img/meteorBrown_big2.png","img/meteorBrown_big3.png","img/meteorBrown_big4.png",
                "img/meteorBrown_med1.png","img/meteorBrown_med3.png","img/meteorBrown_med3.png",
                "img/meteorBrown_small1.png","img/meteorBrown_small2.png"]
for meteor in range(100):
    big_meteor = Meteor(random.choice(metor_list), random.randint(0, screen_width), random.randint(-10000, 0))
    meteor_group.add(big_meteor)

#score
def draw_text(surface, score, size, x, y,color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render((str(score)), True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

pygame.mixer.music.load("img/MyVeryOwnDeadShip.wav")
pygame.mixer.music.play(-1)

#Game loop
while True:
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            count = 1
            if event.key == pygame.K_SPACE:
                laser_group.add(space_ship.create_laser())
        
    run = Run()
    pygame.display.update()
    clock.tick(60)