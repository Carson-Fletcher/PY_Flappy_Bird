"""Handles the creating and movement of players within the game instance."""
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """Class for creating and handling the player within the game."""
    name = "Player"
    current_attempts = 0
    current_score = 0
    current_high_score = 0

    def get_player_data(self) -> dict[str, dict[str, int]]:
        """Loads the player data from the player data json file."""
        with open("./src/assets/json/player.json", encoding="UTF-8") as file:
            return json.load(file)

    def set_player_data(
        self,
        highest_score: Optional[int] = None,
        total_attempts: Optional[int] = None
    ) -> None:
        """Sets the player data in the player data json file."""
        data = self.get_player_data()
        with open("./src/assets/json/player.json", "r+", encoding="UTF-8") as file:
            data[
                "player"
            ]["highest_score"] = highest_score if highest_score is not None else data[
                "player"
            ]["highest_score"]
            data[
                "player"
            ]["total_attempts"] = total_attempts if total_attempts is not None else data[
                "player"
            ]["total_attempts"]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def reset_player_data(self) -> None:
        """Reset player data."""
        data = self.get_player_data()
        with open("./src/assets/json/player.json", "r+", encoding="UTF-8") as file:
            data["player"]["highest_score"] = 0
            data["player"]["total_attempts"] = 0
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
