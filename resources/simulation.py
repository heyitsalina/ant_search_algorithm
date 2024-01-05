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
    bounds: Tuple
        defines the spatial boundaries of the simulation area (min_x, max_x, min_y, max_y)
    
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
    check_future_position():    
        Adjusts the given position to ensure it stays within the simulation bounds.
    """
    def __init__(self):
        self.pheromones = np.zeros((90, 160))
        self.food = []
        self.colonies = []
        self.running = False
        self.bounds = () #(min_x, max_x, min_y, max_y)
        
    def start(self):
        self.running = not self.running
        while self.running:
            self.next_epoch()

    def next_epoch(self):
        for colony in self.colonies:
            for ant in colony.ants:
                self.update_pheromone(ant)
                future_position = ant.move()
                adjusted_position = self.check_future_position(future_position)
                ant.coordinates = adjusted_position

    def update_pheromone(self, ant):
        # This will certainly not work, but just to understand the basic idea
        # if ant.pheromone_status ist 1 or -1
        x, y = 0, 0 #ant.coordinates
        self.pheromones[x][y] += ant.pheromone_status
        
    def add_colony(self, colony):
        self.colonies.append(colony)

    def add_food(self, food):
        self.food.append(food)
    
    def check_future_position(self, future_position):
        """
        Adjusts the given position to ensure it stays within the simulation bounds.

        Args
        -------
        future_position (np.array):
            The anticipated future position of an ant.

        Returns
        -------
        np.array: The adjusted position within the simulation bounds.
        """
        min_x, max_x, min_y, max_y = self.bounds
        x, y = future_position
        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        elif y > max_y:
            y = max_y
        return np.array([x, y])   
