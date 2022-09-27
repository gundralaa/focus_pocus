import pygame
import pygame.constants
import pygame.locals


# Experiment Class 

class Experiment: 

	def __init__(self, width, height): 
		pygame.init()
		self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))


        self.left_image = pygame.image.load("left_image.png")
        self.right_image = pygame.image.load("right_image.png")
        self.background = pygame.image.load("background.jpg")
        self.rounds = 0
        self.left_rep = 10 
        self.right_rep = 7.5
        end = False 


        header = pygame.display.set_caption("Welcome to the SSVEP experiment, please focus at a target!")


        while end != True: 

			self.screen.blit(background, (0,0))
        	self.screen.blit(self.left_image, (10, 50))
        	self.screen.blit(self.right_image, (300, 500))

        	# This for loop ensures that if the user closes the pygame window, then the game will end.  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True


            if self.rounds > 5: 
            	end = True 








# The code below is used to execute the game, as well as giving the dimensions of the game screen (1200 x 720).

if __name__ == '__main__':
        expr = Experiment(1200, 720)
         



