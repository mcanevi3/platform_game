import pygame

class Player:
    def __init__(self, x, y, width, height, image=None, color=(0, 0, 225)):
        self.width = width
        self.height = height
        self.image = image
        self.color = color
        
        self.health=100
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0


    def draw(self, screen):
        if self.image:
            # Draw using the image
            screen.blit(self.image, (self.x, self.y))
        else:
            # Draw a rectangle with the given color
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def move(self):
        amax=1
        vmax=5
        self.ax=self.ax if self.ax<amax else amax
        self.ax=self.ax if self.ax>-amax else -amax
        self.ay=self.ay if self.ay<amax else amax
        self.ay=self.ay if self.ay>-amax else -amax

        self.vx += self.ax
        self.vy += self.ay

        self.vx=self.vx if self.vx<vmax else vmax
        self.vx=self.vx if self.vx>-vmax else -vmax
        self.vy=self.vy if self.vy<vmax else vmax
        self.vy=self.vy if self.vy>-vmax else -vmax

        self.x += self.vx
        self.y += self.vy
    def stop_x(self):
        self.ax=0
        self.vx=0
    def stop_y(self):
        self.ay=0
        self.vy=0
    def stop(self):
        self.stop_x()
        self.stop_y()
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    def get_future(self,horizon=1):
        res=[]
        x_future=self.x
        y_future=self.y
        for i in range(horizon):
            vx_future=self.vx+self.ax
            x_future+=vx_future
            vy_future=self.vy+self.ay
            y_future+=vy_future
            res.append({"x":x_future,"y":y_future,"vx":vx_future,"vy":vy_future})
        return res
    
    def decrease_health(self,amount=10):
        self.health-=amount
        if self.health<0:
            self.health=0

    def increase_health(self,amount=10):
        self.health+=amount
        if self.health>100:
            self.health=100
        
    def is_dead(self):
        return self.health<=0