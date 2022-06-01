"""Handles the creating and running of the game instance."""
from sys import exit as sys_exit
from sys import stderr

import pygame

from .logger import Logger
from .obstacle import Obstacle
from .player import Player


class Game:
    """Main class for creating and running a game instance."""
    def start(self) -> None:
        """Starts the program and intializes pygame and related variables."""
        self.logger = Logger(
            "./logging.log",
            __name__
        )
        self.logger.set_logging_settings(
            True,
            True,
            True,
            True
        )
        pygame.init()
        stderr.write = self.logger.log_exception
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Flappy Bird")
        self.sky_surface = pygame.image.load(
            "./src/assets/images/background/sky.png"
        ).convert()
        self.ground_surface = pygame.image.load(
            "./src/assets/images/background/ground.png"
        ).convert()
        self.font = pygame.font.Font("src/assets/images/fonts/pixel_type.ttf", 50)

        self.clock = pygame.time.Clock()
        self.game_active = False
        self.player = Player()
        self.obstacle_list: list[Obstacle] = []
        self.update()

    def update(self) -> None:
        """Main update loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_active = True
            0/0
            if self.game_active:
                self.display_background()
            else:
                self.display_start_screen()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self) -> None:
        """Quits the current game process."""
        pygame.quit()
        self.save()
        sys_exit()

    def save(self) -> None:
        """Saves all game data."""
        player_data = self.player.get_player_data()["player"]
        self.player.set_player_data(
            self.player.current_high_score if self.player.current_high_score > player_data[
                "highest_score"
            ] else None,
            player_data["total_attempts"] + self.player.current_attempts
        )

    def display_start_screen(self) -> None:
        """Displays the main menu screen."""
        self.screen.fill( (36, 97, 227) )
        score_message = self.font.render(
            f"Score: {self.player.current_score}",
            False,
            (255, 255, 255)
        )
        start_prompt = self.font.render(
            'Press "space" to start!',
            False,
            (255, 255, 255)
        )
        attempts_message = self.font.render(
            f"Attempt {self.player.current_attempts}",
            False,
            (255, 255, 255)
        )
        high_score_message = self.font.render(
            f"High score: {self.player.current_high_score}",
            False,
            (255, 255, 255)
        )
        life_time_stats = self.font.render(
            f"{self.player.get_player_data()['player']}",
            False,
            (255, 255, 255)
        )
        self.screen.blit(score_message, score_message.get_rect(center=(400, 330)))
        self.screen.blit(start_prompt, start_prompt.get_rect(center=(400, 300)))
        self.screen.blit(attempts_message, attempts_message.get_rect(center=(400, 200)))
        self.screen.blit(high_score_message, high_score_message.get_rect(center=(
            (-len(str(self.player.current_high_score)) - 2)
            * len(str(self.player.current_high_score)) + 690,
            25
        )))
        self.screen.blit(life_time_stats, life_time_stats.get_rect(center=(400, 100)))

    def display_background(self) -> None:
        """Displays the background."""
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))
