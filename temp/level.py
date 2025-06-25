import pygame
import json
from collections import deque

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

        self.frame_lock=0

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
        # self.player.update(keys)
        weights=[5,2,1]
        player_future=self.player.get_future(horizon=len(weights))
        player_future_rect=pygame.Rect(player_future[0]["x"],player_future[0]["y"],self.player.width,self.player.height)

        any_collision=False
        vx,vy,ax,ay=None,None,None,None

        for hazard in self.hazards:
            if hazard.colliderect(player_future_rect):
                any_collision = True

                self.frame_lock=self.frame_lock if self.frame_lock>0 else 5
                if self.frame_lock==5:
                    vx=0
                    vy=0
                    w_sum=0
                    for i,elem in enumerate(player_future):
                        w=weights[i]
                        w_sum+=w
                        vx+=w*elem["vx"]
                        vy+=w*elem["vy"]
                    vx=vx/w_sum
                    vy=vy/w_sum
                    vx*=-1
                    vy*=-1
                self.frame_lock-=1
                if self.frame_lock<0:
                    self.frame_lock=0

        self.text_health = self.font.render(f"{self.player.health}", True, (255, 255, 255))                

        # if self.checkpoint and (player_rect_x.colliderect(self.checkpoint) or player_rect_y.colliderect(self.checkpoint)):
        #     self.player.stop()
        #     self.completed=True
        if any_collision:
            if vx is not None: self.player.vx = vx
            if ax is not None: self.player.ax = ax
            if vy is not None: self.player.vy = vy
            if ay is not None: self.player.ay = ay
        else:
            self.frame_lock=0
            if any(keys):  
                if keys[pygame.K_LEFT]:
                    self.player.ax-=0.01
                if keys[pygame.K_RIGHT]:
                    self.player.ax+=0.01                
                if keys[pygame.K_UP]:
                    self.player.ay-=0.01
                if keys[pygame.K_DOWN]:
                    self.player.ay+=0.01
                if keys[pygame.K_SPACE]:
                    pass
            else:
                self.ax=0
                self.ay=0
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
