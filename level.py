import pygame
import json
from player import Player

class Level:
    def __init__(self, screen, level_file):
        self.screen = screen
        
        self.platforms = []
        self.hazards = []
        self.checkpoint = None

        self.load_level(level_file)

        self.font = pygame.font.SysFont("Arial", 32)
        self.text_health = self.font.render(f"{self.player.health}", True, (255, 255, 255))

        # static images
        self.images=[]
        self.image_positions=[]

        img=pygame.image.load("heart1.png") 
        self.images.append(pygame.transform.scale(img, (75, 80)))
        self.image_positions.append((18,20))
       
        self.completed=False
        img=pygame.image.load("goblet1.png") 
        self.completed_img=pygame.transform.scale(img, (120, 120))

    def load_level(self, level_file):
        with open(level_file, 'r') as file:
            level_data = json.load(file)

        for plat in level_data["platforms"]:
            platform = pygame.Rect(plat["x"], plat["y"], plat["width"], plat["height"])
            self.platforms.append(platform)
        
        for hazard in level_data["hazards"]:
            hazard_rect = pygame.Rect(hazard["x"], hazard["y"], hazard["width"], hazard["height"])
            self.hazards.append(hazard_rect)
        
        checkpoint_data = level_data.get("checkpoint", None)
        if checkpoint_data:
            self.checkpoint = pygame.Rect(checkpoint_data["x"], checkpoint_data["y"],
                                          checkpoint_data["width"], checkpoint_data["height"])
        
        init_pos=level_data["start"]
        self.player = Player(init_pos["x"],init_pos["y"],40,40)


    def update(self, keys):
        if self.completed:
            self.screen.blit(self.completed_img,(340,150))
            return 
            
        self.player.update(keys)

        player_rect=self.player.get_rect()
        player_rect=pygame.Rect(player_rect.x+self.player.vx+self.player.ax/2, player_rect.y+self.player.vy+self.player.ay/2, player_rect.width, player_rect.height)
        
        for platform in self.platforms:
            if player_rect.colliderect(platform):
                if self.player.vx>0:
                    self.player.ax=0
                    self.player.vx*=-1
                elif self.player.vx<0:
                    self.player.ax=0
                    self.player.vx*=-1

                if self.player.vy>0:
                    self.player.ay=0
                    self.player.vy*=-1
                elif self.player.vy<0:
                    self.player.ay=0
                    self.player.vy*=-1    
                
        for hazard in self.hazards:
            if player_rect.colliderect(hazard):
                self.player.decrease_health(19)

                if self.player.vx>0:
                    self.player.ax=0
                    self.player.vx*=-1
                elif self.player.vx<0:
                    self.player.ax=0
                    self.player.vx*=-1

                if self.player.vy>0:
                    self.player.ay=0
                    self.player.vy*=-1
                elif self.player.vy<0:
                    self.player.ay=0
                    self.player.vy*=-1


                self.text_health = self.font.render(f"{self.player.health}", True, (255, 255, 255))                

        if self.checkpoint and player_rect.colliderect(self.checkpoint):
            self.player.ax=0
            self.player.vx=0
            self.player.ay=0
            self.player.vy=0

            self.completed=True
        
        self.player.move()

        
    def draw(self):
        if not self.player.is_dead():
            self.player.draw(self.screen)

        for platform in self.platforms:
            pygame.draw.rect(self.screen, (139, 69, 19), platform)  # brown platforms

        for hazard in self.hazards:
            pygame.draw.rect(self.screen, (255, 0, 0), hazard)  # red hazards

        if self.checkpoint:
            pygame.draw.rect(self.screen, (0, 255, 0), self.checkpoint)  # green checkpoint

        for i,img in enumerate(self.images):
            self.screen.blit(img,self.image_positions[i])

        if self.text_health:
            text_rect = self.text_health.get_rect(center=(55,55))
            self.screen.blit(self.text_health, text_rect)
