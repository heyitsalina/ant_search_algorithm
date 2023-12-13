import numpy as np

class Simulation:
    """
    This class represents the simulation in which the ants are moving and the obstacles, food are.
    ...

    Attributes
    ----------
    ants : list
    pheromons : numpy array
        A 2D numpy array representing the positions of the pheromons on a grid. 
    food : list
        A list containing the Food objects.
    colonie : list
        A list containing the colonie objects.
    running : bool
        Indicates if the simulation in running.
    
    Methods
    -------
    start():
        Start the simulation.
    next_epoch():
        Calculates the next position of all Ant objects.
    """
    def __init__(self):
        self.ants = []
        self.pheromons = np.zeros((90, 160))
        self.food = []
        self.colonie = []
        self.running = False

    def start(self):
        self.running = not self.running
        while self.running:
            self.next_epoch()

    def next_epoch(self):
        for ant in self.ants:
            ant.move()