import pytest
import numpy as np
from resources.ant import Ant

ant = Ant(coordinates=(100.0, 100.0),
          amount_to_carry=20)

def test_switch_pheromone():
    assert ant.pheromone_status == -1, "Initial pheromone status should be -1"
    ant.switch_pheromone()
    assert ant.pheromone_status == 1, "pheromone switch should be 1 after switch"

def test_move():
    ant.move()
    assert ant.epoch == 1, "Epoch should increment after move"
    initial_direction = ant.direction.copy()
    ant.move()
    assert not np.array_equal(ant.direction, initial_direction), "Direction should change after move"
    initial_step_size = np.linalg.norm(ant.direction)
    ant.move()
    new_step_size = np.linalg.norm(ant.direction)
    assert np.isclose(initial_step_size, new_step_size), "Step size should remain constant"
    original_position = ant.coordinates
    ant.coordinates = ant.move()
    assert (ant.coordinates != original_position), "Ant's position should change after move"

def test_is_near_target():
    ant.coordinates = (145, 145)  # Inside radius
    result = ant.is_near_target((100, 100))
    assert result is not None, "Should return coordinates when ant is inside radius"
    ant.coordinates = (30, 30)  # Outside radius
    result = ant.is_near_target((100, 100))
    assert result is None, "Should return None when ant is outside radius"

def test_try_carry_food():

    pass

def test_carry_food():

    pass

def test_try_drop_food():

    pass

def test_drop_food():

    pass


if __name__ == "__main__":
    test_move()
    test_is_near_target()
    test_switch_pheromone()