import pytest
import numpy as np
from resources.pheromone import Pheromone


def test_initialization():
    grid_shape = (10, 10)
    pheromone = Pheromone(grid_shape)

    assert pheromone.pheromones.shape == (2, grid_shape[1], grid_shape[0])
    assert np.all(pheromone.pheromones == 0)
    assert np.all(pheromone.timestamps == 0)