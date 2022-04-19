"""Handles the creating and running of the game instance."""
from sys import exit as sys_exit

import pygame


class Game:
    """Main class for creating and running a game instance."""

    def __init__(self) -> None:
        self.game_name = "Flappy Bird"
        self.screen: pygame.surface.Surface
        self.sky_surface: pygame.surface.Surface
        self.ground_surface: pygame.surface.Surface
        self.clock: pygame.time.Clock
        self.font: pygame.font.Font
        self.game_active: bool = False

    def start(self) -> None:
        """Starts the game instance and creates a new window for the game."""
        pygame.init()

        # Init screen and game sprites
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
        self.update()

    def update(self) -> None:
        """Main update loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            if self.game_active:
                self.screen.blit(self.sky_surface, (0, 0))
                self.screen.blit(self.ground_surface, (0, 300))
            else:
                self.screen.fill((36, 97, 227))
                score_message = self.font.render('Your score: {}',False, (255, 255, 255))
                score_message_rect = score_message.get_rect(center=(400, 330))
                self.screen.blit(score_message,score_message_rect)
            pygame.display.update()
            self.clock.tick(60)

    def quit(self) -> None:
        """Quits the current game process."""
        pygame.quit()
        sys_exit()
