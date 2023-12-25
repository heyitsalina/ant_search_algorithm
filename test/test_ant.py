import pytest
from resources.ant import Ant

ant = Ant(pheromone_status=1,
              coordinates=(100.0, 100.0),
              amount_to_carry=20)

def test_switch_pheromon():
    pass

def test_move():
    pass

def test_find_food():
    ant.coordinates = (145, 145)  # Inside radius
    result = ant.find_food((100, 100))
    assert result is not None, "Should return coordinates when ant is inside radius"


def test_carry_food():
    pass


if __name__ == "__main__":
    test_move()
    