import pygame
import random


class Snake:
    def __init__(self, x, y):
        self.body = [(y, x), (y, x - 1), (y, x - 2)]
        self.head = [(y, x)]
        self.direction = 'RIGHT'

    def move(self, width, height):
        head = self.body[0]
        if self.direction == 'UP':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'DOWN':
            new_head = (head[0] + 1, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'RIGHT':
            new_head = (head[0], head[1] + 1)

        # Wrap around the screen
        new_head = (new_head[0] % height, new_head[1] % width)

        return new_head


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.obstacles = []

    def place_snake(self, snake):
        for y, x in snake.body:
            self.grid[y][x] = 'O'

    def place_food(self, food):
        y, x = food
        self.grid[y][x] = 'X'

    def place_obstacles(self, obstacles):
        for obstacle in obstacles:
            y, x = obstacle
            self.grid[y][x] = 'H'
            self.obstacles.append(obstacle)


class GameLogic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(width // 2, height // 2)
        self.board = Board(width, height)
        self.food = self.generate_food()
        self.obstacles = self.generate_obstacles()  # Generate obstacles
        self.speed = 1.0  # Initial speed (1 square per second)
        self.game_over = False

    def generate_food(self):
        incorrect_position = True
        while incorrect_position:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (y, x) not in self.snake.body and (y, x) not in self.board.obstacles:
                incorrect_position = False
                return y, x

    def generate_obstacles(self):
        # TODO: Implement the logic that the obstacles will not generate in the way or inside the snake.
        obstacles = []
        max_obstacle_size = 3
        max_obstacle_squares = 5

        if self.width > 5 and self.height > 5:
            obstacle_num = 0  # Default

            if self.width >= 8 and self.height >= 8:
                obstacle_num = 1
            if self.width >= 10 and self.height >= 10:
                obstacle_num = 2
            if self.width >= 15 and self.height >= 15:
                obstacle_num = 3
            if self.width >= 18 and self.height >= 15:
                obstacle_num = 4
            if self.width == 25 and self.height == 25:
                obstacle_num = 5  # Adjust according to width

            for _ in range(obstacle_num):
                # Generate a random position for the obstacle
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                obstacle = [(y, x)]

                # Generate the width and height of the obstacle
                obstacle_width = random.randint(1, max_obstacle_size)
                obstacle_height = random.randint(1, max_obstacle_size)

                # Ensure that the obstacle doesn't exceed the boundaries of the board
                obstacle_width = min(obstacle_width, self.width - x)
                obstacle_height = min(obstacle_height, self.height - y)

                # Generate the obstacle squares
                while len(obstacle) < max_obstacle_squares:
                    # Generate the direction for the next square
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)
                    for dy, dx in directions:
                        new_y = obstacle[-1][0] + dy
                        new_x = obstacle[-1][1] + dx
                        if 0 <= new_y < self.height and 0 <= new_x < self.width and (new_y, new_x) not in obstacle:
                            obstacle.append((new_y, new_x))
                            break
                    else:
                        break  # Unable to add more squares, break out of the loop

                obstacles.append(obstacle)

        return obstacles

    def move_snake(self):
        new_head = self.snake.move(self.width, self.height)
        if new_head in self.snake.body[1:] or new_head in self.board.obstacles:
            self.game_over = True
            return

        self.snake.body.insert(0, new_head)
        self.snake.head.insert(0, new_head)
        self.snake.head.pop()

        if new_head == self.food:
            self.food = self.generate_food()
            self.speed *= 1.07  # Increase speed by 7%
        else:
            self.snake.body.pop()

    def update_board(self):
        self.board = Board(self.width, self.height)
        self.board.place_snake(self.snake)
        self.board.place_food(self.food)

        # Place obstacles
        for obstacle in self.obstacles:
            self.board.place_obstacles(obstacle)


class SnakeGameGUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_size = 30
        self.grid_color = (50, 50, 50)
        self.snake_head_color = (0, 170, 0)  # Color of the snake's head
        self.snake_body_color = (0, 255, 0)  # Color of the snake's body
        self.obstacle_color = (170, 170, 170)  # Color of the obstacles
        self.frame_width = self.block_size * 2
        self.frame_color = (50, 50, 50)  # Color of the frame
        self.screen = pygame.display.set_mode((self.width * self.block_size + self.frame_width * 2,
                                               self.height * self.block_size + self.frame_width * 2))
        pygame.display.set_caption("Snake Game")

    def draw_board(self, board, speed, snake, player_name):
        self.screen.fill((0, 0, 0))

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
                    if (y, x) in snake.head:  # Check if the cell is the snake's head
                        pygame.draw.ellipse(self.screen, self.snake_head_color, (
                            element_x_indentation, element_y_indentation, self.block_size - 2,
                            self.block_size - 2))
                    else:
                        pygame.draw.rect(self.screen, self.snake_body_color, (
                            element_x_indentation, element_y_indentation, self.block_size - 2,
                            self.block_size - 2))
                elif board.grid[y][x] == 'X':
                    pygame.draw.ellipse(self.screen, (255, 0, 0), (
                        element_x_indentation, element_y_indentation, self.block_size - 2, self.block_size - 2))
                elif board.grid[y][x] == 'H':
                    pygame.draw.rect(self.screen, self.obstacle_color, (
                        element_x_indentation, element_y_indentation, self.block_size - 2,
                        self.block_size - 2))

        # Draw speed text
        font = pygame.font.SysFont(None, int(self.frame_width / 2.5))
        speed_text = font.render(f"Speed: {speed:.2f} squares per second", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, self.height * self.block_size + self.frame_width * 1.5))

        # Draw player's name and score
        font_player = pygame.font.SysFont(None, int(self.frame_width / 2.5))
        player_text = font_player.render(f"Player: {player_name}", True, (255, 255, 255))
        self.screen.blit(player_text, (10, 5))

        font_score = pygame.font.SysFont(None, int(self.frame_width / 2))
        score_text = font_score.render(f"Score: {len(snake.body) - 3}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.frame_width * 3, 5))

        pygame.display.update()


class SnakeGame:
    def __init__(self, width, height, player_name):
        self.width = width
        self.height = height
        self.player_name = player_name

        self.gui = SnakeGameGUI(width, height)
        self.game_logic = GameLogic(width, height)

    def run_game(self):
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

        print("Game Over!")
        print(f"Score: {len(self.game_logic.snake.body) - 3}")


# Example usage:
# width = int(input("Enter the width of the board: "))
# height = int(input("Enter the height of the board: "))
# player_name = input("Enter your name: ")

pygame.init()
game = SnakeGame(25, 25, "test")
game.run_game()
pygame.quit()
