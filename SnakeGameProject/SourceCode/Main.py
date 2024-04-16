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

    def place_snake(self, snake):
        for y, x in snake.body:
            self.grid[y][x] = 'O'

    def place_food(self, food):
        y, x = food
        self.grid[y][x] = 'X'


class GameLogic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(width // 2, height // 2)
        self.board = Board(width, height)
        self.food = self.generate_food()
        self.speed = 1.0  # Initial speed (1 square per second)
        self.game_over = False

    def generate_food(self):
        incorrect_position = True
        while incorrect_position:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (y, x) not in self.snake.body:
                incorrect_position = False
                return y, x

    def move_snake(self):
        new_head = self.snake.move(self.width, self.height)
        if new_head in self.snake.body[1:]:
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


class SnakeGameGUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_size = 30
        self.grid_color = (50, 50, 50)
        self.snake_head_color = (0, 170, 0)  # Color of the snake's head
        self.snake_body_color = (0, 255, 0)  # Color of the snake's body
        self.screen = pygame.display.set_mode((self.width * self.block_size, self.height * self.block_size))
        pygame.display.set_caption("Snake Game")

    def draw_board(self, board, speed, snake):
        self.screen.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.screen, self.grid_color,
                                 (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 1)
                if board.grid[y][x] == 'O':
                    if (y, x) in snake.head:  # Check if the cell is the snake's head
                        pygame.draw.ellipse(self.screen, self.snake_head_color, (
                            x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2,
                            self.block_size - 2))
                    else:
                        pygame.draw.rect(self.screen, self.snake_body_color, (
                            x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2,
                            self.block_size - 2))
                elif board.grid[y][x] == 'X':
                    pygame.draw.ellipse(self.screen, (255, 0, 0), (
                        x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2, self.block_size - 2))

        font = pygame.font.SysFont(None, 24)
        speed_text = font.render(f"Speed: {speed:.2f} squares per second", True, (125, 125, 125))
        self.screen.blit(speed_text, (10, self.height * self.block_size - 30))

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
            self.gui.draw_board(self.game_logic.board, self.game_logic.speed, self.game_logic.snake)
            clock.tick(self.game_logic.speed)  # Adjust game speed

        print("Game Over!")
        print(f"Score: {len(self.game_logic.snake.body) - 1}")


# Example usage:
# width = int(input("Enter the width of the board: "))
# height = int(input("Enter the height of the board: "))
# player_name = input("Enter your name: ")

pygame.init()
game = SnakeGame(25, 25, "test")
game.run_game()
pygame.quit()
