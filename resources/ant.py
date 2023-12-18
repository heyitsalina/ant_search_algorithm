import numpy as np

class Ant:
    def __init__(self, pheromon_status, coordinates, angle, size, speed, amount_to_carry, step_size):
        """
        This class represents an ant in the Ant search algorithm.
        
        Args:
        pheromone_status (float): 
            The current level of pheromone detected by the ant.
        coordinates (tuple):
            The (x, y) current coordinates of the ant in the search space.
        angle (float):
            The current angle of the ant in the search space.
        size (float):
            The size of the ant, influencing its interaction with the environment.
        speed (float):
            The speed at which the ant can move within the search space.
        amount_to_carry (float):
            The maximum amount that the ant can carry during its search.
        step_size (float):
            The distance covered by the ant in each step during its movement within the search space.
        ---------
        
        Attributes:
        direction (numpy array):
            The current direction vector of the ant.
        epoch (int):
            Represents the current epoch or step in the movement of the ant.
        """
        
        self.pheromon_status = pheromon_status
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.amount_to_carry = amount_to_carry
        self.angle = angle
        self.step_size = step_size
        self.direction = np.array([0, 0])
        self.epoch = 0

        
    def switch_pheromon(self):
        pass
    
    def move(self):
        position = np.array(self.coordinates)
        
        if self.epoch == 0:
            theta = np.random.uniform(0, 2 * np.pi)
            z = np.random.uniform(-1, 1)
            
            x = np.sqrt(1 - z**2) * np.cos(theta)
            y = np.sqrt(1 - z**2) * np.sin(theta)
            
            self.direction = np.array([x, y])



        
    
    def find_food(self):
        pass
    
    def carry_food(self):
        pass