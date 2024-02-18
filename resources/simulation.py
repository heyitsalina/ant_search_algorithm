import json
import numpy as np
from resources.colony import Colony
from resources.food import Food
from statistics.statistics import build_pdf

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
        self.obstacles = []
        self.running = False
        self.bounds = () #(min_x, max_x, min_y, max_y)
        self.epoch = 0
        
    def next_epoch(self):
        self.epoch += 1
        active_food_objects = [food for food in self.food if food.amount_of_food != 0]

        for colony in self.colonies:
            for ant in colony.ants:
                for food in active_food_objects:
                    if ant.try_carry_food(food):
                        ant.carry_food(food)
                        break
                if ant.try_drop_food(colony):
                    ant.drop_food(colony)

                pheromone_direction = self.find_pheromone_trace(ant.coordinates, ant.pheromone_status, colony.pheromone.pheromone_array, colony, ant.search_radius)
                future_position = ant.move(pheromone_direction=pheromone_direction)
                future_position = self.check_for_obstacles(future_position)
                adjusted_position = self.check_future_position(future_position)
                ant.coordinates = adjusted_position
                
                idx_row, idx_col = self.map_ant_coordinates_to_pheromone_index(ant_coordinates = ant.coordinates,
                                                                               colony = colony)
                
                colony.pheromone.leave_pheromone(pos = (idx_row, idx_col),
                                                 pheromone_status = ant.pheromone_status)    
            colony.pheromone.reduce_pheromones(0.99, 0.001)
        
        for food in active_food_objects:
            food.move_randomly_after_while(self.bounds)
            
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
    
    def check_for_obstacles(self, future_position):
        x, y = future_position
        
        for obstacle in self.obstacles:
            min_x, max_x, min_y, max_y = obstacle.pos[0]-5, obstacle.pos[0] + obstacle.size[0], obstacle.pos[1]-5, obstacle.pos[1] + obstacle.size[1]
            if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                x_diff = min(abs(x - min_x), abs(x - max_x))
                y_diff = min(abs(y - min_y), abs(y - max_y))

                if x_diff < y_diff:
                    if x_diff == abs(x - min_x):
                        x = min_x - 5
                        if x < min_x:
                            x = min_x
                    else:
                        x = max_x + 1
                        if x > max_x:
                            x = max_x
                else:
                    if y_diff == abs(y - min_y):
                        y = min_y - 5
                        if y < min_y:
                            y = min_y
                    else:
                        y = max_y + 1
                        if y > max_y:
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
    
    def create_statistic(self):
        data = {
            "simulation" : [],
            "colonies": [],
            "food": [],
            "obstacles": []
        }

        simulation_data = {
            "epochs": self.epoch,
            "boundaries": self.bounds
        }
        data["simulation"].append(simulation_data)

        for colony in self.colonies:
            colony_data = {
                "amount": colony.amount,
                "size": colony.size,
                "coordinates": [round(num, 3) for num in colony.coordinates],
                "pheromone grid": colony.pheromone.pheromone_array[0].shape,
                "color": colony.color,
                "food counter": colony.food_counter,
                "step size": colony.ants[0].step_size,
                "amount to carry": colony.ants[0].amount_to_carry,
                "search radius": colony.ants[0].search_radius,
                "pheromone influence": colony.ants[0].pheromone_influence,
            }
            data["colonies"].append(colony_data)

        for food in self.food:
            food_data = {
                "start amount": food.start_amount,
                "amount of food": food.amount_of_food,
                "coordinates": [round(num, 3) for num in food.coordinates],
            }
            data["food"].append(food_data)

        for obstacle in self.obstacles:
            obstacle_data = {
                "pos": obstacle.pos,
                "size": obstacle.size
            }
            data["obstacles"].append(obstacle_data)

        with open("statistics/statistics.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        build_pdf()

    def find_pheromone_trace(self, coordinates, pheromone_status, pheromone_array, colony, search_radius):
        depth = 0 if pheromone_status == 1 else 1
        pheromone_shape = pheromone_array[0].shape
        scale = (self.bounds[1]//pheromone_shape[1], -self.bounds[2]//pheromone_shape[0])

        ant_postion = self.map_ant_coordinates_to_pheromone_index(coordinates, colony)
        pheromone_cell = self.get_pheromone_position(*ant_postion, -pheromone_status*pheromone_array[depth], search_radius)

        if pheromone_cell is None or pheromone_cell == ant_postion:
            return

        pheromone_position = (pheromone_cell[1]*scale[0]+pheromone_shape[0]/2, -pheromone_cell[0]*scale[1]-pheromone_shape[1]/2 )
        pheromone_direction = np.array(pheromone_position) - coordinates

        return pheromone_direction

    def get_pheromone_position(self, row, col, arr, search_radius):
        start_row = max(0, row - search_radius)
        end_row = min(arr.shape[0], row + search_radius + 1)
        start_col = max(0, col - search_radius)
        end_col = min(arr.shape[1], col + search_radius + 1)
        slice_ = arr[start_row:end_row, start_col:end_col]

        if np.argmax(slice_) == 0:
            return
        
        max_pos = np.unravel_index(np.argmax(slice_), slice_.shape)
        max_pos_in_original_array = (start_row + max_pos[0], start_col + max_pos[1])
        return max_pos_in_original_array



if  __name__ == "__main__":
    sim = Simulation()

    sim.bounds = (
            0,
            720,
            -480,
            0 
        )
    
    n_row, n_col = int(sim.bounds[3]-sim.bounds[2])//40, int(sim.bounds[1]-sim.bounds[0])//40
    coordinates = (360, -240)
    amount = 100

    sim.add_colony(Colony(grid_pheromone_shape=(n_row, n_col), amount=amount, size=(100, 100),
                                  coordinates=coordinates, color=(0, 0, 0, 1)))
    
    sim.add_colony(Colony(grid_pheromone_shape=(n_row-2, n_col+2), amount=amount+400, size=(100, 100),
                                  coordinates=coordinates, color=(0, 0, 1, 1)))

    coordinates = (150, -300)
    amount_of_food = 100

    sim.add_food(Food(size=(100, 100), coordinates=coordinates, amount_of_food=amount_of_food))

    sim.add_food(Food(size=(100, 100), coordinates=coordinates, amount_of_food=amount_of_food+250))

    for  i in range(100):
        sim.next_epoch()
    
    for colony in sim.colonies:
        print(colony.food_counter)

    for food in sim.food:
        print(food.amount_of_food)
