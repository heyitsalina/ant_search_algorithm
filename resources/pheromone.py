import numpy as np
import time
import random

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

    def reduce_pheromone(self, reducing_factor, k_sec):
        """
        reduces the pheromone level by a reduction factor
        """
        pass

    def find_pheromone_target(self, step_size, ant_array_position, pheromone_status):
        """
        Searches for the strongest or weakest (depending on the goal=pheromone-status) pheromone-value in the pheromone array 
        in a range of a given step size.
        After the value is found, the ant-movement will be directed in this direction.

        Args:
            step_size (int): Steps the ant does in one epoch. Affects which pheromones (array-elements) will be considered.
            ant_array_position (Tuple[float, float]): The (x, y) coordinates in the grid for the current ant-position.
                                                      Are mapped by the mapping-method.
            pheromone_status (int): The pheromone that the ant is currently placing and therefore looking for.

        Returns:
            float: An angle for the ant.move-method to do the movement in the direction of the calculated angle.
        """

        # To fit the coordinates correctly from x, y to y, x
        ant_array_position = (ant_array_position[1], ant_array_position[0])

        depth = 0
        
        if pheromone_status == 1:
            depth = 1
        else:
            # Convert pheromone-levels to positive to represent all cases (at pheromone-level -1 means depth = 0)
            self.pheromones[0] = -self.pheromones[0]
            
        
        def check_and_store_values(array, center, step_size):
            '''
            Checks all pheromone-levels within the step size and stores their values with the the corresponding positions
            '''

            found_values = []
            original_indices = []

            # Go through all surrounding index positions depending on the step size
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Ignore the current position of the ant
                    if i == 0 and j == 0:
                        continue

                    row = center[0] + i * step_size
                    col = center[1] + j * step_size

                    # Invalid indices are ignored
                    if 0 <= row < array.shape[0] and 0 <= col < array.shape[1]:
                        element = array[row, col]
                        found_values.append(element)
                        original_indices.append((row, col))

            return found_values, original_indices

        # Collect values and indices
        found_values, original_indices = check_and_store_values(self.pheromones[depth], ant_array_position, step_size)


        # Check if any pheromone-levels are found
        if found_values:
            
            # Check if all pheromone-levels are equal or not
            if np.all(found_values == np.max(found_values)):
                #If all pheromones in reach have the same level (f.e. all have 5 or all have 0) a random index will be picked
                original_index_max_value = random.choice(original_indices)
                
            else:
                # Find index of highest value
                # There could be more than one value of highest pheromones but all values must not be the same
                # Therefor pick a random one from them
                max_indices = np.where(found_values == np.max(found_values))[0]
                index_max_value = random.choice(max_indices)
                
                original_index_max_value = original_indices[index_max_value]

        else:
            # If there is no pheromone in step_size-reach, perform an random step by reducing the step_size until possible indices to move are found, 
            # then pick a random one of them
            
            # Loop is performed until original_indices isn't empty anymore
            while not check_and_store_values(self.pheromones[depth], ant_array_position, step_size)[1]:
                step_size = max(step_size - 1, 1)
            
            # Get the new positions within the new possible step size
            found_values, original_indices = check_and_store_values(self.pheromones[depth], ant_array_position, step_size)
            original_index_max_value = random.choice(original_indices)

        # Convert back from (y, x) to (x, y)
        original_index_max_value = (original_index_max_value[1], original_index_max_value[0])

        #Convert pheromone-level back to normal
        if pheromone_status == -1:
            self.pheromones[0] = -self.pheromones[0]

        return original_index_max_value
    