import pytest
import numpy as np
import os
import json
from resources.simulation import Simulation
from resources.colony import Colony
from resources.food import Food



def test_next_epoch():
    sim = Simulation()

    for _ in range(5):
        sim.next_epoch()

    assert sim.epoch == 5


def test_simulation_initialisation():
    sim = Simulation()

    assert sim.food == []
    assert sim.colonies == []
    assert sim.running is False
    assert sim.bounds == ()


def test_add_colony_and_food():
    sim = Simulation()
    sim.bounds = (0, 720, -480, 0)
    food = Food(size=(10,10), coordinates=(100,100), amount_of_food=100)
    colony = Colony(grid_pheromone_shape=(100, 100), amount=10, size=(10,10), coordinates=(100.0, 100.0), color=(1, 1, 1, 1))
    sim.add_colony(colony)
    sim.add_food(food)
    

    assert colony in sim.colonies
    assert food in sim.food
    


    


def test_check_future_position():
    sim = Simulation()

    sim.bounds = (50, 200, 50, 200)
    future_position = [40, 20]
    expected_adjusted_position = [50, 51]

    adjusted_position = sim.check_future_position(future_position)
    
    assert np.array_equal(adjusted_position, expected_adjusted_position)


def test_map_ant_coordinates_to_pheromone_index():
    sim = Simulation()

    sim.bounds = (50, 200, 50, 200)
    ant_coordinates = [125, 125]

    # Random data for our colony
    grid_pheromone_shape = (10, 10)
    amount = 100
    size = (100, 100)
    coordinates = (100, 100)
    color = (255, 255, 255, 255)
    colony = Colony(grid_pheromone_shape, amount, size, coordinates, color)

    idx_row, idx_col = sim.map_ant_coordinates_to_pheromone_index(ant_coordinates, colony)
    expected_idx_row = -8
    expected_idx_col = 8

    assert idx_row == expected_idx_row
    assert idx_col == expected_idx_col


def test_find_pheromone_trace():
    sim = Simulation()

    sim.bounds = (50, 200, 50, 200)
    pheromone_array = np.zeros((2, 10, 10))

    # Data for our colony
    grid_pheromone_shape = (10, 10)
    amount = 100
    size = (100, 100)
    color = (255, 255, 255, 255)
    coordinates = (100, 100)
    colony = Colony(grid_pheromone_shape, amount, size, coordinates, color)
    colony.pheromone.pheromone_array = pheromone_array
    pheromone_status = 1
    search_radius = 3

    # Coordinates not within search radius
    pheromone_direction_none = sim.find_pheromone_trace((40, 40), pheromone_status, pheromone_array, colony, search_radius)
    assert pheromone_direction_none is None, "Should return None if no pheromone trace was found within the search radius."


def test_get_pheromone_position():
    sim = Simulation()

    row = 3
    col = 3
    search_radius = 3
    
    # Test case where the maximum position is None
    arr = np.zeros((2, 2))
    max_pos_in_original_array = sim.get_pheromone_position(row, col, arr, search_radius)
    assert max_pos_in_original_array is None
    
    # Test case where the maximum position is not None
    arr = np.array([[0, 1], [2, 3]])
    max_pos_in_original_array = sim.get_pheromone_position(row, col, arr, search_radius)
    assert max_pos_in_original_array is not None


def test_create_statistic():
    sim = Simulation()

    # Set up sample data for the simulation
    sim.epoch = 10
    sim.bounds = (50, 200, 50, 200)
    sim.colony_data = [{
        "amount": 50,
        "size": (10, 10),
        "coordinates": (30, 40),
        "pheromone grid":[[0, 0], [0, 0]],
        "color": (255, 255, 255, 255),
        "food_counter": 20,
        "ants": [{
            "step_size": 2,
            "amount_to_carry": 5,
            "search_radius": 10,
            "pheromone_influence": 0.5
        }]
    }]

    sim.food_data = [{
        "start_amount": 100,
        "amount_of_food": 80,
        "coordinates": (60, 70)  
    }]

    # Call the create_statistic method
    sim.create_statistic()
    
    # Adjust current path (remove tail) 
    current_path = os.getcwd()

    resetted_path = os.path.split(current_path)

    os.chdir(resetted_path[0])


    # Check if the statistics.json file is created
    assert os.path.exists("statistics.json")

    # Check if the statistics.json file contains the expected data
    with open("statistics.json", "r") as json_file:
        data = json.load(json_file)

    assert data["simulation"][0]["epochs"] == 10
    assert data["simulation"][0]["boundaries"] == [50, 200, 50, 200]
    assert len(data["colonies"]) == 0
    assert len(data["food"]) == 0



if __name__ == "__main__":
    test_next_epoch()
    test_simulation_initialisation()
    test_add_colony_and_food()
    test_check_future_position()
    test_map_ant_coordinates_to_pheromone_index()
    test_find_pheromone_trace()
    test_get_pheromone_position()
    test_create_statistic()
