import pytest
import numpy as np
from resources.pheromone import Pheromone


def test_initialization():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)

    assert pheromone.pheromones.shape == (2, grid_shape[1], grid_shape[0])
    assert np.all(pheromone.pheromones == 0)
    
def test_leave_pheromone():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)
    pos = (5, 5)
    pheromone_status = 1

    pheromone.leave_pheromone(pos, pheromone_status)
    assert pheromone.pheromones[1, pos[1], pos[0]] == pheromone_status
    
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
    for _ in range(5):
        pheromone.reduce_pheromones(reducing_factor = 0.5)
    levels = pheromone.get_pheromone_level(pos)
    assert levels == {'coming from colony': 0, 'coming from food': 0}

    