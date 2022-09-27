import pygame
import pygame.constants
import pygame.locals


# Experiment Class 

class Experiment: 

	def __init__(self, width, height): 
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()


		self.left_image = pygame.image.load("left_image.png")
		self.right_image = pygame.image.load("right_image.png")
		self.background = pygame.image.load("background.jpg")
		self.rounds = 0
		self.left_rep = 10 
		self.right_rep = 7.5
		end = False 


		header = pygame.display.set_caption("Welcome to the SSVEP experiment, please focus at a target!")


		while end != True:
			pygame.display.flip()
			self.clock.tick(60)
			self.screen.blit(self.background, (0,0))


			




			self.screen.blit(self.left_image, (100, 200))
			self.screen.blit(self.right_image, (700, 200))

			# This for loop ensures that if the user closes the pygame window, then the game will end.  

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					end = True


			if self.rounds > 5: 
				end = True 








# The code below is used to execute the game, as well as giving the dimensions of the game screen (1200 x 720).

if __name__ == '__main__':
        expr = Experiment(1200, 720)
         

