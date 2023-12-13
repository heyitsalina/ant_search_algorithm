import numpy as np
from resources.colony import Colony

class Simulation:
    """
    This class represents the simulation in which the ants are moving and the obstacles, food are.
    ...

    Attributes
    ----------
    pheromons : numpy array
        A 2D numpy array representing the positions of the pheromons on a grid. 
    food : list
        A list containing the Food objects.
    colonies : list
        A list containing the colonie objects.
    running : bool
        Indicates if the simulation in running.
    
    Methods
    -------
    start():
        Start the simulation.
    next_epoch():
        Calculates the next position of all Ant objects.
    add_colony():
        Add a Colony object to the simulation.
    add_food():
        Add a Food object to the simulation.
    """
    def __init__(self):
        self
        self.pheromons = np.zeros((90, 160))
        self.food = []
        self.colonies = []
        self.running = False

    def start(self):
        self.running = not self.running
        while self.running:
            self.next_epoch()

    def next_epoch(self):
        for colony in self.colonies:
            for ant in colony.ants:
                ant.move()
                
    def add_colony(self, colony):
        self.colonies.append(colony)

    def add_food(self, food):
        self.food.append(food)
        