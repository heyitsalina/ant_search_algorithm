class World:
    def __init__(self, size=(720, 480), obstacles=0):
        """
        This class represents the world in which the ants are moving and the obstacles, food are.
        
        Args:
        size (tuple):
            Represents the width and height of the world.
        obstacles (int):
            The number of obstacles in the world. 
        """
        
        self.width, self.height = size
        self.obstacles = obstacles

    def generate_obstacles(self):
        pass
