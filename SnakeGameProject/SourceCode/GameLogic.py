from Snake import Snake
from Board import Board
import random
class GameLogic:
    #  TODO: Implement the winning logic
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
                incorrect_position = True
                while incorrect_position:
                    # Generate a random position for the obstacle
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    next_move = self.snake.move(self.width, self.height)
                    if (y, x) not in self.snake.body and (y, x) not in self.board.obstacles and (y, x) != next_move:
                        incorrect_position = False
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