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
    
    def create_statistic(self):
        data = {
            "colonies": [],
            "food": []
        }

        for colony in self.colonies:
            colony_data = {
                "amount": colony.amount,
                "size": colony.size,
                "coordinates": colony.coordinates,
                "pheromone grid": colony.pheromone.pheromone_array[0].shape,
                "color": colony.color,
                "food counter": colony.food_counter
            }
            data["colonies"].append(colony_data)

        for food in self.food:
            food_data = {
                "start amount": food.start_amount,
                "amount of food": food.amount_of_food,
                "coordinates": food.coordinates
            }
            data["food"].append(food_data)

        with open("statistics/statistics.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        build_pdf()



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

    sim.create_json()