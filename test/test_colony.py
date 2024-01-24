from resources.colony import Colony
import pytest
import numpy as np

colony = Colony(grid_pheromone_shape=(100, 100), amount=10, size=10, coordinates=(100.0, 100.0), color=(1, 1, 1, 1))

def test_add_ants():
    assert colony.amount == len(colony.ants)
    colony.ants = []
    amount_to_carry = 20
    step_size = 5
    colony.add_ants(amount_to_carry, step_size)
    for ant in colony.ants:
        assert ant.amount_to_carry == amount_to_carry
        assert ant.step_size == step_size
        assert ant.coordinates == (colony.coordinates[0] + 50, colony.coordinates[1] + 50)

if __name__ == "__main__":
    test_add_ants()
