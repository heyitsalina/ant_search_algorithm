import numpy as np

class Pheromone:
    def __init__(self, grid_shape):
        """
        Manages pheromone information in a tensor within a simulated environment.
        The tensor represents the pheromone strength at different positions within the simulation area.

        Args:
            grid_shape (Tuple[int, int]): A tuple representing the height and width of the simulated environment.

        Attributes:
            pheromones (numpy.ndarray): A 3D numpy array of dimensions (Depth, Height, Width), storing the pheromone strength at each visited position(int).
                                        The depth represents different pheromone matrices ('coming from colony' = -1 | 'coming from food' = 1).

        Methods:
            leave_pheromone():
                Leaves a pheromone from each ant at every movement, adding it to the corresponding location in the tensor.

            get_pheromone_level():
                Determines the pheromone level at a specific location in the tensor.

            reduce_pheromone(reducing_factor: float, zero_threshold: float):
                Reduces the pheromone strength in the tensor after each epoch.
        """

        self.pheromone_array = np.zeros((2, grid_shape[0], grid_shape[1]))


    def leave_pheromone(self, pos, pheromone_status):
        """
        Leaves pheromone at a given position based on the pheromone status. This method is typically
        called when an ant moves, to mark its trail with pheromones.

        Args:
            pos (Tuple[int, int]): The (x, y) coordinates in the grid where the pheromone is to be placed.
            pheromone_status (int): The status of the pheromone to be left, which determines the depth 
                                    in the tensor where the pheromone is placed.

        Returns:
            None. This method modifies the internal state of the pheromone tensor.
        """
        
        depth = 0
        if pheromone_status == 1:
            depth = 1
        
        #Add pheromones status in the corresponding position

        self.pheromone_array[depth, pos[0], pos[1]] += pheromone_status

    
    def get_pheromone_level(self, pos):
        """
        Retrieves the levels of pheromones at a specified grid position. The method returns a dictionary 
        with the levels of two types of pheromones: those coming from the colony and those coming from food.

        Args:
            pos (Tuple[int, int]): The (x, y) coordinates in the grid for which the pheromone levels are to be retrieved.

        Returns:
            dict: A dictionary containing the levels of 'coming from colony' and 'coming from food' pheromones at the specified position.
        """
        
        level_of_pheromones = {
        'coming from colony': self.pheromone_array[0, pos[1], pos[0]],
        'coming from food': self.pheromone_array[1, pos[1], pos[0]]
        }
        
        return level_of_pheromones

    def reduce_pheromones(self, reducing_factor = 0.9999, zero_threshold = 0.0001):
        """
        Reduces the pheromone level by a reduction factor every epoch.
        By the multiplication these will be reduced weighted by their amount, higher amount of pheromones results in higher reduction.

        Args:
            reduction_factor (float): The factor by which the pheromones should be reduced each epoch.
            zero_threshold (float): The value at which the pheromone value is so low that it should be considered 0.

        Returns:
            None. This method modifies the internal state of the pheromone tensor.
        
        """


        self.pheromone_array *= reducing_factor
        self.pheromone_array[0][self.pheromone_array[0] > - zero_threshold] = 0
        self.pheromone_array[1][self.pheromone_array[1] < zero_threshold] = 0