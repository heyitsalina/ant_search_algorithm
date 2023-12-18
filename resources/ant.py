# import random 
import numpy as np

class Ant:
    def __init__(self, pheromone_status, coordinates, amount_to_carry, step_size=1):
        """
        This class represents an ant in the Ant search algorithm.
        
        Args:
        pheromone_status (float): 
            The current level of pheromone detected by the ant.
        coordinates (tuple):
            The (x, y) current coordinates of the ant in the search space.
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
        
        self.pheromon_status = pheromone_status
        self.coordinates = coordinates
        self.amount_to_carry = amount_to_carry
        self.step_size = step_size
        self.direction = np.array([0, 0])
        self.epoch = 0

        
    def switch_pheromon(self):
        pass
    
    def move(self):
        # for test purposes only:
        # self.coordinates = (self.coordinates[0]+random.randrange(-2, 3), self.coordinates[1]+random.randrange(-2, 3))
        pass
    
        position = np.array(self.coordinates)
        
        if self.epoch == 0:
            #Randomly set initial direction in coordinates
            theta = np.random.uniform(0, 2 * np.pi)
            z = np.random.uniform(-1, 1)
            
            x = np.sqrt(1 - z**2) * np.cos(theta)
            y = np.sqrt(1 - z**2) * np.sin(theta)
            
            #Set direction vector        
            self.direction = np.array([x, y]) * self.step_size

            #Update position using the direction vector
            position += self.direction
            self.coordinates = tuple(position)

            self.epoch += 1
        else:
            #Apply a random rotation to the existing direction
            angle_offset = np.random.uniform(-np.pi/4, np.pi/4)
            rotation_matrix = np.array([[np.cos(angle_offset), -np.sin(angle_offset)],
                                    [np.sin(angle_offset), np.cos(angle_offset)]])
            
            #Rotate and normalize the direction vector
            self.direction = np.dot(rotation_matrix, self.direction)
            self.direction = self.direction / np.linalg.norm(self.direction) * self.step_size
            
            #Update position using the rotated direction
            position += self.direction
            self.coordinates = tuple(position)

            self.epoch += 1
        
    def find_food(self):
        pass
    
    def carry_food(self):
        pass
