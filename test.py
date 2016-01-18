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
	message = ["Hello"] # display lives = 3, score = 0
	update_screen(screen, env, message)
	high_score = 0

	events = pygame.event.get() #Contains entire events
	event_types = [event.type for event in events]
	while pygame.QUIT not in event_types:
		env.place_carrot()
		env.step()

		# get a random int, if int = 0, then place_obstacle(random_int for which obstacle)
		num = random.randint(0, 100)

		#Random chances of obstacles appearing
		if num in range(0, 10):
			env.place_obstacle(Tree_Tall())
		elif num in range(10, 15):
			env.place_obstacle(Tree_Short())
		elif num in range(15, 30):
			env.place_obstacle(Rock())
		elif num in range(30, 35):
			env.place_obstacle(Fire())
		elif num in range(35, 45):
			env.place_obstacle(Wolf())

		update_screen(screen, env, message)
		pygame.time.wait(500)

"""
		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				env.bunny.bounce()
	if env.bunny.carrot >= high_score:
		with open('saved_state.txt', 'w') as f:
			f.write( str(env.bunny.carrot ) )
			"""

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
		carrot = Carrot()
		x = carrot.rect.centerx
		y = carrot.rect.centery
		self.item_locations[(x, y)] = carrot
		self.theCarrots.add(carrot)

	def place_obstacle(self, obstacle):
		x = obstacle.rect.centerx
		y = obstacle.rect.centery
		self.item_locations[(x, y)] = obstacle
		self.theObstacles.add(obstacle)

	def step(self, item):
		x = item.rect.centerx
		y = item.rect.centery
		self.item_locations[(x, y)] = Space(x,y)
		x_new = x - 10
		x_new = item.rect.centerx - 10
		self.item_locations[(x_new, y)] = item

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
		carrot = Carrot()
		obstacle = Obstacle()
		if self.bunny.rect.colliderect(carrot):
			self.bunny.carrots += 1
		#Remove carrot
		if self.bunny.rect.colliderect(obstacle):
			self.bunny.lives -= 1
		#Remove obstacle

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
		self.rect.topleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM - self.size)

	def set_pic(self):
		self.image = pygame.image.load(self.name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))

class Bunny(Entity):
	def __init__(self):
		super(Bunny, self).__init__()
		self.name_of_image = "bunny.png"
		self.size = BUNNY_SIZE
		self.set_rect()
		self.rect.centerx = BORDER_SIZE + WIDTH/2 #Keeps bunny centered at all times
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
		self.rect.topleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM - 2*self.size)
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
		self.rect.centerx = x
		self.rect.centery = y
		self.set_pic()

if __name__ == "__main__":
	new_game()
