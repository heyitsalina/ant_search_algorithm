import numpy as np
from resources.timer_decorator import time_this

class Ant:
    def __init__(self, coordinates, amount_to_carry, step_size=1, search_radius=1, pheromone_influence=0.01):
        """
        This class represents an ant in the Ant search algorithm.
        
        Args:
        coordinates (tuple):
            The (x, y) current coordinates of the ant in the search space.
        amount_to_carry (float):
            The maximum amount that the ant can carry during its search.
        step_size (float):
            The distance covered by the ant in each step during its movement within the search space.
        ---------
        
        Attributes:
        pheromone_status (int): 
            The current status of pheromone by the ant.
                - -1 indicates the ant is searching for food and not carrying any.
                -  1 indicates the ant has found food and is carrying it back to the nest.
        direction (numpy array):
            The current direction vector of the ant.
        epoch (int):
            Represents the current epoch or step in the movement of the ant.
        ---------

        Methods:
        first_direction():
            Generates a random direction on the 2D plane using spherical coordinates.
        move():
            Moves the agent based on its current direction and optional pheromone influence.
        switch_pheromone():
            Switches the pheromone status of the ant.
        move(): 
            Moves the ant in the search space.
        is_near_target():
            Determines if an ant is within a specified radius of a food or colony source.
        try_carry_food ():
            Determine if the ant can pick up food from a specified source.
        carry_food()
            Have the ant pick up food from the specified source and update its status.
        try_drop_food():
            Determine if the ant can drop food at its colony.
        drop_food():
            Have the ant drop food at its colony and update its status.
        """
        
        self.pheromone_status = -1
        self.coordinates = coordinates
        self.amount_to_carry = amount_to_carry
        self.step_size = step_size
        self.direction = self.first_direction()
        self.epoch = 0
        self.ant_carries = 0
        self.search_radius = search_radius
        self.pheromone_influence = pheromone_influence

    def first_direction(self):
        """
        Generates a random direction on the 2D plane using spherical coordinates.
        ----------

        Returns:
        numpy array: A 2D vector representing the random direction scaled by the step size.
        """
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.arccos(2 * np.random.uniform(0, 1) - 1)

        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)

        return np.array([x, y]) * self.step_size

    def switch_pheromone(self):
        """
        Switches the pheromone status of the ant.
        """
        self.pheromone_status *= -1
        
    @time_this 
    def move(self, pheromone_direction=None):
        """
        Moves the ant based on its current direction and optional pheromone influence.
        ---------

        Args:
            pheromone_direction (numpy array, optional): An additional directional influence based on pheromones.
        ---------
    
        Returns:
            tuple: The future position of the ant after moving.
        """
        position = np.array(self.coordinates)
        
        angle_offset = np.random.uniform(-np.pi / 4, np.pi / 4)
        
        cos_offset = np.cos(angle_offset)
        sin_offset = np.sin(angle_offset)

        new_x = cos_offset * self.direction[0] - sin_offset * self.direction[1]
        new_y = sin_offset * self.direction[0] + cos_offset * self.direction[1]
        
        self.direction = np.array([new_x, new_y])

        if pheromone_direction is not None:
            self.direction += pheromone_direction * self.pheromone_influence

        magnitude = np.sqrt(new_x ** 2 + new_y ** 2)
        self.direction *= self.step_size / magnitude

        self.epoch += 1

        future_position = position + self.direction
        return tuple(future_position)
         
    @time_this
    def is_near_target(self, target_position, center_offset=45, radius=20):
        """
        Determines if an ant is within a specified radius of a food or colony source.
        ----------

        Parameters:
        target_position (tuple):
            The (x, y) coordinates of the food or colony source.
        center_offset (int):
            The offset value to adjust the center of the target. Defaults to 45 => offset of source of food.
        radius (int):
            The radius of the circular area around the target. Defaults to 20 => radius of source of food.
        ----------

        Returns:
            tuple: The current (x, y) coordinates of the ant if it is within the specified radius; 
                   otherwise, returns None.
        """
        target_center_x, target_center_y = target_position[0] + center_offset, target_position[1] + center_offset

        ant_x, ant_y = self.coordinates
        distance_squared = (target_center_x - ant_x) ** 2 + (target_center_y - ant_y) ** 2

        if distance_squared <= radius ** 2:
            return (ant_x, ant_y)
        return None
    
    def try_carry_food(self, food):
        """
        Determine if the ant can pick up food from a specified source.
        ----------

        Args:
            food (Food): The food source to potentially pick up food from.
        ----------

        Returns:
            bool: True if the ant can carry food, False otherwise.
        """
        return self.pheromone_status == -1 and  self.is_near_target(food.coordinates) and food.amount_of_food > 0
   
    @time_this
    def carry_food(self, food):
        """
        Have the ant pick up food from the specified source and update its status.
        -----------

        Args:
            food (Food): The food source to pick up food from.
        """
        amount_taken = min(food.amount_of_food, self.amount_to_carry)
        food.amount_of_food -= amount_taken
        self.ant_carries = amount_taken 
        self.switch_pheromone()

    def try_drop_food(self, colony):
        """
        Determine if the ant can drop food at its colony.
        ---------

        Args:
            colony (Colony): The colony to potentially drop food at.
        ---------

        Returns:
            bool: True if the ant can drop food, False otherwise.
        """
        return self.pheromone_status == 1 and self.is_near_target(colony.coordinates)
    
    @time_this
    def drop_food(self, colony):
        """
        Have the ant drop food at its colony and update its status.
        ----------

        Args:
            colony (Colony): The colony to drop food at.
        """
        colony.food_counter += self.ant_carries
        self.ant_carries = 0 
        self.switch_pheromone()
        
