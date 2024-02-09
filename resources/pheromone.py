import numpy as np
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

    def reduce_pheromones(self, reducing_factor = 0.5, zero_threshold = 0.01):
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
        
        
    def find_target_pheromone_idx(self, idx_ant_pos, pheromone_status, search_radius = 3):
        """
        Identifies the index of the neighboring cell with the optimal pheromone value based on the ant's status.

        Args:
            idx_ant_pos (tuple): The current grid position of the ant (row, column).
            pheromone_status (int): The status of the ant (-1 for seeking food, 1 for returning to colony).

        Returns:
            tuple: The grid index of the target cell with the highest (when seeking food) or lowest (when returning) pheromone value.
        """
        
        # Initialize target pheromone values for comparison
        target_pheromone_value = None
        idx_target_pheromone_value = None

        # Determine the grid size
        n_rows, n_cols = self.pheromone_array.shape[1:]

        # Determine the pheromone layer to inspect
        depth = 0 if pheromone_status == 1 else 1

        # Store indices of potential targets
        potential_targets = []

        # Define range limits for row and column
        row_start = max(0, idx_ant_pos[0] - search_radius)
        row_end = min(idx_ant_pos[0] + (search_radius + 1), n_rows)
        col_start = max(0, idx_ant_pos[1] - search_radius)
        col_end = min(idx_ant_pos[1] + (search_radius + 1), n_cols)

        # Iterate over cells around the ant
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                if (i, j) != idx_ant_pos:  # Ignore the ant's current cell
                    current_value = self.pheromone_array[depth, i, j]

                    # Update target for highest pheromone value when seeking food
                    if pheromone_status == -1 and (target_pheromone_value is None or current_value > target_pheromone_value):
                        target_pheromone_value = current_value
                        idx_target_pheromone_value = (i, j)
                        potential_targets = [(i, j)]  # Reset potential targets since a new max has been found

                    # Update target for lowest pheromone value when returning to colony
                    elif pheromone_status == 1 and (target_pheromone_value is None or current_value < target_pheromone_value):
                        target_pheromone_value = current_value
                        idx_target_pheromone_value = (i, j)
                        potential_targets = [(i, j)]  # Reset potential targets since a new min has been found

                    # Add index to potential targets if value is equal to the current target
                    elif current_value == target_pheromone_value:
                        potential_targets.append((i, j))

        # Choose randomly from potential targets if there are multiple
        if len(potential_targets) > 1:
            idx_target_pheromone_value = random.choice(potential_targets)
            
        return idx_target_pheromone_value
    
    
    def get_target_pheromone_pos(self, idx_ant_pos, pheromone_status, bounds):
        """
        Converts the target pheromone grid index to its corresponding (center) position in the environment.

        Args:
            idx_ant_pos (tuple): The grid position of the ant (row, column).
            pheromone_status (int): The pheromone status indicating if the ant is seeking food (-1) or returning (1).
            bounds (tuple): The min and max bounds of the environment (min_x, max_x, min_y, max_y).

        Returns:
            tuple: The (x, y) position in the environment corresponding to the target pheromone index.
        """
        
        # Find the grid index for the target pheromone
        idx_target_pheromone_value = self.find_target_pheromone_idx(idx_ant_pos, pheromone_status)
        
        # Get the dimensions of the pheromone grid
        n_row, n_col = self.pheromone_array.shape[1:] # Rows (y-axis), Columns (x-axis)
        
        width_board = bounds[1] - bounds[0]
        height_board = bounds[3] - bounds[2]
        
        width_spot = width_board / n_col
        height_spot = height_board / n_row
        
        # Compute the central position of the target grid cell
        x_target_pos = idx_target_pheromone_value[1] * width_spot + width_spot / 2
        y_target_pos = idx_target_pheromone_value[0] * height_spot + height_spot / 2
        
        # Return the position with the y-coordinate inverted to match the environment's coordinate system
        return x_target_pos, -y_target_pos