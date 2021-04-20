import pygame, os

TUNNEL_IMAGE = pygame.image.load(os.path.join('Assets', 'tunnel.png'))



###TUNNEL###
class Tunnel:
    def __init__(self):
        self.w = 115
        self.h = 125
        self.sprite = pygame.transform.scale(TUNNEL_IMAGE, (self.w, self.h))
        self.velx = 5
        self.hitbox = self.sprite.get_rect(midtop=(900, 300))
    def draw(self,win):
        tun_rect = pygame.draw.rect(win, (255,0,0),(self.hitbox),2)
        win.blit(self.sprite, self.hitbox)
    def move(self):
        self.hitbox.centerx -= self.velx
    def collision(self, player):
        if player.hitbox.colliderect(self.hitbox):
            return True
        return False
    def offscreen(self,player):
        if self.hitbox.x < player.x-150:
            return True
        return False