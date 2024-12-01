import pygame
pygame.init()
screen_size = [500, 500]
screen = pygame.display.set_mode(screen_size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 255, 0), (250, 250), 75)
    pygame.display.flip()
    
pygame.quit()