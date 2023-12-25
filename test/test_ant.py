import pytest
import numpy as np
from resources.ant import Ant

ant = Ant(pheromone_status=1,
              coordinates=(100.0, 100.0),
              amount_to_carry=20)

def test_switch_pheromon():
    pass

def test_move():
    ant.move()
    assert ant.epoch == 1, "Epoch should increment after move"
    initial_direction = ant.direction.copy()
    ant.move()
    assert not np.array_equal(ant.direction, initial_direction), "Direction should change after move"

def test_find_food():
    ant.coordinates = (145, 145)  # Inside radius
    result = ant.find_food((100, 100))
    assert result is not None, "Should return coordinates when ant is inside radius"
    ant.coordinates = (30, 30)  # Outside radius
    result = ant.find_food((100, 100))
    assert result is None, "Should return None when ant is outside radius"

def test_carry_food():
    pass


if __name__ == "__main__":
    test_move()
    test_find_food()