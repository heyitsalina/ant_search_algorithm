import numpy as np

class Simulation:
    """
    This class represents the simulation in which the ants are moving and the 
    Colony and Food objects are.
    ...

    Attributes
    ----------
    food : list
        A list containing the Food objects.
    colonies : list
        A list containing the colonie objects.
    running : bool
        Indicates if the simulation in running.
    bounds: Tuple
        defines the spatial boundaries of the simulation area (min_x, max_x, min_y, max_y)
    
    Methods
    -------
    start():
        Start the simulation.
    next_epoch():
        Calculates the next position of all Ant objects.
    add_colony():
        Add a Colony object to the simulation.
    add_food():
        Add a Food object to the simulation.
    check_future_position():    
        Adjusts the given position to ensure it stays within the simulation bounds.
    """
    def __init__(self):
        self.food = []
        self.colonies = []
        self.running = False
        self.bounds = () #(min_x, max_x, min_y, max_y)
        
    def next_epoch(self):
        for colony in self.colonies:
            for ant in colony.ants:
                for food in self.food:
                    if ant.try_carry_food(food):
                        ant.carry_food(food)
                        break
                if ant.try_drop_food(colony):
                    ant.drop_food(colony)

                pheromone_direction = self.find_pheromone_trace(ant.coordinates, ant.pheromone_status, colony.pheromone.pheromone_array)
                future_position = ant.move()
                adjusted_position = self.check_future_position(future_position)
                ant.coordinates = adjusted_position
                
                idx_row, idx_col = self.map_ant_coordinates_to_pheromone_index(ant_coordinates = ant.coordinates,
                                                                               colony = colony)
                colony.pheromone.leave_pheromone(pos = (idx_row, idx_col),
                                                 pheromone_status = ant.pheromone_status)
                
        self.food = list(food for food in self.food if food.amount_of_food > 0)
        
    def add_colony(self, colony):
        self.colonies.append(colony)

    def add_food(self, food):
        self.food.append(food)
    
    def check_future_position(self, future_position):
        """
        Adjusts the given position to ensure it stays within the simulation bounds.

        Args
        -------
        future_position (np.array):
            The anticipated future position of an ant.

        Returns
        -------
        np.array: The adjusted position within the simulation bounds.
        """
        min_x, max_x, min_y, max_y = self.bounds
        x, y = future_position
        if x < min_x:
            x = min_x
        elif x >= max_x:
            x = max_x - 1
        if y <= min_y:
            y = min_y + 1
        elif y > max_y:
            y = max_y
        return np.array([x, y])
    

    def map_ant_coordinates_to_pheromone_index(self, ant_coordinates, colony):
        """
        This method takes the coordinates of an ant and maps them to the
        corresponding index in the pheromone grid based on the simulation bounds
        and the shape of the pheromone grid.

        Args
        -------
            ant_coordinates (tuple): The x and y coordinates of the ant's position.
            colony (Colony): The colony object containing the pheromone grid.

        Returns
        -------
            tuple: A tuple containing the row and column indices in the
            pheromone grid that correspond to the ant's position.
        """
        
        width_board = self.bounds[1] - self.bounds[0]
        height_board = self.bounds[3] - self.bounds[2]
        
        n_row = colony.pheromone.pheromone_array.shape[1] #y
        n_col = colony.pheromone.pheromone_array.shape[2] #x
        
        width_spot = width_board / n_col
        height_spot = height_board / n_row
        
        idx_row = -int(ant_coordinates[1] / height_spot)
        idx_col = int(ant_coordinates[0] / width_spot)

        return idx_row, idx_col
    
    def find_pheromone_trace(self, coordinates, pheromone_status, pheromone_grid):
        depth = 0 if pheromone_status == 1 else 1
        pheromone_shape = pheromone_grid[0].shape
        scale = (self.bounds[1]//pheromone_shape[1], -self.bounds[2]//pheromone_shape[0])

        ant_postion = (coordinates[0] * scale[0],  coordinates[1] * scale[1])

        pheromone_cell = self.find_pheromone_target(*ant_postion, pheromone_status*pheromone_grid[depth])
        pheromone_position = self.calculate_pheromone_target_pos(pheromone_cell, pheromone_grid)
        pheromone_direction = np.array(pheromone_position) - coordinates

        return pheromone_direction

    def find_pheromone_target(self, row, col, arr):
        slice_ = arr[max(0, row - 1):min(row + 2, arr.shape[0]),
                 max(0, col - 1):min(col + 2, arr.shape[1])]
        max_pos = np.unravel_index(np.argmax(slice_), slice_.shape)
        max_pos_in_original_array = (max(0, row - 1) + max_pos[0], max(0, col - 1) + max_pos[1])
        
        return max_pos_in_original_array

    def calculate_pheromone_target_pos(self, idx_target_pheromone_value, pheromone_grid):
        
        n_row = pheromone_grid[1] #y
        n_col = pheromone_grid[2] #x        
        
        width_board = self.bounds[1] - self.bounds[0]
        height_board = self.bounds[3] - self.bounds[2]
        
        width_spot = width_board/ n_col
        height_spot = height_board/ n_row
        
        x_target_pos = idx_target_pheromone_value[1] * width_spot + width_spot/2 
        y_target_pos = idx_target_pheromone_value[0] * height_spot + height_spot/2
        
        return x_target_pos, -y_target_pos