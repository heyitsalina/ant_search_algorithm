# Ant Food Search Simulation Architecture

## Pheromone Management (`pheromone.py`)

Manages pheromone levels in the simulation.

### Key Methods:

- `leave_pheromone`: Marks trails based on ant movements.
- `reduce_pheromones`: Applies decay to pheromone levels over time.

## Simulation Control (`simulation.py`)

Central hub for simulating ant and food interactions within an environment.

### Key Methods:

- `next_epoch`: Advances the simulation, updating ant positions and interactions.
- `add_colony`, `add_food`, `add_obstacle`: Adds colonies, food and obstacle sources to the simulation.
- `check_future_position`: Ensures entities stay within bounds.
- `check_for_obstacles`: Ensures that entities do not collide with obstacles and adjusts the future position if it overlaps with obstacles.
- `map_ant_coordinates_to_pheromone_index`: Maps ant coordinates to the corresponding indices in the pheromone grid.
- `find_pheromone_trace`: Searches for pheromone traces in the vicinity of the specified coordinates, considering the given search radius.
- `get_pheromone_position`: Retrieves the position of the strongest pheromone signal within the specified search radius.

## Food Sources (`food.py`)

Represents food sources with specific locations and amounts.

### Key Methods:

- `move_randomly_after_while`: Optionally moves the food source after a set number of epochs.

## Ant Entities (`ant.py`)

Simulates individual ant behaviors in food search and collection.

### Key Methods:

- `move`: Simulates the movement of the ant. It applies a random rotation to the existing direction, potentially influenced by pheromones, and updates its position accordingly.
- `is_near_target`: Checking if the ant is within a specified radius of a given target position to interact.
- `carry_food`, `drop_food`: Interactions with food sources for collection.
- `switch_pheromone`: Switching the pheromone status.

## Colony Management (`colony.py`)

Manages ant colonies, including resource allocation and ant behavior coordination.

### Key Methods:

- `add_ants`: Generation and management of ants within the colony.

This focused overview emphasizes the system's modular design and the interaction between its components through specific methods, offering a clearer understanding of how the simulation operates.
