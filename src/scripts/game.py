"""Handles the creating and running of the game instance."""
from collections import deque
from random import randint
from sys import exit as sys_exit
from sys import stderr

import pygame

from .logger import Logger, LoggingLevels
from .obstacle import Obstacle
from .player import Player


class Game:
    """Main class for creating and running a game instance."""
    def start(self) -> None:
        """Starts the program and intializes pygame and related variables."""
        self.logger = Logger("./logging.log", __name__)
        self.logger.set_settings(
            name=True,
            date_time=(True, None),
            logging_level=(False, LoggingLevels.INFO),
            stack_trace=True
        )
        self.logger.logging_state = True
        with open(self.logger.defualt_src, "w", encoding="UTF-8"):
            pass
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
        self.paused = False
        self.obstacle_queue: deque[Obstacle] = deque([Obstacle()])
        self.current_obstacles: deque[Obstacle] = deque([])
        self.player = Player(
            pygame.transform.scale(
                pygame.image.load("src/assets/images/sprites/bird.png"), (65, 50)
            )
        )
        self.update()

    def update(self) -> None:
        """Main update loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if (
                        (self.game_active and not self.paused)
                        and (event.key in {pygame.K_SPACE, pygame.K_UP})
                    ):
                        if self.game_active:
                            self.player.move_player(
                                self.player.position.x, self.player.position.y - 50
                            )
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                    if event.key == pygame.K_ESCAPE:
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True
            if self.paused and self.game_active:
                self.pause()
            elif self.game_active:
                self.display_background()
                self.draw_obstacle()
                self.update_player()
            if not self.game_active:
                self.display_start_screen()
            self.display_fps()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self) -> None:
        """Quits the current game process."""
        pygame.quit()
        self.save()
        sys_exit(0)

    def save(self) -> None:
        """Saves all game data."""
        player_data = self.player.get_player_data()
        self.player.set_player_data(
            self.player.current_high_score if self.player.current_high_score > player_data[
                "highest_score"
            ] else None,
            player_data["total_attempts"] + self.player.current_attempts
        )

    def pause(self) -> None:
        """Pauses the game."""
        self.screen.fill( (0, 0, 0) )
        pause_message = self.font.render(
            "Paused",
            False,
            (255, 255, 255)
        )
        resume_message = self.font.render(
            "Press Esc to resume the game",
            False,
            (255, 255, 255)
        )
        self.screen.blit(pause_message, pause_message.get_rect(center=(400, 50)))
        self.screen.blit(resume_message, resume_message.get_rect(center=(400, 125)))

    def update_player(self) -> None:
        """Updates the player's position and moves them down."""
        self.screen.blit(
            self.player.sprite, tuple(self.player.position)
        )
        self.player.move_player(self.player.position. x, self.player.position.y + 2.5)
        obstacle_list: list[pygame.Rect] = []
        if self.current_obstacles:
            rect = self.current_obstacles[0].get_rect()
            obstacle_list.extend((rect[0], rect[1]))
        if int(self.player.position.y) not in range(10, 375) or self.player.rect.collidelist(obstacle_list) != -1:
            self.restart()

    def restart(self) -> None:
        """Restarts the game so the player can play another game."""
        self.player.kill()
        self.player.previous_score = self.player.current_score
        self.player.current_score = 0
        self.game_active = False
        self.current_obstacles.clear()
        self.obstacle_queue.clear()

    def display_start_screen(self) -> None:
        """Displays the main menu screen."""
        self.screen.fill( (36, 97, 227) )
        score_message = self.font.render(
            f"Score: {self.player.previous_score}",
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
            f"{self.player.get_player_data()}",
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
        score = self.font.render(
            f"{self.player.current_score}",
            False,
            (252, 183, 114)
        )
        self.screen.blit(score, score.get_rect(center=(
            (-len(str(self.player.current_score)) - 2)
            * len(str(self.player.current_score)) + 780,
            25
        )))

    def draw_obstacle(self):#, current_time: int) -> None:
        """Draws rectangle to the screen."""
        if self.current_obstacles:
            to_remove: list[Obstacle] = []
            for i in self.current_obstacles:                    
                if i.can_move:
                    for j in i.get_rect():
                        pygame.draw.rect(self.screen, (23, 252, 3), j)
                    i.move()
                else:
                    to_remove.append(i)
            for i in to_remove:
                self.current_obstacles.remove(i)
                self.player.current_score += 1
        if self.obstacle_queue:
            if len(self.current_obstacles) < 10 and randint(0, 100) == randint(0, 100):
                self.current_obstacles.append(self.obstacle_queue.popleft())
        else:
            self.obstacle_queue.append(Obstacle())

    def display_fps(self) -> None:
        """Displays the fps counter to the upper left courner."""
        fps_counter = self.font.render(
            str(int(self.clock.get_fps())),
            False,
            (255, 255, 255),
            (0, 0, 0)
        )
        self.screen.blit(fps_counter, fps_counter.get_rect(center=(20, 20)))
