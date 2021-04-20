import pygame
import numpy as np
import os
from NeuralNetwork import NeuralNetwork
###CHARACTER###

IMAGE = pygame.image.load(os.path.join('Assets', 'RunningMan.png'))
WIN_W, WIN_H = 900, 500

class Player:
    def __init__(self, win):
        self.w = 155
        self.h = 140
        self.char = pygame.transform.scale(IMAGE, (self.w, self.h))
        self.x = 100
        self.y = 300
        self.vely = 25
        self.score = 0
        self.fitness = 0
        self.jump = False
        self.brain = None
        self.hitbox = pygame.draw.rect(win, (255,0,0),(self.x+55,self.y+20,50,100),2)
        if self.brain == None:
            self.brain = NeuralNetwork(3, 7, 2, None)
        else:
            self.brain = self.brain.copy()

    def jumpAction(self):
        if self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely
            self.vely -= 1
        if self.vely < -25:
            self.jump = False
            self.vely = 25

    def draw(self,win):
        self.hitbox = pygame.draw.rect(win, (255,0,0),(self.x+55,self.y+20,50,100),2)
        win.blit(self.char, (self.x, self.y))
    
    def update(self):
        self.score+=1
    
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
            if (d < closestD and d > 0):
                closest = tunnels[i]
                closestD = d
        inputs = np.asarray([self.y / WIN_H, closest.hitbox.x / WIN_W, self.vely / 10])
        inputs = np.atleast_2d(inputs)
        output = self.brain.predict(inputs)
        if output[0] <.5:
            self.jumpAction()
###CHARACTER###