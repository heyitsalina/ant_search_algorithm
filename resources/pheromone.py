import numpy as np
import time

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

            reduce_pheromone(reducing_factor: float, timeframe: float):
                Reduces the pheromone strength in the tensor after a certain timeframe by a specific factor.
        """
        self.pheromones = np.zeros((2, grid_shape[1], grid_shape[0]))
        self.timestamps = np.zeros((2, grid_shape[1], grid_shape[0]))

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
        self.pheromones[depth, pos[1], pos[0]] += pheromone_status
        
        #Check if element is not null / needed for the time deltas in reduce_pheromones
        if self.pheromones[depth, pos[1], pos[0]] != 0:
            self.timestamps[depth, pos[1], pos[0]] += round(time.time(), 2)
    
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
        'coming from colony': self.pheromones[0, pos[1], pos[0]],
        'coming from food': self.pheromones[1, pos[1], pos[0]]
        }
        
        return level_of_pheromones

    def reduce_pheromones(self, reducing_factor = 0.5, k_sec = 5):
        """
        reduces the pheromone level by a reduction factor
        """
        non_zero_indices = np.nonzero(self.pheromones)
        layers, rows, cols = non_zero_indices #richtige reihenfolge der x und y?
        values = self.pheromones[non_zero_indices]

        for layer, row, col, value in zip(layers, rows, cols, values):
            current_time = round(time.time(), 2)
            timestamp_to_compare = self.timestamps[layers, row, col]

            time_delta = current_time - timestamp_to_compare #zb 12
            multiplier = int(time_delta / k_sec) # zb 2, wenn delta 5
            remaining_time_delta = time_delta - (multiplier * k_sec)

            if time_delta >= k_sec:
                 if layer == 0:
                    self.pheromones[layer, rows, cols] += multiplier * reducing_factor #pheromones coming from colony are negative -> addition
                 else:
                     self.pheromones[layer, rows, cols] -= multiplier * reducing_factor #pheromones coming from food are positive -> subtraction

                 if self.pheromones[layer, rows, cols] == 0:
                     self.timestamps[layer, rows, cols] = 0
                 else:
                    self.timestamps[layer, rows, cols] = current_time - remaining_time_delta #set time to current time so that's possible to compare the new lapsed time next time; "add" remaining time (by substracting = greater difference at substraction next time) that could have elapsed but was otherwise not taken into account
    