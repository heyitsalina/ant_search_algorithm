from resources.ant import Ant
from resources.pheromone import Pheromone
from resources.timer_decorator import time_this


class Colony:
    def __init__(self, grid_pheromone_shape, amount, size, coordinates, color, show_pheromone=False):
        """
        This class represents the Ant-colony.
        --------

        Args:
        grid_pheromone_shape (tuple):
            number of rows and columns of pheromone array
        amount (float):
            amount of Ants per colony
        size (float):
            size of the colonys nest
        coordinates (tuple):
            The (x,y) coordinates of the ants nest
        colors (str):
            The color representation of the colony.
        show_pheromone (bool, optional):
            Whether to display pheromone trails. Defaults to False.
        ----------

        Attributes:
        pheromone (Pheromone):
            The pheromone object and its grid shape associated with the colony.
        ants (list):
            List of ants belonging to the colony.
        food_counter (int):
            Counter to track the amount of food collected by the colony.
        -----------

        Methods:
        def add_ants():
            Add ants to the colony.
        """

        self.pheromone = Pheromone(grid_shape=grid_pheromone_shape)
        self.amount = amount
        self.size = size
        self.coordinates = coordinates
        self.color = color
        self.show_pheromone = show_pheromone
        self.ants = []
        self.add_ants()
        self.food_counter = 0

        
    @time_this
    def add_ants(self, amount_to_carry=1, step_size=3, search_radius=1, pheromone_influence=0.01):
        """
        Add ants to the colony.
        --------

        Args:
        amount_to_carry (float):
            The maximum amount that each ant can carry. Defaults to 1.
        step_size (float):
            The distance covered by ants in each step during movement. Defaults to 3.
        ---------

        Returns:
            None.
        """

        for _ in range(self.amount):
            self.ants.append(Ant(coordinates=(self.coordinates[0]+50, self.coordinates[1]+50),
                                 amount_to_carry=amount_to_carry,
                                 step_size=step_size, 
                                 search_radius=search_radius,
                                 pheromone_influence=pheromone_influence))
