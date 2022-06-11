"""Handles the creating of obstacles within the game instance."""
from random import randint
from typing import Literal, Optional

import pygame

from .coordinate import Coordinate


class Obstacle:
    """Class for handling the creating of obstables."""
    def __init__(self) -> None:
        self.size = (50, 300)
        bottom_rectangle_y = randint(235, 360)
        self.position = [
            Coordinate(700, bottom_rectangle_y),
            Coordinate(700, bottom_rectangle_y-(1.8*235))
        ]
        self.can_move = True

    def get_rect(self) -> tuple[pygame.Rect, pygame.Rect]:
        """Get rect"""
        return (
            pygame.Rect(
                tuple(self.position[0])[0], tuple(self.position[0])[1], self.size[0], self.size[1]
            ),
            pygame.Rect(
                tuple(self.position[1])[0], tuple(self.position[1])[1], self.size[0], self.size[1]
            )
        )

    def move(self) -> None:
        """Move the obstace foward."""
        if self.position[0].x < 45:
            self.can_move = False
        self.position[0].x -= 3
        self.position[1].x -= 3
