import pytest
import numpy as np
from resources.ant import Ant
from resources.food import Food
from resources.colony import Colony

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
    food = Food(size=10, coordinates=(150, 150), amount_of_food=100)
    ant = Ant(coordinates=(150+45, 150+45), amount_to_carry=20)  # Near the food
    assert ant.try_carry_food(food), "Ant should be able to try to carry food when near it and food is available"


def test_carry_food():
    food = Food(size=10, coordinates=(150, 150), amount_of_food=100)
    ant = Ant(coordinates=(150+45, 150+45), amount_to_carry=20)
    ant.try_carry_food(food)  
    ant.carry_food(food)
    assert ant.pheromone_status == 1, "Ant's pheromone status should be 1 after carrying food"
    assert food.amount_of_food < 100, "Food amount should decrease after ant carries food"
    assert ant.ant_carries > 0, "Ant should be carrying some amount of food"

def test_try_drop_food():
    colony = Colony(grid_pheromone_shape=(100, 100), amount=1, size=10, coordinates=(100, 100), color="red")
    ant = Ant(coordinates=(100+45, 100+45), amount_to_carry=20)  # Ant is near the colony
    ant.pheromone_status = 1  # Assume ant is carrying food
    assert ant.try_drop_food(colony), "Ant should be able to try to drop food when near the colony"


def test_drop_food():
    pass


if __name__ == "__main__":
    test_move()
    test_is_near_target()
    test_switch_pheromone()
    test_try_carry_food()
    test_carry_food()