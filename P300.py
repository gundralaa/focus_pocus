import psychopy
import time

from psychopy import visual, core

# Code for P300

class Experiment: 

    def __init__(self, width, height): 

        self.width = width
        self.height = height

        win = visual.Window([width,height])

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        stimulus = visual.TextStim(win, text='')

        for letter in letters:
            stimulus.setText(letter)
            stimulus.draw()
            win.flip()
            core.wait(2.0)
        
expr = Experiment(500, 500)
