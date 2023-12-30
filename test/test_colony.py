from resources.colony import Colony
import pytest
import numpy as np

colony = Colony(amount=10, size=10, coordinates=(100.0, 100.0), color="brown")
amount_to_carry = 20     # anpassbar
step_size = 5           # anpassbar
colony.add_ants(amount_to_carry, step_size)

def test_add_ants():
    initial_ant_count = len(colony.ants)
    assert len(colony.ants) == initial_ant_count + colony.amount
    for ant in colony.ants:
        assert ant.amount_to_carry == amount_to_carry
        assert ant.step_size == step_size
        assert ant.coordinates == (colony.coordinates[0] + 50, colony.coordinates[1] + 50)

if __name__ == "__main__":
    test_add_ants()