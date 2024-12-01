import pygame
import random
import time

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.mixer.init()
pygame.init()
#pygame.mixer.music.load("StarWars.wav")
#pygame.mixer.music.play(-1)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CLOCK_SPEED = 15
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 350)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load("jet4.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        #self.surf.fill((0, 200, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
    
    def update(self, key_pressed):
        if key_pressed[K_UP]:
            self.rect.move_ip(0, -10)
        elif key_pressed[K_DOWN]:
            self.rect.move_ip(0, 10)
        elif key_pressed[K_LEFT]:
            self.rect.move_ip(-10, 0)
        elif key_pressed[K_RIGHT]:
            self.rect.move_ip(10, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemies, self).__init__()
        #self.surf = pygame.Surface((25, 10))
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        #self.surf.fill((0, 200, 0))
        self.rect = self.surf.get_rect(center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))
        self.speed = random.randint(5, 25)
        self.mask = pygame.mask.from_surface(self.surf)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

def show_game_over(score=0):
    gover_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font_obj = pygame.font.SysFont(None, 40)
    text_obj = font_obj.render("GAME OVER !!", True, (0, 200, 0))
    surf_center = ((SCREEN_WIDTH-text_obj.get_width())/2,
                    (SCREEN_HEIGHT-text_obj.get_height())/2)
    score_obj = font_obj.render(f"SCORE: {score}", True, (0, 200, 0))
    score_location = ((SCREEN_WIDTH-score_obj.get_width())/2,
                        ((SCREEN_HEIGHT + 100)-score_obj.get_height())/2)
    waiting = True
    while waiting:
        gover_screen.fill((0, 0, 0))
        gover_screen.blit(text_obj, surf_center)
        gover_screen.blit(score_obj, score_location)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    waiting = False
            elif event.type == QUIT:
                waiting = False
        pygame.display.flip()

def show_level_select():
    bg_image = pygame.image.load("space1.png").convert()
    bg_image.set_colorkey((0, 0, 0), RLEACCEL)
    level_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font_obj = pygame.font.SysFont(None, 30)
    level_buttons = []
    running = True
    button_width = 200
    button_height = 40
    global CLOCK_SPEED
    button_x = (SCREEN_WIDTH - button_width)/2
    button_y = (SCREEN_HEIGHT - button_height)/2
    for i in range(1, 4):
        button = pygame.Rect(button_x, 100 + 50 * i, button_width, button_height)
        level_buttons.append(button)
    level_screen.blit(bg_image, (0, 0))
    for button in level_buttons:
        pygame.draw.rect(level_screen, (255, 255, 255), button)
        txt = font_obj.render(f"Level {level_buttons.index(button)}", True, (0, 0, 0))
        text_rect = txt.get_rect(center=button.center)
        level_screen.blit(txt, text_rect)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in level_buttons:
                    if button.collidepoint(mouse_pos):
                       CLOCK_SPEED += 5 * level_buttons.index(button)
                       running = False
                    
        pygame.display.flip()

def main():
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    running = True
    clock = pygame.time.Clock()
    font_obj = pygame.font.SysFont(None, 35)
    score = 0
    bg_image = pygame.image.load("space1.png").convert()
    bg_image.set_colorkey((0, 0, 0), RLEACCEL)
    show_level_select()
    while running:
        score += 1
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemies()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        enemies.update()   
        screen.blit(bg_image, (0, 0))
        #screen.fill((0, 0, 0))
        score_txt = font_obj.render(f"SCORE: {score}", True, (0, 200, 0))
        score_width, _ = score_txt.get_size()
        #screen.blit(score_update, (SCREEN_WIDTH-100, SCREEN_HEIGHT-10))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            screen.blit(score_txt, (SCREEN_WIDTH - score_width, 0))
        
        if pygame.sprite.spritecollideany(player, enemies, pygame.sprite.collide_mask):
            pygame.time.wait(2000)
            player.kill()
            show_game_over(int(score))
            running = False
        pygame.display.flip()
        clock.tick(CLOCK_SPEED)
    
if __name__ == "__main__":
    main()