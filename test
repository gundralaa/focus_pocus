import pygame

#----------------------------------------------------------------------

class Background():

    def __init__(self, screen):
        self.screen = screen

        self.timer = 0
        self.color = 0
        self.up = True # up or down

    #-------------------

    def change(self):

        if self.timer == 60: # 15 frames for UP and 15 frames for DOWN
            self.timer = 0
            self.up = not self.up

        self.timer += 1

        if self.up:
            self.color += 1
        else:
            self.color -= 1

        print(self.up, self.color)

    #-------------------

    def draw(self):
        self.screen.fill((self.color, self.color, self.color))

#----------------------------------------------------------------------

class Game():

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800,600))

        self.background = Background(self.screen)

    #-------------------

    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True

        while RUNNING:

            # ----- events -----

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False

            # ----- changes -----

            self.background.change()

            # ----- draws ------

            self.background.draw()

            pygame.display.update()

            # ----- FPS -----

            clock.tick(30)

        #-------------------

        pygame.quit()

#----------------------------------------------------------------------

Game().run()