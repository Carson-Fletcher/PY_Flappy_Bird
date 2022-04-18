"""Handles the creating and running of the game instance."""
from sys import exit as sys_exit

import pygame


class Game:
    """Main class for creating and running a game instance."""

    def __init__(self) -> None:
        self.screen: pygame.Surface
        self.clock: pygame.time.Clock

    def start(self) -> None:
        """Starts the game instance and creates a new window for the game."""
        print(pygame.__file__)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        self.screen.fill((155, 0, 200))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Hello, World!")
        self.update()

    def update(self) -> None:
        """Main update loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self) -> None:
        """Quits the current game process."""
        pygame.quit()
        sys_exit()
