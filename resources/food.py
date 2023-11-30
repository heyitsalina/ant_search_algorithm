
class food:
    def __init__(self, size, coordinates, amount_of_food):
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
    

