"""Handles the creating of obstacles within the game instance."""
import pygame
from src.scripts.coordinate import Coordinate


class Obstacle:
    """Class for handling the creating of obstables."""
    def __init__(self) -> None:
        self.size = (50, 300)
        self.position = [
            Coordinate(700, 400),
            Coordinate(700, 0)
        ]
        self.can_move = True

    def get_rect(self) -> tuple[pygame.Rect, pygame.Rect]:
        """Get rect"""
        return (
            pygame.Rect(
                tuple(self.position[0])[0], tuple(self.position[0])[1], self.size[0], self.size[1]
            ), # bottom rect
            pygame.Rect(
                tuple(self.position[1])[0], tuple(self.position[1])[1], self.size[0], self.size[1]
            )  # top rect
        )

    def move(self) -> None:
        """Move the obstace foward."""
        if self.position[0].x < 45:
            self.can_move = False
        self.position[0].x -= 3
        self.position[1].x -= 3
