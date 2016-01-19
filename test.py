# bunnybounce.py
# Created 1/17/2016 by Claudia Wu, Illina Yang, Wings Yeung, Diane Zhou

import pygame, sys
import random

"""
Dimensions
"""
WIDTH = 1000 # game screen width
HEIGHT = 600 # game screen height
MESSAGE_WIDTH = 200 # text prompt screen width
BORDER_SIZE = 10 # border around game screen size
GROUND = HEIGHT * 4/5 # y-position of "ground" in game
BUNNY_LOC = WIDTH/4 # x-position of the bunny

"""
Image Sizes
"""
BUNNY_SIZE = 50
CARROT_SIZE = 50
TREE_TALL_WIDTH = 150
TREE_TALL_HEIGHT = 200
TREE_SHORT_SIZE = 100
ROCK_SIZE = 25
FIRE_SIZE = 50
WOLF_SIZE = 75
<<<<<<< HEAD

"""
Gameplay Variables
"""
VELOCITY = 15 # Default initial velocity of bunny bouncing up
ACCELERATION = 1 # Amount velocity decreases per time step
POWER = 5 # Additional velocity per space bar pressed by player
PLACEMENT_TIME = 10 # How often carrots show up
STEP = 7 # Number of pixels carrots and obstacles move per time step
POSSIBILITIES = 100 # The smaller this number (a denominator), the more often obstacles show up
POSSIBILITIES_MIN = 20
HARDER_TIME = 200 # How often the game gets harder (more obstacles show up)
HARDER = 5 # How much POSSIBILITIES decreases per HARDER_TIME time steps

"""
RGB Color Definitions
"""
=======
BOTTOM = HEIGHT * 4/5
BOUNCE_HEIGHT = 25

# RGB Color Definitions
>>>>>>> origin/master
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def new_game():

	# Initialize gameplay environment.
	pygame.init()
	window_size = (WIDTH + MESSAGE_WIDTH + 3*BORDER_SIZE, HEIGHT + 2*BORDER_SIZE)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Bunny Bounce")
	env = Environment()

	# Player presses space bar to start the game.
	message = ["Press space bar to start."]
	update_screen(screen, env, message)
	start = False
	while start is False:
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				start = True
				main_loop(screen, env)
		elif pygame.QUIT in event_types:
			break

	#***additional feature to do if time
	"""
	if env.bunny.carrots >= high_score:
	#       with open('saved_state.txt', 'w') as f:
	#               f.write( str(env.bunny.carrot ) )
	"""

	quit_game()

def main_loop(screen, env):
<<<<<<< HEAD
	
	message = ["carrot number"] # display score = 0
=======

	end = False
	message = ["Hello"] # display lives = 3, score = 0
>>>>>>> origin/master
	update_screen(screen, env, message)
	# high_score = 0

	loop_count = 0 # Keeps track of number of iterations of loop below

	# Initialize variables with default / initial values
	velocity = VELOCITY
	new_velocity = VELOCITY
	possibilities = POSSIBILITIES

	end = False
	while end is False:

		"""
		Every iteration of the loop:
		-Move all carrots and obstacles to the left.
		-Check for player input.
		-Bunny bounce movement.
		"""

		# Move all items to the left.
		for item in env.theCarrots:
			item.rect.left -= STEP 
		for item in env.theObstacles:
			item.rect.left -= STEP

		# Remove items that have reached the left side of the screen.
		for carrot in env.theCarrots:
			if carrot.rect.left < BORDER_SIZE:
<<<<<<< HEAD
				env.theCarrots.remove(carrot)
		for obstacle in env.theObstacles:
			if obstacle.rect.left < BORDER_SIZE:
				env.theObstacles.remove(obstacle)
=======
				env.remove_carrot(carrot)
		for obstacle in env.theObstacles:
			if obstacle.rect.left < BORDER_SIZE:
				env.remove_obstacle(obstacle)
>>>>>>> origin/master

		# Bounce movement
		env.bunny.rect.bottom -= velocity # Up = pixel index decreasing
		#env.bunny.bounce(velocity) #***might not need this***
		velocity -= ACCELERATION # Velocity decreases after each time step (think physics & gravity)
		if env.bunny.rect.bottom >= GROUND: # Reset velocity when bunny reaches ground
			velocity = new_velocity
			new_velocity = VELOCITY

		update_screen(screen, env, message)

		# If player presses space bar, next bounce will be higher.
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				new_velocity += POWER
		elif pygame.QUIT in event_types:
			end = True

		"""
		Every PLACEMENT_TIME iterations of the loop:
		-Place a carrot.
		-Randomly choose whether to place an obstacle and which obstacle to place.
		"""

<<<<<<< HEAD
		if loop_count % PLACEMENT_TIME == 0:

			env.theCarrots.add(Carrot()) # Place a carrot
			#env.place_carrot(Carrot()) #***might not need this***

			# The result of a random integer determines which obstacle, if any, shows up.
			num = random.randint(0, possibilities)
			if num in range(0, 1):
				env.theObstacles.add(Tree_Tall())
				#env.place_obstacle(Tree_Tall()) #***might not need this***
			elif num in range(1, 3):
				env.theObstacles.add(Tree_Short())
				#env.place_obstacle(Tree_Short()) #***might not need this***
			elif num in range(3, 6):
				env.theObstacles.add(Rock())
				#env.place_obstacle(Rock()) #***might not need this***
			elif num in range(6, 8):
				env.theObstacles.add(Fire())
				#env.place_obstacle(Fire()) #***might not need this***
			elif num in range(8, 10):
				env.theObstacles.add(Wolf())
				#env.place_obstacle(Wolf()) #***might not need this***
		
		"""
		Every HARDER_TIME iterations of the loop, decrease <possibilities>.
		As <possibilities> decreases, the probability of generating an integer representing
		an obstacle increases, making the game harder.
		"""
		if loop_count == HARDER_TIME:
			loop_count = 0
			if possibilities > POSSIBILITIES_MIN:
				possibilities -= HARDER
=======
		if loop_count % 10 == 0:
			#env.place_carrot(Carrot())

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
>>>>>>> origin/master

		"""
		Update screen and loop_count before allowing next iteration to run.
		"""
		update_screen(screen, env, message)
		loop_count += 1

		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.QUIT in event_types:
			end = True

<<<<<<< HEAD
=======
	message = ["Hello"]
	update_screen(screen, env, message)

		# if env.bunny.carrots >= high_score:
	#       with open('saved_state.txt', 'w') as f:
	#               f.write( str(env.bunny.carrot ) )

>>>>>>> origin/master
def update_screen(screen, env, message = []):
	"""
	Update images and text prompts on the screen.
	"""
	screen.fill(BLACK) # change color later or insert image
	pygame.draw.lines(screen, WHITE, False, [(BORDER_SIZE, GROUND), (BORDER_SIZE+WIDTH, GROUND)], 1)
	for _ in range(len(message)):
		update_text(screen, message, _)
	env.theCarrots.draw(screen)
	env.theObstacles.draw(screen)
	env.theBunny.draw(screen)
	pygame.display.flip()

def update_text(screen, message, index, textSize = 20):
	"""
	Update the image of the text on the screen.
	"""
	font = pygame.font.Font(None, textSize)
	text = font.render(message[index], True, WHITE, BLACK)
	textRect = text.get_rect()
	textRect.x = WIDTH + 2*BORDER_SIZE
	textRect.y = textSize
	screen.blit(text, textRect)

def quit_game():
	"""
	Quit the game and close the program.
	"""
	pygame.quit()
	sys.exit()

class Environment:
<<<<<<< HEAD
	
=======

>>>>>>> origin/master
	def __init__(self):
		
		# Initialize dictionary of locations with objects
		#self.item_locations = dict.fromkeys([(x,y) for x in range(WIDTH) for y in range(HEIGHT)], Space(x,y))
		#***might not need this dictionary***

		# Sprite groups of all entities
		self.theCarrots = pygame.sprite.Group()
		self.theObstacles = pygame.sprite.Group()
		self.theBunny = pygame.sprite.Group()

		# Add the bunny to the environment
		self.bunny = Bunny()
		#self.item_locations[self.bunny.rect.bottomleft] = self.bunny
		self.theBunny.add(self.bunny)

	#***might not need these methods***
	"""
	def place_carrot(self, carrot):
		#self.item_locations[carrot.rect.bottomleft] = carrot
		self.theCarrots.add(carrot)

	def place_obstacle(self, obstacle):
		#self.item_locations[obstacle.rect.bottomleft] = obstacle
		self.theObstacles.add(obstacle)
	
	def step(self, item):
<<<<<<< HEAD
		#(x, y) = item.rect.bottomleft
		#self.item_locations[(x, y)] = Space(x,y)
		item.rect.left -= STEP
		#self.item_locations[(item.rect.left, y)] = item
		
	def remove_carrot(self, carrot):
		#(x, y) = carrot.rect.bottomleft
		self.theCarrots.remove(carrot)
		#self.item_locations[(x, y)] = Space(x, y)

	def remove_obstacle(self, obstacle):
		#(x, y) = obstacle.rect.bottomleft
		self.theObstacles.remove(obstacle)
		#self.item_locations[(x, y)] = Space(x, y)
	"""

	#***methods we might need to write***
	"""
=======
		(x, y) = item.rect.bottomleft
		self.item_locations[(x, y)] = Space(x,y)
		item.rect.left -= 5
		self.item_locations[(item.rect.left, y)] = item

	def remove_carrot(self, carrot):
		(x, y) = carrot.rect.bottomleft
		self.theCarrots.remove(carrot)
		self.item_locations[(x, y)] = Space(x, y)
>>>>>>> origin/master

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
<<<<<<< HEAD

	"""
	All items in the game are in this class. Subclasses:
	-Bunny
	-Obstacle
	-Space #***might not need this class***
	"""
=======
>>>>>>> origin/master

	def __init__(self):
		super(Entity, self).__init__()
		self.name_of_image = ""
		self.size = 0

	def create_image(self):
		self.set_rect()
		self.set_pic()

	def set_rect(self):
		self.rect = pygame.Surface([self.size, self.size]).get_rect()
<<<<<<< HEAD
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, GROUND)
=======
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM)
>>>>>>> origin/master

	def set_pic(self):
		self.image = pygame.image.load(self.name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))

class Bunny(Entity):

	def __init__(self):
		super(Bunny, self).__init__()
		self.name_of_image = "bunny.png"
		self.size = BUNNY_SIZE
		self.set_rect()
		self.rect.centerx = BORDER_SIZE + BUNNY_LOC
		self.set_pic()

		# self.lives = 3 #***additional feature***
		self.carrots = 0

<<<<<<< HEAD
	def bounce(self, velocity): #***might not need this method***
		self.rect.bottom -= velocity
=======
	def bounce(self, bounce_count, height):
		if bounce_count < height:
			self.rect.centery -= 10
		else:
			self.rect.centery += 10
>>>>>>> origin/master

class Obstacle(Entity):
	"""
	All items moving across the screen in the game are in this class. Subclasses:
	-Carrot
	-Tree_Short
	-Tree_Tall
	-Rock
	-Fire
	-Wolf
	"""
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
		self.size = TREE_SHORT_SIZE
		self.create_image()

class Tree_Tall(Obstacle):
	def __init__(self):
		super(Tree_Tall, self).__init__()
		self.name_of_image = "apple-tree.png"
<<<<<<< HEAD
		self.size = TREE_TALL_WIDTH
		self.rect = pygame.Surface([TREE_TALL_WIDTH, TREE_TALL_HEIGHT]).get_rect()
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - TREE_TALL_WIDTH, GROUND)
		self.image = pygame.image.load(self.name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (TREE_TALL_WIDTH, TREE_TALL_HEIGHT))
=======
		self.size = TREE_SIZE
		self.rect = pygame.Surface([self.size, 2*self.size]).get_rect()
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, BOTTOM)
		self.image = pygame.image.load(self.name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (self.size, 2*self.size))
>>>>>>> origin/master

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

<<<<<<< HEAD
class Space(Entity): #***might not need this class***
=======
class Space(Entity):
>>>>>>> origin/master
	def __init__(self, x, y):
		super(Space, self).__init__()
		self.name_of_image = "blank.png"
		self.size = 1
		self.set_rect()
		self.rect.bottomleft = (x, y)
		self.set_pic()

if __name__ == "__main__":
	new_game()
