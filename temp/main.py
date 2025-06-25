import json
import pygame
from temp.level import Level

pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

level_name=""
with open("settings.json", 'r') as file:
    settings_data = json.load(file)
    level_name=settings_data["level_file"]
level = Level(screen, level_name)

running = True
while running:
    clock.tick(30)
    screen.fill((135, 206, 235))  # sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    level.update(keys)
    level.draw()

    if keys[pygame.K_r]:
        level = Level(screen, level_name)

        
    if keys[pygame.K_ESCAPE]:
        running=False
        
    pygame.display.flip()

pygame.quit()
