from random import choice
from typing import List

import numpy as np

from ...bot import Bot
from ...constants import Move, MOVE_VALUE_TO_DIRECTION
from ...snake import Snake


def is_on_grid(pos, grid_size):
    return 0 <= pos[0] < grid_size[0] and 0 <= pos[1] < grid_size[1]


def collides(head, snakes):
    for snake in snakes:
        if snake.collides(head):
            return True
    return False


class SimpleEater(Bot):
    """
    Move towards food, but stay away from the heads of other snakes
    """

    @property
    def name(self):
        return 'Simple Eater'

    @property
    def contributor(self):
        return 'Nobleo'

    def determine_next_move(self, snake: Snake, other_snakes: List[Snake], candies: List[np.array]) -> Move:
        moves = self._determine_possible_moves(snake, other_snakes[0])
        return self.choose_towards_candy(moves, snake, candies)

    def _determine_possible_moves(self, snake, other_snake) -> List[Move]:
        """
        Return a list with all moves that we want to do. Later we'll choose one from this list randomly. This method
        will be used during unit-testing
        """
        # highest priority, a move that is on the grid
        on_grid = [move for move in MOVE_VALUE_TO_DIRECTION
                   if is_on_grid(snake[0] + MOVE_VALUE_TO_DIRECTION[move], self.grid_size)]
        if not on_grid:
            return list(Move)

        # then avoid collisions with other snakes
        collision_free = [move for move in on_grid
                          if is_on_grid(snake[0] + MOVE_VALUE_TO_DIRECTION[move], self.grid_size)
                          and not collides(snake[0] + MOVE_VALUE_TO_DIRECTION[move], [snake, other_snake])]
        if collision_free:
            return collision_free
        else:
            return on_grid

    def choose_towards_candy(self, moves: List[Move], snake, candies):
        if not candies:
            return choice(moves)
        return min(moves,
                   key=lambda move: self.distance_to_closest_candy(snake[0] + MOVE_VALUE_TO_DIRECTION[move], candies))

    def distance_to_closest_candy(self, position, candies):
        distances = [np.linalg.norm(position - candy, 1) for candy in candies]
        return min(distances)
