import pytest
import numpy as np
from resources.pheromone import Pheromone


def test_initialization():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)


    assert pheromone.pheromone_array.shape == (2, grid_shape[1], grid_shape[0])
    assert np.all(pheromone.pheromone_array == 0)

    
def test_leave_pheromone():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)
    pos = (5, 5)
    pheromone_status = 1

    pheromone.leave_pheromone(pos, pheromone_status)
    assert pheromone.pheromone_array[1, pos[1], pos[0]] == pheromone_status
    

def test_reduce_pheromones():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)
    
    pos = (5, 5)
    pheromone_status_food = 1
    pheromone_status_colony = -1

    # Ant coming from food
    pheromone.leave_pheromone(pos, pheromone_status_food)

    # Ant coming from colony
    pheromone.leave_pheromone(pos, pheromone_status_colony)

    # Verify that pheromones are correctly placed
    assert pheromone.pheromone_array[1, pos[1], pos[0]] == pheromone_status_food
    assert pheromone.pheromone_array[0, pos[1], pos[0]] == pheromone_status_colony

    # Reducing by 50%
    reducing_factor = 0.5
    pheromone.reduce_pheromones(reducing_factor)
    
    # Directly checking the array
    assert pheromone.pheromone_array[1, pos[1], pos[0]] == pheromone_status_food * reducing_factor
    assert pheromone.pheromone_array[0, pos[1], pos[0]] == pheromone_status_colony * reducing_factor


    # Reducing by 0.5^6
    reducing_factor = 0.5**6
    pheromone.reduce_pheromones(reducing_factor)
    
    # The final values should be exactly 0 after the reduction
    assert pheromone.pheromone_array[1, pos[1], pos[0]] == 0
    assert pheromone.pheromone_array[0, pos[1], pos[0]] == 0
    