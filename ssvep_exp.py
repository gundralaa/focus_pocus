import pygame
import pygame.constants
import pygame.locals
import time 


# Experiment Class 

class Experiment: 

	def __init__(self, width, height): 
		start_time = time.time()

		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()


		self.left_image = pygame.image.load("left_image.png")
		self.left_blit = pygame.image.load("left_blit.jpg")
		self.right_image = pygame.image.load("right_image.png")
		self.right_blit = pygame.image.load("right_blit.jpg")
		self.background = pygame.image.load("background.jpg")

		end = False 

		
		self.clock.tick(60)
		self.screen.blit(self.background, (0,0))
		self.screen.blit(self.left_image, (100, 200))
		self.screen.blit(self.right_image, (700, 200))


		header = pygame.display.set_caption("Welcome to the SSVEP experiment, please focus at a target!")

		off1 = False 
		off2 = False 
		while end != True:
			if (not off1 and int(round((time.time() - start_time) % 0.05, 0)) == 0):
				self.screen.blit(self.left_blit, (0,0))
				pygame.display.flip()
				off1 = True 
			elif (off1 and int(round((time.time() - start_time) % 0.1, 0)) == 0):
				self.screen.blit(self.left_image, (100, 200))
				pygame.display.flip()
				off1 = False
			pygame.display.flip()
			if (not off2 and int(round((time.time() - start_time) % 0.1, 0)) == 0):
				self.screen.blit(self.right_blit, (680,0))
				pygame.display.flip()
				off2 = True 
			elif (off2 and int(round((time.time() - start_time) % 0.2, 0)) == 0):
				self.screen.blit(self.right_image, (700, 200))
				pygame.display.flip()
				off2 = False
		


			# This for loop ensures that if the user closes the pygame window, then the game will end.  

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					end = True


# The code below is used to execute the game, as well as giving the dimensions of the game screen (1200 x 720).

if __name__ == '__main__':
        expr = Experiment(1200, 720)
         

