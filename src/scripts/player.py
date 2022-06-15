"""Handles the creating and movement of players within the game instance."""
from dataclasses import dataclass
from json import dump as json_dump
from json import load as json_load
from typing import Optional

import pygame
from src.scripts.coordinate import Coordinate


@dataclass
class Player:
    """Class for creating and handling the player within the game."""
    sprite: pygame.surface.Surface
    name = "Player"
    current_attempts = 0
    current_score = 0
    previous_score = 0
    current_high_score = 0
    _starting_position = Coordinate(130, 100)
    position: Coordinate = _starting_position

    def __post_init__(self) -> None:
        self.rect = self.sprite.get_rect()

    def kill(self) -> None:
        """Kill and reset the player."""
        self.position = Coordinate(130, 100)
        self.current_attempts += 1
        if self.current_score > self.current_high_score:
            self.current_high_score = self.current_score

    def move_player(self, x: float, y: float) -> None:
        """Moves the player up by the given amount."""
        self.position.x = x
        self.position.y = y

    def get_player_data(self) -> dict[str, int]:
        """Loads the player data from the player data json file."""
        with open("./src/assets/json/data.json", encoding="UTF-8") as file:
            return json_load(file)["player"]

    def set_player_data(
        self,
        highest_score: Optional[int] = None,
        total_attempts: Optional[int] = None
    ) -> None:
        """Sets the player data in the player data json file."""
        data = self.get_player_data()
        with open("./src/assets/json/data.json", "r+", encoding="UTF-8") as file:
            data["highest_score"] = highest_score if highest_score is not None else data[
                "highest_score"
            ]
            data["total_attempts"] = total_attempts if total_attempts is not None else data[
                "total_attempts"
            ]
            file.seek(0)
            json_dump({"player": data}, file, indent=4)
            file.truncate()

    def reset_player_data(self) -> None:
        """Reset player data."""
        data = self.get_player_data()
        with open("./src/assets/json/data.json", "r+", encoding="UTF-8") as file:
            data["highest_score"] = 0
            data["total_attempts"] = 0
            file.seek(0)
            json_dump({"player": data}, file, indent=4)
            file.truncate()
