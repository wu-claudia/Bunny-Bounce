# bunnybounce.py
# Created 1/17/2016 by Claudia Wu, Illina Yang, Wings Yeung, Diane Zhou

import pygame, sys
import random

"""
Global Variables
"""
WIDTH = 500
MESSAGE_WIDTH = 200
HEIGHT = 500
BORDER_SIZE = 10
BUNNY_SIZE = 50
CARROT_SIZE = 50
TREE_SIZE = 100 #tall = TREE_SIZE*2
ROCK_SIZE = 25
FIRE_SIZE = 50
WOLF_SIZE = 75
BOTTOM = HEIGHT * 4/5
BOUNCE_HEIGHT = 10

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

        main_loop(screen, env)

def main_loop(screen, env):

        end = False
        message = ["Hello"] # display lives = 3, score = 0
        update_screen(screen, env, message)
        high_score = 0

        loop_count = 0
        bounce_count = 0
        height = BOUNCE_HEIGHT

        while end == False:

                """
                Every iteration of the loop: move all carrots and obstacles to the left.
                Bunny bounce movement.
                Check for user input.
                """

                # Move all items to the left.
                for item in env.theCarrots:
                        env.step(item) 
                for item in env.theObstacles:
                        env.step(item)

                # Remove items that have reached the left side of the screen.
                for carrot in env.theCarrots:
                        if carrot.rect.left < BORDER_SIZE:
                                env.remove_carrot(carrot)
                for obstacle in env.theObstacles:
                        if obstacle.rect.left < BORDER_SIZE:
                                env.remove_obstacle(obstacle)

                # Bounce movement
                env.bunny.bounce(bounce_count, height)
                bounce_count = (bounce_count+1) % height

                # Check for user input and respond accordingly.
                events = pygame.event.get() #Contains entire events
                event_types = [event.type for event in events]
                if pygame.KEYDOWN in event_types:
                        if events[0].key == pygame.K_SPACE:
                                if height < 6*BOUNCE_HEIGHT:
                                        height += BOUNCE_HEIGHT


                """
                Every 10 iterations of the loop: place a carrot and randomly place an obstacle
                """

                if loop_count % 10 == 0:
                        
                        env.place_carrot(Carrot())

                        # get a random int, if int = 0, then place obstacle (random_int for which obstacle)
                        num = random.randint(0, 100)

                        #Random chances of obstacles appearing
                        if num in range(0, 5):
                                env.place_obstacle(Tree_Tall())
                        elif num in range(5, 10):
                                env.place_obstacle(Tree_Short())
                        elif num in range(10, 20):
                                env.place_obstacle(Rock())
                        elif num in range(20, 25):
                                env.place_obstacle(Fire())
                        elif num in range(25, 35):
                                env.place_obstacle(Wolf())

                update_screen(screen, env, message)

                loop_count += 1

                events = pygame.event.get() #Contains entire events
                event_types = [event.type for event in events]
                if pygame.QUIT in event_types:
                        end = True

        message = ["Hello"]
        update_screen(screen, env, message)

                # if env.bunny.carrots >= high_score:
        #       with open('saved_state.txt', 'w') as f:
        #               f.write( str(env.bunny.carrot ) )

def update_screen(screen, env, message = []):
        screen.fill(BLACK) # change color later or insert image
        pygame.draw.lines(screen, WHITE, False, [(BORDER_SIZE, BOTTOM), (BORDER_SIZE+WIDTH, BOTTOM)], 1)
        for _ in range(len(message)):
                update_text(screen, message, _)
        env.theCarrots.draw(screen)
        env.theObstacles.draw(screen)
        env.theBunny.draw(screen)
        pygame.display.flip()

def update_text(screen, message, index, textSize = 20):
        font = pygame.font.Font(None, textSize)
        text = font.render(message[index], True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.x = 5*WIDTH + 2*BORDER_SIZE
        textRect.y = textSize
        screen.blit(text, textRect)

def quit_game():
        pygame.quit()
        sys.exit()

class Environment:
        
        def __init__(self):
                # Initialize dictionary of locations with objects
                self.item_locations = dict.fromkeys([(x,y) for x in range(WIDTH) for y in range(HEIGHT)], Space(x,y))

                # Sprite list of all entities
                self.theCarrots = pygame.sprite.Group()
                self.theObstacles = pygame.sprite.Group()
                self.theBunny = pygame.sprite.Group()

                # Add the bunny
                self.bunny = Bunny()
                self.item_locations[self.bunny.rect.bottomleft] = self.bunny
                self.theBunny.add(self.bunny)

        def place_carrot(self, carrot):
                self.item_locations[carrot.rect.bottomleft] = carrot
                self.theCarrots.add(carrot)

        def place_obstacle(self, obstacle):
                self.item_locations[obstacle.rect.bottomleft] = obstacle
                self.theObstacles.add(obstacle)
        
        def step(self, item):
                (x, y) = item.rect.bottomleft
                self.item_locations[(x, y)] = Space(x,y)
                item.rect.left -= 5
                self.item_locations[(item.rect.left, y)] = item
                
        def remove_carrot(self, carrot):
                (x, y) = carrot.rect.bottomleft
                self.theCarrots.remove(carrot)
                self.item_locations[(x, y)] = Space(x, y)

        def remove_obstacle(self, obstacle):
                (x, y) = obstacle.rect.bottomleft
                self.theObstacles.remove(obstacle)
                self.item_locations[(x, y)] = Space(x, y)
                
        """

        def display_high_score(high_score):
                #displays a high score if available and displays 0 if not available
                pass

        def display_lives(lives_left):
                #displays the amount of lives left
                pass

        def bounce_bunny(bounce_height):
                #takes in a value from the Bunny class to see how high the bunny character will bounce
                self.bunny.bounce(bounce_height)

        def check_collision(bunny, score):
                #checks to see what it is colliding with
                carrot = Carrot()
                obstacle = Obstacle()
                if self.bunny.rect.colliderect(carrot):
                        self.bunny.carrots += 1
                #Remove carrot
                if self.bunny.rect.colliderect(obstacle):
                        self.bunny.lives -= 1
                #Remove obstacle
        """

class Entity(pygame.sprite.Sprite):

        def __init__(self):
                super(Entity, self).__init__()
                self.name_of_image = ""
                self.size = 0

        def create_image(self):
                self.set_rect()
                self.set_pic()

        def set_rect(self):
                self.rect = pygame.Surface([self.size, self.size]).get_rect()
                self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM)

        def set_pic(self):
                self.image = pygame.image.load(self.name_of_image).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))

class Bunny(Entity):

        def __init__(self):
                super(Bunny, self).__init__()
                self.name_of_image = "bunny.png"
                self.size = BUNNY_SIZE
                self.set_rect()
                self.rect.centerx = BORDER_SIZE + WIDTH/2 # Keeps bunny centered at all times
                self.set_pic()

                # self.lives = 3
                self.carrots = 0

        def bounce(self, bounce_count, height):
                if bounce_count < height/5:
                        self.rect.centery -= 10
                elif bounce_count < 2*height/5:
                        self.rect.centery -= 5
                elif bounce_count < 3*height/5:
                        self.rect.centery +=0
                elif bounce_count < 4*height/5:
                        self.rect.centery += 5
                else:
                        self.rect.centery += 10

class Obstacle(Entity):
        def __init__(self):
                super(Obstacle, self).__init__()

class Carrot(Obstacle):
        def __init__(self):
                super(Carrot, self).__init__()
                self.name_of_image = "carrot.png"
                self.size = CARROT_SIZE
                self.create_image()

class Tree_Short(Obstacle):
        def __init__(self):
                super(Tree_Short, self).__init__()
                self.name_of_image = "lemon-tree.png"
                self.size = TREE_SIZE
                self.create_image()

class Tree_Tall(Obstacle):
        def __init__(self):
                super(Tree_Tall, self).__init__()
                self.name_of_image = "apple-tree.png"
                self.size = TREE_SIZE
                self.rect = pygame.Surface([self.size, 2*self.size]).get_rect()
                self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM)
                self.image = pygame.image.load(self.name_of_image).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (self.size, 2*self.size))

class Rock(Obstacle):
        def __init__(self):
                super(Rock, self).__init__()
                self.name_of_image = "rock.png"
                self.size = ROCK_SIZE
                self.create_image()

class Fire(Obstacle):
        def __init__(self):
                super(Fire, self).__init__()
                self.name_of_image = "fire.png"
                self.size = FIRE_SIZE
                self.create_image()

class Wolf(Obstacle):
        def __init__(self):
                super(Wolf, self).__init__()
                self.name_of_image = "wolf.png"
                self.size = WOLF_SIZE
                self.create_image()

class Space(Entity):
        def __init__(self, x, y):
                super(Space, self).__init__()
                self.name_of_image = "blank.png"
                self.size = 1
                self.set_rect()
                self.rect.bottomleft = (x, y)
                self.set_pic()

if __name__ == "__main__":
        new_game()
