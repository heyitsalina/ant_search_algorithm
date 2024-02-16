from resources.ant import Ant
from resources.pheromone import Pheromone


class Colony:
    def __init__(self, grid_pheromone_shape, amount, size, coordinates, color, show_pheromone=False):
        """
        This class represents the Ant-colony.

        Args:
        grid_pheromone_shape(tuple):
            number of rows and columns of pheromone array
        amount (float):
            amount of Ants per colony
        size (float):
            size of the colonys nest
        coordinates (tuple):
            The (x,y) coordinates of the ants nest
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

    def add_ants(self, amount_to_carry=1, step_size=3, search_radius=3, pheromone_influence=0.01):
        for _ in range(self.amount):
            self.ants.append(Ant(coordinates=(self.coordinates[0]+50, self.coordinates[1]+50),
                                 amount_to_carry=amount_to_carry,
                                 step_size=step_size, search_radius=search_radius,
                                 pheromone_influence=pheromone_influence))
    