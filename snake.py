# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 22:39:50 2019

@author: ChiJuWu
"""

import pygame
import numpy as np
import time
import random


##############
# game rules
##############

# If the snake eats a target, the target moves to a new position and snake length increases.
def collision_with_target(target_position, score):
    target_position = [random.randrange(1,30)*10, random.randrange(1,30)*10]
    score = score + 1
    return target_position, score


def collision_with_boundaries(snake_head):
    # 300 is the window size
    if snake_head[0]>=300 or snake_head[0]<0 or snake_head[1]>=300 or snake_head[1]<0:
        return 1
    else:
        return 0


def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0


def is_direction_blocked(snake_position, current_direction_vector):
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0


############################
# generate initial snake
############################

def generate_snake(snake_head, snake_position, target_position, button_direction, score):
    # change head direction
    if button_direction == 0:                # 0: leftward
        snake_head[0] = snake_head[0] - 10   # x axis decreases
    elif button_direction == 1:              # 1: rightward
        snake_head[0] = snake_head[0] + 10   # x axis increases
    elif button_direction == 2:              # 2: upward
        snake_head[1] = snake_head[1] - 10   # y axis increases
    elif button_direction == 3:              # 3: downward
        snake_head[1] = snake_head[1] + 10   # y axis decreases
    else:
        pass

        
    if snake_head == target_position:
        target_position, score = collision_with_target(target_position, score)
        snake_position.insert(0,list(snake_head))

    else:
        # To move the snake, we need to add one unit to the head and remove one unit from the tail.
        snake_position.insert(0,list(snake_head))
        snake_position.pop()

    return snake_position, target_position, score

############################
# display snake and target
############################

def display_target(display, target_position, target):
    display.blit(target, (target_position[0], target_position[1]) )


def display_snake(snake_position):
    for position in snake_position:
        # draw rectangular 
        pygame.draw.rect(display, black, pygame.Rect(position[0], position[1], 10, 10) )

############################
# Game controlling by user
############################

def play_game(snake_head, snake_position, target_position, button_direction, target, score):
    # default: not to crash
    crashed = False
    prev_button_direction = 1    # default original direction is rightward: 1
    button_direction = 1

    # current direction = head position - 1st body position
    current_direction_vector = np.array(snake_position[0])-np.array(snake_position[1])

    # as long as game is not crashed
    while crashed is not True:
        for event in pygame.event.get():
            # crashed if quit game
            if event.type == pygame.QUIT:
                crashed = True
            # detect if key is physically pressed
            if event.type == pygame.KEYDOWN:
                # if press 'left' and the previous direction is not right 
                # (because cannot go backwards), then change to left (assigned to 0) 
                if event.key == pygame.K_LEFT and prev_button_direction != 1:
                    button_direction = 0
                # if press 'right' and the previous direction is not left 
                # (because cannot go backwards), then change to right (assigned to 1) 
                elif event.key == pygame.K_RIGHT and prev_button_direction != 0: 
                    button_direction = 1
                # if press 'up' and the previous direction is not down 
                # (because cannot go backwards), then change to up (assigned to 2) 
                elif event.key == pygame.K_UP and prev_button_direction != 3:
                    button_direction = 2
                # if press 'down' and the previous direction is not up 
                # (because cannot go backwards), then change to down (assigned to 3) 
                elif event.key == pygame.K_DOWN and prev_button_direction != 2: 
                    button_direction = 3
                # any other key does not change anything
                else:
                    button_direction = button_direction

        display.fill(window_color)
        display_target(display, target_position, target)
        display_snake(snake_position)

        snake_position, target_position, score = generate_snake(snake_head, snake_position, target_position, button_direction, score)

        # caption of the window
        if score <= 2:
            pygame.display.set_caption("Snake Game v.1  Level 1")
            pygame.display.update()
        elif score >= 3 and score <= 5:
            pygame.display.set_caption("Snake Game v.1  Level 2")
            pygame.display.update()
        elif score >= 6 and score <= 8:
            pygame.display.set_caption("Snake Game v.1  Level 3")
            pygame.display.update()
        else:
            pygame.display.set_caption("Snake Game v.1  Level 4")
            pygame.display.update()
        

        prev_button_direction = button_direction
        if is_direction_blocked(snake_position, current_direction_vector) == 1:
            crashed = True
        
        # change level speed 
        if score <= 2:
            clock.tick(4)
        elif score >= 3 and score <= 5:
            clock.tick(6)
        elif score >= 6 and score <= 8:
            clock.tick(8)
        else:
            clock.tick(10)
            
    return score

############################
# display final score
############################

def display_final_score(display_text, final_score):
    largeText = pygame.font.Font('freesansbold.ttf',int(400/20))
    TextSurf = largeText.render(display_text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1)


############################
# main body of game setting
############################

if __name__ == "__main__":

    # Initializing display setups
    #-----------------------------
    display_width, display_height = 300, 300
    
    green = (0,255,0)
    red = (255,0,0)
    black = (0,0,0)
    window_color = (250,250,250)
    clock = pygame.time.Clock()
    target_image = pygame.image.load('target.jpg')

    # Initializing snake and target position (both random)
    #--------------------------------------------------------------
    # head position is random between 30% to 70% of the display
    snake_head = np.int_(np.random.uniform(0.2*display_width/10, 0.8*display_width/10, 2))*10
    snake_head = snake_head.tolist()
    # snake default length: 3 pixels (horizontal, head faces right)
    snake_position = [[snake_head[0], snake_head[1]], \
                      [snake_head[0]-10,snake_head[1]], \
                      [snake_head[0]-20,snake_head[1]]]
    # target position
    target_position = [random.randrange(1,30)*10, random.randrange(1,30)*10]
    # initial score
    score = 0

    #initialize pygame modules
    pygame.init()

    # display game window
    #--------------------------------------------------------------
    display = pygame.display.set_mode((display_width, display_height))
    display.fill(window_color)
    pygame.display.update()

    final_score = play_game(snake_head, snake_position, target_position, 1, target_image, score)
    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()

    display_text = 'Game Over! Score:' + str(final_score)
    display_final_score(display_text, final_score)

    pygame.quit()