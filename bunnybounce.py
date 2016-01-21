# bunnybounce.py
# Created 1/17/2016 by Claudia Wu, Illina Yang, Wings Yeung, Diane Zhou

import pygame, sys, random
from example_menu import main as menu

"""
Dimensions
"""
WIDTH = 1000 # game screen width
HEIGHT = 600 # game screen height
MESSAGE_WIDTH = 200 # text prompt screen width
BORDER_SIZE = 20 # border around game screen size
WINDOW_SIZE = (WIDTH + MESSAGE_WIDTH + 3*BORDER_SIZE, HEIGHT + 2*BORDER_SIZE)
TEXT_SIZE = 30 # size of text on screen
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
ROCK_SIZE = 50
FIRE_SIZE = 50
WOLF_SIZE = 75

"""
Gameplay Variables
"""
VELOCITY = 10 # Default initial velocity of bunny bouncing up
ACCELERATION = 1 # Amount velocity decreases per time step
POWER = 5 # Additional velocity per spacebar pressed by player
PLACEMENT_TIME = 10 # How often carrots show up
STEP = 7 # Number of pixels carrots and obstacles move per time step
POSSIBILITIES = 100 # The smaller this number (a denominator), the more often obstacles show up
POSSIBILITIES_MIN = 20
HARDER_TIME = 200 # How often the game gets harder (more obstacles show up)
HARDER = 5 # How much POSSIBILITIES decreases per HARDER_TIME time steps

"""
RGB Color Definitions
"""
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def init_game():
	"""
	Initialize the game with the menu screen.
	If the player chooses "Play Game", <menu> method returns "None".
	"""
	pygame.init()
	pygame.display.set_caption("Bunny Bounce")
	if menu(pygame.display.set_mode(WINDOW_SIZE)) is None:
		new_game()

def new_game():

	# Set up gameplay environment.
	screen = pygame.display.set_mode(WINDOW_SIZE)
	env = Environment()

	# Pass in previous highest score.
	with open('saved_state.txt', 'r') as f:
		high_score = f.readline()

	# Player presses spacebar to start the game.
	message = ["Press spacebar to"]
	message.append("start.")
	update_screen(screen, env, message)
	start = False
	score = 0
	while start is False:
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				start = True
				main_loop(screen, env, high_score)
		elif pygame.QUIT in event_types:
			quit_game()

def main_loop(screen, env, high_score):

	message = ["Current Score: 0"]
	message.append("High Score: " + str(high_score))
	update_screen(screen, env, message)

	loop_count = 0 # Keeps track of number of iterations of loop below

	# Initialize variables with default / initial values
	velocity = VELOCITY
	new_velocity = VELOCITY
	possibilities = POSSIBILITIES

	while 1:

		"""
		Every iteration of the loop:
		-Move all carrots and obstacles to the left.
		-Check for collision with carrots and obstacles.
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
				env.theCarrots.remove(carrot)
		for obstacle in env.theObstacles:
			if obstacle.rect.left < BORDER_SIZE:
				env.theObstacles.remove(obstacle)

		# Check for collision with carrots. Update score as necessary.
		if env.collision_carrot():
			env.bunny.score += 1
			message[0] = "Current Score: " + str(env.bunny.score)

		# Check for collision with obstacles.
		# Game ends if there is collision.
		if env.collision_obstacle():
			end_game(screen, env, high_score)
			return

		# Bounce movement
		env.bunny.rect.bottom -= velocity # Up = pixel index decreasing
		velocity -= ACCELERATION # Velocity decreases after each time step (think physics & gravity)
		if env.bunny.rect.bottom >= GROUND: # Reset velocity when bunny reaches ground
			velocity = new_velocity
			new_velocity = VELOCITY

		update_screen(screen, env, message)

		# If player presses spacebar, next bounce will be higher.
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.KEYDOWN in event_types:
			for action in events:
				if action.key == pygame.K_SPACE:
					new_velocity += POWER
					break
		elif pygame.QUIT in event_types:
			quit_game()

		"""
		Every PLACEMENT_TIME iterations of the loop:
		-Place a carrot.
		-Randomly choose whether to place an obstacle and which obstacle to place.
		"""

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

		"""
		Update screen and loop_count before allowing next iteration to run.
		"""
		update_screen(screen, env, message)
		loop_count += 1

		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.QUIT in event_types:
			quit_game()

def update_screen(screen, env, message = []):
	"""
	Update images and text prompts on the screen.
	"""
	screen.fill(BLACK)
	for _ in range(len(message)):
		update_text(screen, message, _)
	env.theBackground.draw(screen)
	env.theCarrots.draw(screen)
	env.theObstacles.draw(screen)
	env.theBunny.draw(screen)
	pygame.display.flip()

def update_text(screen, message, index, textSize = 20):
	"""
	Update the image of the text on the screen.
	"""
	font = pygame.font.Font(None, TEXT_SIZE)
	text = font.render(message[index], True, WHITE, BLACK)
	textRect = text.get_rect()
	textRect.x = WIDTH + 2*BORDER_SIZE
	textRect.y = (index+1) * TEXT_SIZE
	screen.blit(text, textRect)

def end_game(screen, env, high_score):

	"""
	When the game ends:
	-Display the player's score. #and the high score ***additional feature***
	-Allow the player to play again or quit.
	"""

	message = ["Your score: " + str(env.bunny.score)]
	if env.bunny.score > high_score:
		message.append("New high score!")
		with open('saved_state.txt', 'w') as f:
			f.write( str(env.bunny.score ) )
	else:
		message.append("High score: " + str(high_score))
	message.append("")
	message.append("Press spacebar to ")
	message.append("play again.")
	message.append("")
	message.append("Close window to ")
	message.append("quit.")
	update_screen(screen, env, message)
	
	response = False
	while response is False:
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.KEYDOWN in event_types:
			if events[0].key == pygame.K_SPACE:
				new_game()
				response = True
		elif pygame.QUIT in event_types:
			quit_game()

def quit_game():
	"""
	Quit the game and close the program.
	"""
	pygame.quit()
	sys.exit()

class Environment:

	def __init__(self):

		# Sprite groups of all entities
		self.theCarrots = pygame.sprite.Group()
		self.theObstacles = pygame.sprite.Group()
		self.theBunny = pygame.sprite.Group()
		self.theBackground = pygame.sprite.Group()

		# Add the bunny to the environment
		self.bunny = Bunny()
		#self.item_locations[self.bunny.rect.bottomleft] = self.bunny
		self.theBunny.add(self.bunny)

		# Add the background to the environment
		self.add_background()

	def add_background(self):
		background = Entity()
		background.rect = pygame.Surface([WIDTH, HEIGHT]).get_rect()
		background.rect.topleft = (BORDER_SIZE, BORDER_SIZE)
		background.image = pygame.image.load("background.png").convert_alpha()
		background.image = pygame.transform.smoothscale(background.image, (WIDTH, HEIGHT))
		self.theBackground.add(background)

	"""
	Check for collision between bunny and items (carrots and obstacles).
	"""

	def collision_carrot(self):
		carrots = [carrot.rect for carrot in self.theCarrots]
		index = self.bunny.rect.collidelist(carrots)
		if index != -1:
			self.theCarrots.remove(self.theCarrots.sprites()[index])
			return True
		return False

	def collision_obstacle(self):
		obstacles = [obstacle.rect for obstacle in self.theObstacles]
		index = self.bunny.rect.collidelist(obstacles)
		if index != -1:
			self.theObstacles.remove(self.theObstacles.sprites()[index])
			return True
		return False

	#***methods we might need to write***
	"""

	def display_high_score(high_score):
		#displays a high score if available and displays 0 if not available
		pass
	"""

class Entity(pygame.sprite.Sprite):

	"""
	All items in the game are in this class. Subclasses:
	-Bunny
	-Obstacle
	-Space #***might not need this class***
	"""

	def __init__(self):
		super(Entity, self).__init__()
		self.name_of_image = ""
		self.size = 0

	def create_image(self):
		self.set_rect()
		self.set_pic()

	def set_rect(self):
		self.rect = pygame.Surface([self.size, self.size]).get_rect()
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - self.size, GROUND)

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
		self.score = 0 # corresponds to number of carrots collected

	def bounce(self, velocity): #***might not need this method***
		self.rect.bottom -= velocity

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
		self.size = TREE_TALL_WIDTH
		self.rect = pygame.Surface([TREE_TALL_WIDTH, TREE_TALL_HEIGHT]).get_rect()
		self.rect.bottomleft = (BORDER_SIZE + WIDTH - TREE_TALL_WIDTH, GROUND)
		self.image = pygame.image.load(self.name_of_image).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, (TREE_TALL_WIDTH, TREE_TALL_HEIGHT))

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

if __name__ == "__main__":
	init_game()



