from random import random
from typing import BinaryIO
import pygame, sys, random
from pygame.constants import FULLSCREEN, QUIT
from pygame import mixer

def draw_floor(): #move floor to the left
    screen.blit(floor_surface,(floor_x_pos, 450))
    screen.blit(floor_surface,(floor_x_pos + 288, 450))

def create_pipe():
    random_pipes_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipes_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipes_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes): #bird hit pipe
    global life
    for pipe in pipes:
        if bird_rect.colliderect(pipe) and life <= 0:
            death_sound.play()
            return False
        elif bird_rect.colliderect(pipe):
            life -= 1

    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
            return False
        
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird,bird_rect

def score_display(game_state):
    global life
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)

        life_surface = game_font.render('Life = 5', True, (255, 255, 255))
        life_rect = score_surface.get_rect(center = (10, 50))
        screen.blit(life_surface, life_rect)

    if game_state == 'game_over':
        life = 140
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score:{int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (144, 425))
        screen.blit(high_score_surface, high_score_rect)
        
        life_surface = game_font.render('Life = 0', True, (255, 255, 255))
        life_rect = score_surface.get_rect(center = (50, 50))
        screen.blit(life_surface, life_rect)    

        life_surface = hint_font.render('hint : you can hit pipe 5 times', True, (255, 255, 255))
        life_rect = score_surface.get_rect(center = (50, 100))
        screen.blit(life_surface, life_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

pygame.mixer.pre_init(frequency = 44100, size = 8, channels=1, buffer=256)
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 20)
hint_font = pygame.font.Font('04B_19.ttf', 10)

#game variables
gravity = 0.125
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
life = 140

bg_surface = pygame.image.load('assets/background-night.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,600)
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center =  (144, 256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

"""mixer.music.load('sound/canon in d.wav')
mixer.music.play(-1)"""

while True: #for one player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 3 #how high bird jump
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0

            bird_surface, bird_rect = bird_animation()    
    
    screen.blit(bg_surface, (0,0)) #make background on the scrren
    
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        check_collision(pipe_list)
        game_active = check_collision(pipe_list)
        
        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    #floor 
    floor_x_pos -= 0.5
    draw_floor()
    if floor_x_pos <= -288:  #reset floor to run again
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(80)
