import pygame
from level import Level

pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

level = Level(screen, "level1.json")

running = True
while running:
    clock.tick(60)
    screen.fill((135, 206, 235))  # sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    level.update(keys)
    level.draw()

    if keys[pygame.K_r]:
        level = Level(screen, "level1.json")

        
    if keys[pygame.K_ESCAPE]:
        running=False
        
    pygame.display.flip()

pygame.quit()
