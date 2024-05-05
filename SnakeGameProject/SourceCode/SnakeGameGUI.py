import pygame
from Board import Board
from GameLogic import GameLogic

class SnakeGameGUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_size = 30
        self.color_text = (181, 228, 140)
        self.grid_color = (50, 50, 50)
        self.snake_head_color = (60, 152, 132)  # Color of the snake's head
        self.snake_body_color = (29, 103, 83)  # Color of the snake's body
        self.obstacle_color = (120, 120, 120)  # Color of the obstacles
        self.food_color = (217, 237, 146)
        self.frame_width = self.block_size * 2
        self.frame_color = (24, 78, 119)  # Frame color
        self.screen = pygame.display.set_mode((self.width * self.block_size + self.frame_width * 2,
                                               self.height * self.block_size + self.frame_width * 2))
        pygame.display.set_caption("Snake Game")

    def draw_board(self, board, speed, snake, player_name):
        self.screen.fill((0, 0, 0))  # Color of the background of the grid
        offset = self.block_size // 20  # Adjust this value to change the size of the triangle

        # Draw frame around the board
        pygame.draw.rect(self.screen, self.frame_color,
                         (0, 0, self.width * self.block_size + self.frame_width * 2,
                          self.height * self.block_size + self.frame_width * 2), self.frame_width)

        for y in range(self.height):
            for x in range(self.width):
                element_x_indentation = x * self.block_size + self.frame_width + 1
                element_y_indentation = y * self.block_size + self.frame_width + 1

                pygame.draw.rect(self.screen, self.grid_color,
                                 (x * self.block_size + self.frame_width, y * self.block_size + self.frame_width,
                                  self.block_size, self.block_size), 1)
                if board.grid[y][x] == 'O':
                    if (y, x) == snake.head[0]:  # Check if the cell is the snake's head
                        if snake.direction == 'UP':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + self.block_size // 2, element_y_indentation + offset),
                                (element_x_indentation + offset, element_y_indentation + self.block_size - offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation +
                                 self.block_size - offset)
                            ])
                        elif snake.direction == 'DOWN':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size // 2, element_y_indentation +
                                 self.block_size - offset)
                            ])
                        elif snake.direction == 'LEFT':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + self.block_size - offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation +
                                 self.block_size - offset),
                                (element_x_indentation + offset, element_y_indentation + self.block_size // 2)
                            ])
                        elif snake.direction == 'RIGHT':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + offset, element_y_indentation + offset),
                                (element_x_indentation + offset, element_y_indentation + self.block_size - offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation +
                                 self.block_size // 2)
                            ])
                    else:
                        pygame.draw.rect(self.screen, self.snake_body_color, (
                            element_x_indentation, element_y_indentation, self.block_size - 2,
                            self.block_size - 2))

                elif board.grid[y][x] == 'X':
                    pygame.draw.ellipse(self.screen, self.food_color, (
                        element_x_indentation, element_y_indentation, self.block_size - 2, self.block_size - 2))
                elif board.grid[y][x] == 'H':
                    pygame.draw.rect(self.screen, self.obstacle_color, (
                        element_x_indentation, element_y_indentation, self.block_size - 2,
                        self.block_size - 2))

        # Draw speed text
        font = pygame.font.SysFont('speed', int(self.frame_width / 2.5))
        speed_text = font.render(f"Speed: {speed:.2f} squares per second", True, self.color_text)
        self.screen.blit(speed_text, (10, self.height * self.block_size + self.frame_width * 1.5))

        # Draw player's name and score
        font_player = pygame.font.SysFont('player', int(self.frame_width / 2.5))
        player_text = font_player.render(f"Player: {player_name}", True, self.color_text)
        self.screen.blit(player_text, (10, 5))

        font_score = pygame.font.SysFont('score', int(self.frame_width / 2))
        score_text = font_score.render(f"Score: {len(snake.body) - 3}", True, self.color_text)
        player_text_height = font_player.size(f"Player: {player_name}")[1]
        self.screen.blit(score_text, (10, player_text_height + self.frame_width // 3))

        pygame.display.update()
