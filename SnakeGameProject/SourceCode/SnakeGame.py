import pygame
from GameLogic import GameLogic
from SnakeGameGUI import SnakeGameGUI
from StartWindow import StartWindow
from EndGameWindow import EndGameWindow


class SnakeGame:
    def __init__(self):
        self.game_logic = None
        self.gui = None
        screen_info = pygame.display.Info()
        self.width = screen_info.current_w * 2 // 3
        self.height = screen_info.current_h * 2 // 3
        self.start_window = StartWindow(self.width, self.height)
        self.player_name, self.size = None, None

    def start_game(self):
        self.gui = SnakeGameGUI(self.size, self.size)
        self.game_logic = GameLogic(self.size, self.size)
        clock = pygame.time.Clock()

        while not self.game_logic.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_logic.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.game_logic.snake.direction != 'DOWN':
                        self.game_logic.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.game_logic.snake.direction != 'UP':
                        self.game_logic.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.game_logic.snake.direction != 'RIGHT':
                        self.game_logic.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.game_logic.snake.direction != 'LEFT':
                        self.game_logic.snake.direction = 'RIGHT'

            self.game_logic.move_snake()
            self.game_logic.update_board()
            self.gui.draw_board(self.game_logic.board, self.game_logic.speed, self.game_logic.snake, self.player_name)
            clock.tick(self.game_logic.speed)  # Adjust game speed

        game_result = self.game_logic.endgame_text
        print(game_result)
        print(f"Score: {len(self.game_logic.snake.body) - 3}")

        end_game_window = EndGameWindow(self.start_window.width, self.start_window.height, game_result)
        while not end_game_window.done:
            end_game_window.draw_window()
            action = end_game_window.handle_events()
            if action == "save_exit":
                # Implement the logic to save the game and exit
                return
            elif action == "play_again":
                # Reset the start window with the player's name pre-filled
                self.start_window = StartWindow(self.width, self.height, self.player_name, self.size)
                self.run_game()  # Restart the game
                break

    def run_game(self):
        while not self.start_window.done:
            self.start_window.draw_window()
            self.player_name, self.size = self.start_window.handle_events()
            if self.player_name and self.size:
                break

        if self.player_name is None or self.size is None:
            return  # Ending the game if the start window was closed.

        self.start_game()  # Start the game
