class Obstacle:
    """
    Initializes an obstacle object within the search space.
    -------

    Args:
    coordinates (tuple):
        The (x, y) coordinates of the obstacle in the search space.
    size (tuple):
        The size of the obstacle in the search space. Defaults to (50, 50).
    """
    def __init__(self, coordinates, size=(50, 50)):
        self.coordinates = coordinates
        self.size = size
        