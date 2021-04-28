import pygame
import numpy as np
import os
from NeuralNetwork import NeuralNetwork
###CHARACTER###

IMAGE = pygame.image.load(os.path.join('Assets', 'llama.png'))
WIN_W, WIN_H = 900, 500


class Player:
    def __init__(self, win, brain):
        self.w = 155
        self.h = 140
        self.sprite = pygame.transform.scale(IMAGE, (self.w, self.h))
        self.x = 100
        self.y = 300
        self.score = 0
        self.fitness = 0
        self.gravity = .55
        self.on_ground = False
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.velY = 0
        self.brain = brain
        self.rect = self.sprite.get_rect(topleft=(0, 300))
        self.hitbox = pygame.Rect(self.x, self.y, 10, 90)
        if self.brain == None:
            self.brain = NeuralNetwork(2, 7, 1, None)
        else:
            self.brain = self.brain.copied()

    def __str__(self):
        return f'Fitness: {self.fitness}, Brain: {self.brain}'
    
    def __repr__(self):
        return f'Fitness: {self.fitness}, Brain: {self.brain}'

    def move(self,dt):
        self.velY += self.acceleration.y * dt
        if self.velY > 15: self.velY = 15
        self.rect.y += self.velY * dt + (self.acceleration.y * .5) * (dt*dt)
        if self.rect.y > 300:
            self.on_ground = True
            self.velY = 0
            self.rect.y = 300

    def jumpAction(self):
        if self.on_ground:
            self.velY -= 15
            self.on_ground = False

    def draw(self,win):
        self.hitbox = pygame.Rect(self.rect.x+20, self.rect.y+20, 70, 110)
        char_rect = pygame.draw.rect(win, (255,0,0),(self.hitbox),-1)
        win.blit(self.sprite, self.rect)
    
    def update(self,dt):
        self.score+=1
        self.move(dt)
    
    def dispose(self):
        self.brain.dispose()

    def mutate(self):
        self.brain.mutate(0.1)

    def think(self, tunnels):
        d = 0
        closest = None
        closestD = float("inf")
        for i in range(len(tunnels)):
            d = tunnels[i].hitbox.x - self.x
            if (d < closestD):
                closest = tunnels[i]
                closestD = d
    
        inputs = np.asarray([self.y, closest.hitbox.x])
        inputs = np.atleast_2d(inputs)
        output = self.brain.predict(inputs)
        if output[0] < .5:
                self.jumpAction()
           