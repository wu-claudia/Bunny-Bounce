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

# main_loop(screen, env)

def main_loop(screen, env):

	end = False
	message = [] # display lives = 3, score = 0
	update_screen(screen, env, message)
	high_score = 0

	events = pygame.event.get() #Contains entire events
	event_types = [event.type for event in events]
	while pygame.QUIT not in event_types:
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
	env.theEntities.draw(screen)
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

		self.item_locations = dict.fromkeys([(x,y) for x in range(WIDTH) for y in
												range(HEIGHT)])
		self.theItems = pygame.sprite.Group() #Sprite list of the bunny and the items

		self.bunny = Bunny()
		self.carrot = Carrot()
		self.theItems.add(self.bunny)
		self.item_locations[(self.bunny.rect.centerx, self.bunny.rect.centery)] = self.bunny

def place_item(item, i, j):
	# places a type of item at the specified coordinates (i, j)
	pass
def remove_item(item):
	#removes an item from its previous location
	pass
def display_high_score(high_score):
	#displays a high score if available and displays 0 if not available
	pass
def display_lives(lives_left):
	#displays the amount of lives left
	pass
def bounce_bunny(bounce_height):
	#takes in a value from the Bunny class to see how high the bunny character will bounce
	self.bunny.bounce()

def check_collision(bunny, score):
	#checks if the bunny has collided with an obstacle or carrot by comparing location
	if abs(self.carrot.rect.centerx) < (BUNNY_SIZE + CARROT_SIZE) and abs(self.carrot.rect.centery - self.bunny.rect.centery) < (BUNNY_SIZE + CARROT_SIZE):
		self.bunny.carrots += 1
	#Remove carrot
	if abs(self.obstacle.rect.centerx) < (BUNNY_SIZE + CARROT_SIZE) and abs(self.obstacle.rect.centery - self.bunny.rect.centery) < (BUNNY_SIZE + CARROT_SIZE):
		self.bunny.lives -= 1
	#Remove obstacle

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		super(Entity, self).__init__()

class Bunny(Entity):
	def __init__(self):
		super(Bunny, self).__init__()
		self.image = pygame.image.load("bunny.png").convert_alpha()
		self.rect = pygame.Surface([BUNNY_SIZE, BUNNY_SIZE]).get_rect()
		self.rect.centerx = WIDTH/2 #Keeps bunny centered at all times
		self.rect.centery = HEIGHT*4/5
		self.lives = 3
		self.carrots = 0

	def bounce(self):
		#moves the bunny up
		self.rect.centery += BUNNY_SIZE
		self.rect.centery -= BUNNY_SIZE

class Item(Entity):
	def __init__(self):
		super(Item, Entity).__init__()
		# self.item_list =
		# self.item_type =
	def move_item(self):
		#updates location of obstacles
		pass

class Carrot(Item):
	def __init__(self, y):
		super(Carrot, self).__init__()
		self.image = pygame.image.load("carrot.png")
		self.rect = pygame.Surface([CARROT_SIZE, CARROT_SIZE]).get_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH - CARROT_SIZE/2
		self.rect.centery = y

class Obstacle(Item):
	def __init__(self):
		super(Obstacle, self).__init__()
	# tree(different heights), rock, wolf, fire

class Tree_Tall(Obstacle):
	def __init__(self):
		super(Tree_Tall, self).__init__()
		self.image = pygame.image.load("apple-tree.png").convert_alpha()
		self.rect = pygame.Surface([TREE_SIZE, 2*TREE_SIZE]).get_rect()
		# self.rect.centerx =
		# self.rect.centery =

class Tree_Short(Obstacle):
	def __init__(self):
		super(Tree_Short, self).__init__()
		self.image = pygame.image.load("lemon-tree.png").convert_alpha()
		self.rect = pygame.Surface([TREE_SIZE, TREE_SIZE]).get_rect()

class Rock(Obstacle):
	def __init__(self):
		super(Rock, self).__init__()
		self.image = pygame.image.load("rock.png").convert_alpha()
		self.rect = pygame.Surface([ROCK_SIZE, ROCK_SIZE]).get_rect()
		# self.rect.centerx =
		# self.rect.centery =

class Fire(Obstacle):
	def __init__(self):
		super(Fire, self).__init__()
		self.image = pygame.image.load("fire.png").convert_alpha()
		self.rect = pygame.Surface([FIRE_SIZE, FIRE_SIZE]).get_rect()
		# self.rect.centerx =
		# self.rect.centery =

if __name__ == "__main__":
	new_game()
