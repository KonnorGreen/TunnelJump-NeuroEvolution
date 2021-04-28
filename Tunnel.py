import pygame, os

TUNNEL_IMAGE = pygame.image.load(os.path.join('Assets', 'tunnel.png'))


class Tunnel:
    def __init__(self):
        self.w = 100
        self.h = 100
        self.sprite = pygame.transform.scale(TUNNEL_IMAGE, (self.w, self.h))
        self.velx = 7
        self.hitbox = self.sprite.get_rect(midright=(900, 400))
    def draw(self,win):
        tun_rect = pygame.draw.rect(win, (255,0,0),(self.hitbox),-1)
        win.blit(self.sprite, self.hitbox)
    def move(self,dt):
        self.hitbox.centerx -= self.velx * dt
    def collision(self, player):
        if player.hitbox.colliderect(self.hitbox):
            return True
        return False