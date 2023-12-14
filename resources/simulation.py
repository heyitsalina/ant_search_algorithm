import numpy as np

class Simulation:
    """
    This class represents the simulation in which the ants are moving and the 
    Colony and Food objects are.
    ...

    Attributes
    ----------
    pheromones : numpy array
        A 2D numpy array representing the positions of the pheromones on a grid. 
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
    update_pheromone():
        Update the array of pheromones.
    add_colony():
        Add a Colony object to the simulation.
    add_food():
        Add a Food object to the simulation.
    """
    def __init__(self):
        self
        self.pheromones = np.zeros((90, 160))
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
                self.update_pheromone(ant)
                ant.move()
    
    def update_pheromone(self, ant):
        # This will certainly not work, but just to understand the basic idea
        # if ant.pheromone_status ist 1 or -1
        x, y = ant.coordinates
        self.pheromones[x][y] += ant.pheromon_status

    def add_colony(self, colony):
        self.colonies.append(colony)

    def add_food(self, food):
        self.food.append(food)
        