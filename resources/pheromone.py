import numpy as np

class pheromone:
    def __init__(self, grid_shape):
        """
        Manages pheromone information in a tensor within a simulated environment.
        The tensor represents the pheromone strength at different positions within the simulation area.

        Args:
            grid_shape (Tuple[int, int]): A tuple representing the height and width of the simulated environment.

        Attributes:
            pheromones (numpy.ndarray): A 3D numpy array of dimensions (Height, Width, Depth), storing the pheromone strength at each visited position(int).
                                        The depth represents different pheromone matrices ('coming from colony' = -1 | 'coming from food' = 1).

        Methods:
            leave_pheromone():
                Leaves a pheromone from each ant at every movement, adding it to the corresponding location in the tensor.

            get_pheromone_level():
                Determines the pheromone level at a specific location in the tensor.

            reduce_pheromone(reducing_factor: float, timeframe: float):
                Reduces the pheromone strength in the tensor after a certain timeframe by a specific factor.
        """
        self.pheromones = np.zeros((grid_shape[0], grid_shape[1], 2))

    def leave_pheromone(self, pos, pheromone_status):
        pass
    
    def get_pheromone_level(self, pos):
        pass

    def reduce_pheromone(self, reducing_factor, timeframe):
        pass