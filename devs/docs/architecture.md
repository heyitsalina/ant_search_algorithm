# Ant Food Search Simulation Architecture

## Pheromone Management (`pheromone.py`)

Manages pheromone levels in the simulation.

### Key Methods:

- `leave_pheromone`: Marks trails based on ant movements.
- `get_pheromone_level`: Retrieves pheromone levels at specific locations.
- `reduce_pheromones`: Applies decay to pheromone levels over time.

## Simulation Control (`simulation.py`)

Central hub for simulating ant and food interactions within an environment.

### Key Methods:

- `next_epoch`: Advances the simulation, updating ant positions and interactions.
- `add_colony`, `add_food`: Adds colonies and food sources to the simulation.
- `check_future_position`: Ensures entities stay within bounds.

## Food Sources (`food.py`)

Represents food sources with specific locations and amounts.

### Key Methods:

- `move_randomly_after_while`: Optionally moves the food source after a set number of epochs.

## Ant Entities (`ant.py`)

Simulates individual ant behaviors in food search and collection.

### Key Methods:

- Movement and decision-making based on environmental cues and pheromone trails.
- Interactions with food sources for collection.

## Colony Management (`colony.py`)

Manages ant colonies, including resource allocation and ant behavior coordination.

### Key Methods:

- Generation and management of ants within the colony.
- Accumulation of resources from collected food.

This focused overview emphasizes the system's modular design and the interaction between its components through specific methods, offering a clearer understanding of how the simulation operates.
