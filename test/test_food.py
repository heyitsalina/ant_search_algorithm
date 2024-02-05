import pytest
from resources.food import *


def test_food_initialization():
    food = Food(size=10, coordinates=(100,100), amount_of_food=100)

    assert food.size == 10 
    assert food.coordinates == (100, 100)
    assert food.amount_of_food == 100
    assert food.show_life_bar == True

