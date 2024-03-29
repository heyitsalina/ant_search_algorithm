import random


class Food:
    def __init__(self, size, coordinates, amount_of_food, move_after_number_of_epochs = 500, show_life_bar=True, move_randomly = False):
        """
        This class represents a food source in the Ant Search Algorithm.
        ---------

        Args:
        size (float):
            The size of the food source
        coordinates (tuple):
            The (x, y) coordinates of the food source in the search space.
        amount_of_food (float):
            The total amount of food available at the source.
        move_after_number_of_epochs (int):
            The number of epochs after which the food source may move.
        show_life_bar (bool):
            Flag to indicate whether to display the life bar of the food source.
        move_randomly (bool):
            Flag to indicate whether the food source moves randomly.
        ----------

        Methods:
        move_randomly_after_while():
            Moves the food source randomly within the given bounds at specified epochs.
            
        """
        self.coordinates = coordinates
        self.size = size
        self.amount_of_food = amount_of_food
        self.start_amount = amount_of_food
        self.show_life_bar = show_life_bar
        self.move_randomly = move_randomly 
        self.move_after_number_of_epochs = move_after_number_of_epochs
        self.epoch = 0
    
    def move_randomly_after_while(self, bounds):
        """
        Moves the food source randomly within the given bounds at specified epochs.
        Resets the food amount to its initial value upon movement.
        ---------

        Args:
        checkpoint_epoch (int):
            Epoch target for moving the food source.
        bounds (tuple):
            ant world bounds for the movement (min_x, max_x, min_y, max_y).
        --------

        Returns:
        None: Modifies the food source's coordinates and amount directly.
        """
        if self.move_randomly is False:
            return
        
        self.epoch += 1
        if self.epoch % self.move_after_number_of_epochs == 0:
        
            min_x, max_x, min_y, max_y = bounds
            
            x_coord = random.uniform((min_x + self.size[0]), (max_x - self.size[0]))
            y_coord = random.uniform((min_y + self.size[1]), (max_y - self.size[1]))
            
            self.coordinates = (x_coord, y_coord)
            
            self.amount_of_food = self.start_amount
