import pytest
from resources.simulation import Simulation

sim = Simulation()


def test_next_epoch():
    for _ in range(5):
        sim.next_epoch()


def test_simulation_initialisation():
    sim = Simulation()

    assert sim.food == []
    assert sim.colonies == []
    assert sim.running is False
    assert sim.bounds == ()


def test_add_colony_and_food():
    sim = Simulation()
    
    sim.add_colony("Colony1")
    sim.add_food("Food1")

    assert sim.colonies == ["Colony1"]
    assert sim.food == ["Food1"]

def test_check_future_position():

    pass


def test_map_ant_coordinates_to_pheromone_index():

    pass
