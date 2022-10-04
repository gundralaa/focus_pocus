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
            stimulus.size = 1
            stimulus.draw()
            win.flip()
            core.wait(0.5)
        
expr = Experiment(500, 500)
