import numpy as np

class pheromone:
    def __init__(self, pheromone_shape):
        self.pheromones = np.zeros((pheromone_shape[0], pheromone_shape[1], 2))

    def put_pheromone(self):
        pass
    
    def get_pheromone_level(self):
        pass

    def reduce_pheromone(self, reducing_factor, time_frame):
        pass