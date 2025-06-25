import json
import pygame
from level import Level

pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
# Ayarlar
music_on = True
fullscreen = False
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

img=pygame.image.load("gear1.png") 
gear_img1=pygame.transform.scale(img, (40, 40))
# -------------------------------------------
current_screen = "menu" 
# Buton tanımı
def draw_button(label, rect):
    pygame.draw.rect(screen, WHITE, rect)
    text = font.render(label, True, BLACK)
    screen.blit(text, (rect.x + 10, rect.y + 5))

btn_width=250
btn_height=40
menu_x=275
menu_y=200
# Butonlar
menu_buttons = [
    {"label": "Ayarlar", "rect": pygame.Rect(menu_x, menu_y, btn_width, btn_height), "action": "settings"},
    {"label": "Oyuna Başla", "rect": pygame.Rect(menu_x,menu_y+(10+btn_height)*1, btn_width, btn_height), "action": "start_game"},
    {"label": "Çıkış", "rect": pygame.Rect(menu_x, menu_y+(10+btn_height)*2, btn_width, btn_height), "action": "quit"}
]

settings_buttons = [
    {"label": "Level 1", "rect": pygame.Rect(menu_x, menu_y, btn_width, btn_height), "action": "level1"},
    {"label": "Level 2", "rect": pygame.Rect(menu_x, menu_y+(10+btn_height)*1, btn_width, btn_height), "action": "level2"},
    {"label": "Level 3", "rect": pygame.Rect(menu_x, menu_y+(10+btn_height)*2, btn_width, btn_height), "action": "level3"},
    {"label": "Geri", "rect": pygame.Rect(menu_x, menu_y+(10+btn_height)*3, btn_width, btn_height), "action": "back"}
]

game_buttons = [
    {"label": "x", "rect": pygame.Rect(800-60, 20, 40, 40), "action": "menu"}
]
# -------------------------------------------
level_name=""
with open("settings.json", 'r') as file:
    settings_data = json.load(file)
    level_name=settings_data["level_file"]
level = Level(screen, level_name)

running = True
while running:
    clock.tick(60)
    # screen.fill((135, 206, 235))  # sky blue background
    screen.fill(GRAY)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            if current_screen == "menu":
                for btn in menu_buttons:
                    if btn["rect"].collidepoint(pos):
                        if btn["action"] == "settings":
                            current_screen = "settings"
                        elif btn["action"] == "start_game":
                            level = Level(screen,level_name)
                            current_screen = "game"
                        elif btn["action"] == "quit":
                            running = False

            elif current_screen == "settings":
                for btn in settings_buttons:
                    if btn["rect"].collidepoint(pos):
                        if btn["action"] == "level1":
                            level_name="level1.json"
                            with open("settings.json", 'w') as file:
                                str=''
                                str+='{\n'
                                str+='    "level_file":"level1.json"\n'
                                str+='}\n'
                                file.writelines(str)
                            btn["label"] = "Level 1"
                            current_screen = "menu"
                        elif btn["action"] == "level2":
                            level_name="level2.json"
                            with open("settings.json", 'w') as file:
                                str=''
                                str+='{\n'
                                str+='    "level_file":"level2.json"\n'
                                str+='}\n'
                                file.writelines(str)
                            btn["label"] = "Level 2"
                            current_screen = "menu"
                        elif btn["action"] == "level3":
                            level_name="level3.json"
                            with open("settings.json", 'w') as file:
                                str=''
                                str+='{\n'
                                str+='    "level_file":"level3.json"\n'
                                str+='}\n'
                                file.writelines(str)
                            btn["label"] = "Level 3"
                            current_screen = "menu"
                        elif btn["action"] == "back":
                            current_screen = "menu"
            elif current_screen=="game":
                for btn in game_buttons:
                    if btn["rect"].collidepoint(pos):
                        if btn["action"] == "menu":
                            current_screen="menu"

    if current_screen == "menu":
        for btn in menu_buttons:
            draw_button(btn["label"], btn["rect"])

    elif current_screen == "settings":
        for btn in settings_buttons:
            draw_button(btn["label"], btn["rect"])

    elif current_screen == "game":
        keys = pygame.key.get_pressed()
        
        level.update(keys)
        level.draw()

        if keys[pygame.K_r]:
            level = Level(screen, level_name)

            
        if keys[pygame.K_ESCAPE]:
            current_screen="menu"

        for btn in game_buttons:
            pygame.draw.rect(screen, WHITE, btn["rect"])
            screen.blit(gear_img1, btn["rect"])

        
    pygame.display.flip()

pygame.quit()
