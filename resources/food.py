import random

class Food:
    def __init__(self, size, coordinates, amount_of_food, show_life_bar=True):
        """
        This class represents a food source in the Ant Search Algorithm.

        Args:
        size (float):
            The size of the food source
        coordinates (tuple):
            The (x, y) coordinates of the food source in the search space.
        amount_of_food (float):
            The total amount of food available at the source.
        """
        
        self.coordinates = coordinates
        self.size = size
        self.amount_of_food = amount_of_food
        self.start_amount = amount_of_food
        self.show_life_bar = show_life_bar
        self.epoch = 0
        
    def move_randomly_after_while(self, checkpoint_epoch, bounds):
        
        self.epoch += 1
        if self.epoch % checkpoint_epoch == 0:
        
            min_x, max_x, min_y, max_y = bounds
            
            x_coord = random.uniform((min_x + self.size[0]), (max_x - self.size[0]))
            y_coord = random.uniform((min_y + self.size[1]), (max_y - self.size[1]))
            
            self.coordinates = (x_coord, y_coord)
            
            self.amount_of_food = self.start_amount