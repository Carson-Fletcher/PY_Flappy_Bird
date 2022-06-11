"""Module for wrapper class around coordinates."""
from dataclasses import dataclass


@dataclass
class Coordinate:
    """Wrapper class for handling coordinates."""
    x: float
    y: float

    def __iter__(self):
        for i in (self.x, self.y):
            yield i
