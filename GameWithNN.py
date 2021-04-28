#ML Learning Project
#Video for Genetic Algorithm: https://www.youtube.com/playlist?list=PLRqwX-V7Uu6bJM3VgzjNV5YxVxUwzALHV
#

#os.environ["CUDA_VISIBLE_DEVICES"]="-1" #Use CPU

import pygame
import os, time,random
from Player import Player
from Tunnel import Tunnel

###GN ALGO###
def nextGen(savedPlayers):
    calcFit(savedPlayers) # Calculate the fitness of each savedPlayer
    for i in range(TOTAL_PLAYERS):
        players.append(pickOne())
    savedPlayers.clear()
    return savedPlayers

def calcFit(savedPlayers):
    summ = 0
    for p in savedPlayers:
        summ += p.score    # Add up all of the scores
    for p in savedPlayers:
        p.fitness = p.score / summ #Normalizing all of the fitness
    return savedPlayers # We return the list of savedPlayers with their updated fitnesses.

def pickOne():
    index = 0 # Assume that the one we will pick is first
    r = random.uniform(0,1) # Random number between 0 and 1.0
    while r > 0:
        r = r - savedPlayers[index].fitness # Pick until we are below 0
        index+=1
    index -= 1
    play = savedPlayers[index] # Best fitness
    
    child = Player(WIN, play.brain) #I make a child and use the best players brain
    child.mutate()
    return child
###GN ALGO###

###SCORE and HIGHSCORE###
def score_display(game_state):
    if game_state == 'main_game':
        font = pygame.font.SysFont(None, 24, bold=False, italic=False)
        gen_surface = font.render(
            f'Generation: {int(generation)}', True, (0, 0, 0))
        gen_rect = gen_surface.get_rect(center=(400, 50))
        WIN.blit(gen_surface, gen_rect)
        score_surface = font.render(
            f'Score: {int(game_score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(100, 50))
        WIN.blit(score_surface, score_rect)
        high_score_surface = font.render(
            f'High Score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(800, 50))
        WIN.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
###SCORE and HIGHSCORE###

pygame.display.init()
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.font.init()
pygame.scrap.init()
WIDTH, HEIGHT = 900, 500 # Width and Height of the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load(os.path.join('Assets', 'background.jpg'))
bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption("Jump AI")  # Window Title


SPAWNTUNNEL = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUNNEL, random.randint(1000, 1500)) #Timer to spawn Tunnel


TOTAL_PLAYERS = 15
players = []
savedPlayers = []
tunnel_list = []
generation = 1
for i in range(TOTAL_PLAYERS):
    players.append(Player(WIN, None))
bgi = 0
game_score = 0
high_score = 0
FPS = 60


last_time = time.time()

clock = pygame.time.Clock()
game_running = True
while game_running:  # GameLoop
    dt = time.time() - last_time
    dt*=FPS
    last_time = time.time()
    for event in pygame.event.get():  # Every event will be under here
        if event.type == pygame.QUIT:  # Event to run when we click the X button
            game_running = False
        if event.type == SPAWNTUNNEL:
            pygame.time.set_timer(SPAWNTUNNEL, random.randint(1000, 2000))
            tunnel_list.append(Tunnel())

    
    # Tunnels
    for tunnel in reversed(tunnel_list):
        tunnel.move(dt)
        if tunnel.hitbox.x < -100:
                tunnel_list.remove(tunnel)


    for tunnel in tunnel_list:
        for x,player in enumerate(players):
            if len(tunnel_list) == 0:
                pass    
            if tunnel.collision(player):
                savedPlayers.append(players.pop(x))

    for player in players:
        if len(tunnel_list) == 0:
                pass
        else:
            player.think(tunnel_list)
            player.update(dt)

    if len(players) == 0:
        print("All Dead")
        high_score = update_score(game_score, high_score)
        game_score = 0
        generation += 1
        nextGen(savedPlayers)
        tunnel_list.clear()


    ### Background ###
    WIN.fill((0, 0, 0))
    WIN.blit(bg, (bgi, 0))
    WIN.blit(bg,  (WIDTH+bgi, 0))
    if bgi == -WIDTH:
        WIN.blit(bg, (WIDTH+bgi, 0))
        bgi = 0
    bgi -= 1
        ### Background ###


    for player in players:
        player.draw(WIN)
            

    for tunnel in tunnel_list:
        tunnel.draw(WIN)

    game_score += 0.03
    score_display('main_game')
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
### GAME CODE ###
