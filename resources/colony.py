from resources.ant import Ant

class Colony:
    def __init__(self, amount, size, coordinates, color):
        """
        This class represents the Ant-colony.

        Args:
        amount (float):
            amount of Ants per colony
        size (float):
            size of the colonys nest?
        coordinates (tuple):
            The (x,y) coordinates of the ants nest?
        """
        self.amount = amount
        self.size = size
        self.coordinates = coordinates
        self.color = color
        self.ants = []
        self.add_ants()
        self.food_counter = 0

    def add_ants(self, amount_to_carry=1, step_size=3):
        for _ in range(self.amount):
            self.ants.append(Ant(coordinates=(self.coordinates[0]+50, self.coordinates[1]+50),
                                 amount_to_carry=amount_to_carry,
                                 step_size=step_size))
    