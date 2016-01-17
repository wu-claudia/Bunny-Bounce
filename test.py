# -*- coding: utf-8 -*-
# bunnybounce.py
# Created 1/17/2016 by Claudia Wu, Illina Yang, Wings Yeung, Diane Zhou

import pygame, sys

"""
Global Variables
"""
WIDTH = 500
MESSAGE_WIDTH = 200
HEIGHT = 500
BORDER_SIZE = 10
BUNNY_SIZE = 50
CARROT_SIZE = 50
TREE_SIZE = 50
ROCK_SIZE = 25
FIRE_SIZE = 50

# RGB Color Definitions
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def new_game():

    pygame.init()

    window_size = (WIDTH + MESSAGE_WIDTH + 3*BORDER_SIZE, HEIGHT + 2*BORDER_SIZE)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Bunny Bounce")

    env = Environment() #This part will initialize all the objects (bunny, obstacles, etc)
    message = ["hello"]
    update_screen(screen, env, message)

def update_screen(screen, env, message = []):
    screen.fill(BLACK) # change color later or insert image
    for _ in range(len(message)):
        update_text(screen, message, _)
    env.theEntities.draw(screen)
    pygame.display.flip()


def update_text(screen, message, index, textSize = 20):
    font = pygame.font.Font(None, textSize)
    text = font.render(message[index], True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.x = WIDTH + 2*BORDER_SIZE
    textRect.y = textSize * (index+1)
    screen.blit(text, textRect)

class Environment:
    
    def __init__(self):

        self.item_locations = dict.fromkeys([(x,y) for x in range(WIDTH) for y in range(HEIGHT)])

        self.theEntities = pygame.sprite.Group() #Sprite list of the bunny and the items

        self.bunny = Bunny()
        self.theEntities.add(self.bunny)
        self.item_locations[(self.bunny.rect.centerx, self.bunny.rect.centery)] = self.bunny

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
    
    def set_pic(self, name_of_image, size):
        self.image = pygame.image.load(name_of_image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, size)

class Bunny(Entity):
    def __init__(self):
        super(Bunny, self).__init__()
        self.name_of_image = "bunny.png"
        self.rect = pygame.Surface([BUNNY_SIZE, BUNNY_SIZE]).get_rect()
        self.rect.centerx = WIDTH/2 #Keeps bunny centered at all times
        self.rect.centery = HEIGHT*4/5
        self.set_pic(self.name_of_image, (BUNNY_SIZE, BUNNY_SIZE))

if __name__ == "__main__":
    new_game()
