import pytest
from resources.simulation import Simulation

sim = Simulation()

def test_next_epoch():
    for _ in range(5):
        sim.next_epoch()

