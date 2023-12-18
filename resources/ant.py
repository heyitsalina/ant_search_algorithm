
class Ant:
    def __init__(self, pheromon_status, start_coordinates, angle, size, speed, amount_to_carry, step_size):
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
        """
        
        self.pheromon_status = pheromon_status
        self.coordinates = [start_coordinates]
        self.size = size
        self.speed = speed
        self.amount_to_carry = amount_to_carry
        self.angle = angle
        self.step_size = step_size
        
    def switch_pheromon(self):
        pass
    
    def move(self, move_to = (0, 0)):
        pass
        
    
    def find_food(self):
        pass
    
    def carry_food(self):
        pass