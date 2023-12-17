import random 

class Ant:
    def __init__(self, pheromon_status, coordinates, size, speed, amount_to_carry):
        """
        This class represents an ant in the Ant search algorithm.
        
        Args:
        pheromone_status (float): 
            The current level of pheromone detected by the ant.
        coordinates (tuple):
            The (x, y) coordinates of the ant in the search space.
        size (float):
            The size of the ant, influencing its interaction with the environment.
        speed (float):
            The speed at which the ant can move within the search space.
        amount_to_carry (float):
            The maximum amount that the ant can carry during its search.  
        """
        
        self.pheromon_status = pheromon_status
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.amount_to_carry = amount_to_carry 
        
    def switch_pheromon(self):
        pass
    
    def move(self):
        # for test purposes only:
        self.coordinates = (self.coordinates[0]+random.randrange(-2, 3), self.coordinates[1]+random.randrange(-2, 3))
    
    def find_food(self):
        pass
    
    def carry_food(self):
        pass