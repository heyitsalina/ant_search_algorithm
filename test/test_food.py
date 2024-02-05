import pytest
from resources.food import Food


def test_food_initialization():
    food = Food(size=10, coordinates=(100,100), amount_of_food=100)

    assert food.size == 10 
    assert food.coordinates == (100, 100)
    assert food.amount_of_food == 100
    assert food.show_life_bar is True



if __name__ == "__main__":
    test_food_initialization()