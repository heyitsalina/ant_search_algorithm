
# Algorithms Used in Ant Food Search Simulation

## Overview

This document outlines the algorithms and decision-making processes employed in the Ant Food Search Simulation. It focuses on how ants find food, navigate using pheromones, interact with food sources, and manage colony resources.

## Ant Movement and Decision Making

Ants decide their movement based on a combination of random exploration and pheromone trail following. The movement is influenced by several factors including the presence of pheromones, obstacles, and the ant's current state (searching for food or returning to the colony).

### Key Processes:

- **Initial Direction**: At the start, ants move in a randomly chosen direction until some ants find food. They do this this by generating a random angle theta and using it to create a normalized direction vector scaled by self.step_size. On subsequent moves, it randomly adjusts this direction within a specific angle range (angle_offset), applies this rotation to maintain or change its trajectory, and recalculates the future position based on the updated direction. The direction vector's length is normalized and scaled by the step size to ensure consistent movement speed.
- **Pheromone Influence**: If ants find food, their moving behaviour changes. Ants adjust their path based on pheromone concentrations, favoring directions with higher pheromone levels. When pheromone influence is factored in, the method integrates the pheromone direction into the object's movement direction if pheromone_direction is provided. This pheromone direction is scaled by self.pheromone_influence to adjust its impact on the overall direction. The object's direction is then the sum of the rotated direction and the scaled pheromone direction. This combined direction is normalized and scaled by the step size, ensuring the movement is influenced by both the object's own direction and the pheromone trail, guiding the object more effectively towards or away from certain areas based on the pheromone signals.
- **Food Detection and Collection**: Upon locating food, ants collect it and switch their status to return to the colony, leaving a pheromone trail.

## Pheromone Management

Pheromones are crucial for indirect communication between ants. They leave pheromone trails to guide other ants to food sources and back to the colony.

### Key Processes:

- **Pheromone Deposition**: Ants deposit pheromones along their path as they move.
- **Pheromone Evaporation**: Over time, pheromone intensity decreases, simulating natural evaporation.
- **Trail Following**: Ants sense and follow pheromone trails to find food sources or return to the colony.
