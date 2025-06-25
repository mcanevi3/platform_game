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

    def update(self, keys):
        self.handle_keys(keys)
        
    def on_left(self):
        self.ax = -0.2
    def on_right(self):
        self.ax = 0.2
    def on_up(self):
        self.ay = -0.2
    def on_down(self):
        self.ay = 0.2
    def on_space(self):
        print("space pressed")

    def handle_keys(self, keys):
        if any(keys):  
            if keys[pygame.K_LEFT]:
                self.on_left()                
            if keys[pygame.K_RIGHT]:
                self.on_right()                
            if keys[pygame.K_UP]:
                self.on_up()
            if keys[pygame.K_DOWN]:
                self.on_down()
            if keys[pygame.K_SPACE]:
                self.on_space()
        else:
            self.ax=0
            self.ay=0

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
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
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