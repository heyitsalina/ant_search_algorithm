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
    
def test_get_pheromone_level():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)
    pos = (5, 5)
    pheromone_status = 1

    pheromone.leave_pheromone(pos, pheromone_status)
    levels = pheromone.get_pheromone_level(pos)

    assert levels == {'coming from colony': 0, 'coming from food': pheromone_status}

def test_reduce_pheromones():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)
    
    pos = (5, 5)

    # Ant coming from food
    pheromone_status = 1
    pheromone.leave_pheromone(pos, pheromone_status)

    # Ant coming from colony
    pheromone_status = - 1
    pheromone.leave_pheromone(pos, pheromone_status)

    # First reduction
    pheromone.reduce_pheromones(reducing_factor = 0.5)
    levels = pheromone.get_pheromone_level(pos)
    assert levels == {'coming from colony': - 0.5, 'coming from food': 0.5}

    # Second reduction
    pheromone.reduce_pheromones(reducing_factor = 0.5)
    levels = pheromone.get_pheromone_level(pos)
    assert levels == {'coming from colony': - 0.25, 'coming from food': 0.25}

    # Further reductions
    pheromone.reduce_pheromones(reducing_factor = 0.5**5)
    levels = pheromone.get_pheromone_level(pos)
    assert levels == {'coming from colony': 0, 'coming from food': 0}

def test_find_pheromone_target():
    grid_shape = (5, 5)
    pheromone = Pheromone(grid_shape)

    # Negative values array
    pheromone.pheromone_array[0] = -np.arange(1, pheromone.pheromone_array[0].size + 1).reshape(pheromone.pheromone_array.shape[1:])

    # Positive values array
    pheromone.pheromone_array[1] = np.arange(1, pheromone.pheromone_array[1].size + 1).reshape(pheromone.pheromone_array.shape[1:])
    
    # Step_size
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,2), pheromone_status = 1) == (3,3)
    assert pheromone.find_pheromone_target(step_size = 2, ant_array_position = (2,2), pheromone_status = 1) == (4,4)

    # Only one position possible
    assert pheromone.find_pheromone_target(step_size = 3, ant_array_position = (2,1), pheromone_status = 1) == (2, 4)

    # Three positions possible
    assert pheromone.find_pheromone_target(step_size = 4, ant_array_position = (4,4), pheromone_status = 1) == (0, 4)
    
    # Step_size need to be reduced to pick a random position (while-loop)
    # (Step_size out of bounds of the array)
    expected_results = [(0, 0), (4, 0), (0, 4)]
    assert pheromone.find_pheromone_target(step_size = 6, ant_array_position = (4,4), pheromone_status = 1) in expected_results

    expected_results = [(0, 0), (2, 0), (4, 0), (0, 2), (4, 2), (0, 4), (2, 4), (4, 4)]
    assert pheromone.find_pheromone_target(step_size = 3, ant_array_position = (2,2), pheromone_status = 1) in expected_results
    assert pheromone.find_pheromone_target(step_size = 5, ant_array_position = (2,2), pheromone_status = 1) in expected_results

    # Array with negatives
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,2), pheromone_status = -1) == (3, 3)

    # Ant position at edges
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (0,2), pheromone_status = 1) == (1, 3)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,0), pheromone_status = 1) == (3, 1)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (4,2), pheromone_status = 1) == (4, 3)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,4), pheromone_status = 1) == (3, 4)

    # Ant position at corners
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (0,0), pheromone_status = 1) == (1, 1)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (4,0), pheromone_status = 1) == (4, 1)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (4,4), pheromone_status = 1) == (3, 4)
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (0,4), pheromone_status = 1) == (1, 4)

    # Positive values array, same values (10's)
    pheromone.pheromone_array[1] = np.array([[0, 10, 10, 10, 0],
                                        [0, 10, 13, 10, 0],
                                        [0, 10, 10, 10, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0]])
    
    expected_results = [(1, 0), (2, 0), (3, 0), (1, 1), (3, 1), (1, 2), (2, 2), (3, 2)]
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,1), pheromone_status = 1) in expected_results

    # Positive values array, same values (0's)
    pheromone.pheromone_array[1] = np.array([[0, 0, 0, 0, 0],
                                        [0, 0, 13, 0, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0]])
    
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,1), pheromone_status = 1) in expected_results

    # Positive values array, two values have the same pheromone-level
    pheromone.pheromone_array[1] = np.array([[0, 0, 10, 10, 0],
                                        [0, 0, 13, 0, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0]])
    
    expected_results = [(2, 0), (3, 0)]
    assert pheromone.find_pheromone_target(step_size = 1, ant_array_position = (2,1), pheromone_status = 1) in expected_results
