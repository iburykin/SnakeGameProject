import time
from SourceCode.Snake import Snake
from SourceCode.Board import Board
from SourceCode.mongodb import store_game_result
from SourceCode.mongodb import store_game_result_to_mongodb
import random
class GameLogic:
    def __init__(self, width, height, nickname):
        self.width = width
        self.height = height
        self.nickname = nickname  # Initialize the nickname
        self.score = 0  # Initialize the score to 0
        self.snake = Snake(width // 2, height // 2)
        self.board = Board(width, height)
        self.food = self.generate_food()
        self.obstacles = self.generate_obstacles()  # Generate obstacles
        self.update_board()
        self.speed = 1.0  # Initial speed (1 square per second)
        self.total_cells = self.width * self.height
        self.total_obstacles = sum(len(obstacle) for obstacle in self.obstacles)
        self.winning_condition = self.total_cells - self.total_obstacles
        self.win_bool = False
        self.endgame_text = "Congratulations! You have won the game." if self.win_bool else "Game Over!"
        self.game_over = False

    def get_state(self):
        state = {
            'board': [],
            'nickname': self.nickname,  # Include the nickname in the game state
            'score': self.score,  # Include the score in the game state
            'speed': self.speed,  # Include the speed in the game state
            'game_over': self.game_over,
            'endgame_text': self.endgame_text  # Include the endgame_text in the game state
        }
        for row in self.board.grid:
            state_row = []
            for cell in row:
                if cell == ' ':
                    state_row.append(' ')
                elif cell == 'O':
                    state_row.append('O')
                elif cell == 'X':
                    state_row.append('X')
                elif cell == 'H':
                    state_row.append('H')
            state['board'].append(state_row)
        return state

    def generate_food(self):
        incorrect_position = True
        while incorrect_position:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (y, x) not in self.snake.body and (y, x) not in self.board.obstacles:
                incorrect_position = False
                return y, x

    def generate_obstacles(self):
        obstacle = []
        obstacles = []
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
                incorrect_position = True
                while incorrect_position:
                    # Generate a random position for the obstacle
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    next_move = self.snake.move(self.width, self.height)
                    if ((y, x) not in self.snake.body and (y, x) not in self.board.obstacles and
                            (y, x) != next_move and (y, x) != self.food):
                        incorrect_position = False
                        obstacle = [(y, x)]

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

    def move_snake(self, direction=None):
        if direction:
            self.snake.direction = direction
        new_head = self.snake.move(self.width, self.height)
        if new_head in self.snake.body[1:] or new_head in self.board.obstacles:
            self.game_over = True
            store_game_result(self.nickname, self.score, self.width)
            store_game_result_to_mongodb(self.nickname, self.score, self.width)
            return

        self.snake.body.insert(0, new_head)
        self.snake.head.insert(0, new_head)
        self.snake.head.pop()

        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
            self.speed /= 1.07  # Increase speed by 7%
        else:
            self.snake.body.pop()

        # Check if the player has won the game
        if len(self.snake.body) == self.winning_condition:
            self.win_bool = True
            self.game_over = True
            store_game_result(self.nickname, self.score, (self.width, self.height))
            store_game_result_to_mongodb(self.nickname, self.score, (self.width, self.height))
            print("Congratulations! You have won the game.")

        self.update_board()

    def update_board(self):
        # Clear the board
        self.board.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Place the new state of the snake, food, and obstacles on the board
        self.board.place_snake(self.snake)
        self.board.place_food(self.food)
        for obstacle in self.obstacles:
            self.board.place_obstacles(obstacle)

    def update_game(self):
        while not self.game_over:
            self.move_snake()
            time.sleep(self.speed)
