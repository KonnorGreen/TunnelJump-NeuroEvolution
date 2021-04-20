import pygame
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
import random
from Player import Player
from Tunnel import Tunnel


###GN ALGO###
def nextGen(savedPlayers):
    calcFit()
    for i in range(TOTAL):
        players.append(pickOne())
    for i in range(TOTAL):
        savedPlayers[i].dispose()
    savedPlayers = []
    return savedPlayers

def pickOne():
    index = 0
    r = random.uniform(0,1)
    while r > 0:
        r = r - savedPlayers[index].fitness
        index+=1
    index -= 1
    play = savedPlayers[index]
    child = Player(WIN)
    child.brain = play.brain
    child.mutate()
    return child



def calcFit():
    summ = 0
    for p in savedPlayers:
        summ += p.score
    for p in savedPlayers:
        p.fitness = p.score / summ

###SCORE and HIGHSCORE###
def score_display(game_state):
    if game_state == 'main_game':
        font = pygame.font.SysFont(None, 24, bold=False, italic=False)
        gen_surface = font.render(
            f'Generation: {int(generation)}', True, (255, 255, 255))
        gen_rect = gen_surface.get_rect(center=(400, 50))
        WIN.blit(gen_surface, gen_rect)
        score_surface = font.render(
            f'Score: {int(game_score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(100, 50))
        WIN.blit(score_surface, score_rect)
        high_score_surface = font.render(
            f'High Score: {int(high_score)}', True, (255, 255, 255))
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
pygame.time.set_timer(SPAWNTUNNEL, 2300)  # Spawns a tunnel every 2.3 seconds

# Initiates Character

TOTAL = 5
players = []
savedPlayers = []
tunnel_list = []
generation = 0

for i in range(TOTAL):
    players.append(Player(WIN))
bgi = 0
game_score = 0
high_score = 0
game_active = True
FPS = 60  # Frames Per Second
clock = pygame.time.Clock()
game_running = True
tunnel_list.append(Tunnel())
while game_running:  # GameLoop
    clock.tick(FPS)  # Ensuring we never go over capped framerate
    for event in pygame.event.get():  # Every event will be under here
        if event.type == pygame.QUIT:  # Event to run when we click the X button
            game_running = False
        if event.type == SPAWNTUNNEL:
            tunnel_list.append(Tunnel())
    
        # Tunnels
    for tunnel in reversed(tunnel_list):
        tunnel.move()
        for player in reversed(players):
            crash = tunnel.collision(player)
            if crash:
                savedPlayers.append(players.pop(0))
        if tunnel.offscreen(player):
              tunnel_list.remove(tunnel)

    for player in players:
        player.think(tunnel_list)
        player.update()

    if len(players) == 0:
        high_score = update_score(game_score, high_score)
        game_score = 0
        generation += 1
        nextGen(savedPlayers)
        tunnel_list.clear()
        pygame.time.set_timer(SPAWNTUNNEL, 0)
        pygame.time.set_timer(SPAWNTUNNEL, 2300)
        tunnel_list.append(Tunnel())


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
    #pygame.time.delay(10)
    pygame.display.update()

pygame.quit()
### GAME CODE ###
