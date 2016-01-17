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
	message = [] # display lives = 3, score = 0
	update_screen(screen, env, message)
	high_score = 0

	events = pygame.event.get() #Contains entire events
	event_types = [event.type for event in events]
	while pygame.QUIT not in event_types:
		place_carrot()
		pygame.time.wait(500)
		# get a random int, if int = 0, then place_obstacle(random_int for which obstacle)
		num = random.randint(0, 100)

		#Random chances of obstacles appearing
		if num in range(0, 10):
			place_obstacle(Tree_Tall())
		elif num in range(10, 15):
			place_obstacle(Tree_Small())
		elif num in range(15, 30):
			place_obstacle(Rock())
		elif num in range(30, 35):
			place_obstacle(Fire())
		elif num in range(35, 45):
			place_obstacle(Wolf())

		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				env.bunny.bounce()
	if env.bunny.carrot >= high_score:
		with open('saved_state.txt', 'w') as f:
			f.write( str(env.bunny.carrot ) )

def update_screen(screen, env, message = []):
	screen.fill(BLACK) # change color later or insert image
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
	textRect.y = textSize * (index+1)
	screen.blit(text, textRect)

def quit_game():
	pygame.quit()
	sys.exit()

class Environment:
	def __init__(self):
		# Initialize dictionary of locations with objects
		self.item_locations = dict.fromkeys([(x,y) for x in range(WIDTH) for y in range(HEIGHT)], Space(x,y))

		#Sprite list of all entities
		self.theCarrots = pygame.sprite.Group()
		self.theObstacles = pygame.sprite.Group()
		self.theBunny = pygame.sprite.Group()

		# Add the bunny
		self.bunny = Bunny()
		self.theBunny.add(self.bunny)
		self.item_locations[(self.bunny.rect.centerx, self.bunny.rect.centery)] = 'None'
		self.bunny

	def place_carrot(self):
		self.theCarrots.add(Carrot())

	def place_obstacles(self, obstacle):
		# places a type of item at the specified coordinates (i, j)
		i = 'None'# right side
		j = 'None'# get random number within j range
		self.item_locations[(i,j)] = obstacle

	def remove_item(item):
		#removes an item from its previous location
		x = item.rect.centerx
		y = item.rect.centery
		self.item_locations[(x, y)] = Space(x, y)

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
		if abs(self.carrot.rect.centerx) < (BUNNY_SIZE + CARROT_SIZE) and abs(self.carrot.rect.centery - self.bunny.rect.centery) < (BUNNY_SIZE + CARROT_SIZE):
			self.bunny.carrots += 1
		#Remove carrot
		if abs(self.obstacle.rect.centerx) < (BUNNY_SIZE + CARROT_SIZE) and abs(self.obstacle.rect.centery - self.bunny.rect.centery) < (BUNNY_SIZE + CARROT_SIZE):
			self.bunny.lives -= 1
		#Remove obstacle

class Entity(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Entity, self).__init__()
		self.name_of_image = ""
		self.rect = pygame.Surface([1,1]).get_rect()
		self.rect.centerx = 0
		self.rect.centery = 0

	def set_pic(self):
		self.image = pygame.image.load(name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (self.rect.centerx,
		self.rect.centery))

class Bunny(Entity):
	def __init__(self):
		super(Bunny, self).__init__()
		self.name_of_image = "bunny.png"
		self.rect = pygame.Surface([BUNNY_SIZE, BUNNY_SIZE]).get_rect()
		self.rect.centerx = WIDTH/2 #Keeps bunny centered at all times
		self.rect.centery = BOTTOM - BUNNY_SIZE/2
		self.set_pic()

		self.lives = 3
		self.carrots = 0

	def bounce(self, bunny_height):
		#moves the bunny up
		self.rect.centery += bunny_height
		self.rect.centery -= bunny_height

class Obstacle(Entity):
	def __init__(self):
		super(Obstacle, self).__init__()
	# tree(different heights), rock, wolf, fire

class Carrot(Obstacle):
	def __init__(self, y):
		super(Carrot, self).__init__()
		self.name_of_image = "carrot.png"
		self.rect = pygame.Surface([CARROT_SIZE, CARROT_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH - CARROT_SIZE/2
		self.rect.centery = BOTTOM - CARROT_SIZE/2
		self.set_pic()

class Tree_Tall(Obstacle):
	def __init__(self):
		super(Tree_Tall, self).__init__()
		self.name_of_image = "apple-tree.png"
		self.rect = pygame.Surface([TREE_SIZE, 2*TREE_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE+WIDTH-TREE_SIZE/2
		self.rect.centery = BOTTOM-TREE_SIZE/2
		self.set_pic()

class Tree_Short(Obstacle):
	def __init__(self):
		super(Tree_Short, self).__init__()
		self.name_of_image = "lemon-tree.png"
		self.rect = pygame.Surface([TREE_SIZE, TREE_SIZE]).get_rect()
		self.set_pic()

class Rock(Obstacle):
	def __init__(self):
		super(Rock, self).__init__()
		self.name_of_image = "rock.png"
		self.rect = pygame.Surface([ROCK_SIZE, ROCK_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH - ROCK_SIZE/2
		self.rect.centery = BOTTOM-ROCK_SIZE/2
		self.set_pic()

class Fire(Obstacle):
	def __init__(self):
		super(Fire, self).__init__()
		self.name_of_image = "fire.png"
		self.rect = pygame.Surface([FIRE_SIZE, FIRE_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH - FIRE_SIZE/2
		self.rect.centery = BOTTOM-FIRE_SIZE/2
		self.set_pic()

class Wolf(Obstacle):
	def __init__(self):
		super(Wolf, self).__init__()
		self.name_of_image = "wolf.png"
		self.rect = pygame.Surface([WOLF_SIZE, WOLF_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH - ROCK_SIZE/2
		self.rect.centery = BOTTOM - WOLF_SIZE/2
		self.set_pic()

class Space(Entity):
	def __init__(self, x, y):
		super(Space, self).__init__()
		self.name_of_image = "blank.png"
		self.rect = pygame.Surface([1, 1]).get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.set_pic()

if __name__ == "__main__":
	new_game()
