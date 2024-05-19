class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.obstacles = []

    def place_snake(self, snake):
        for y, x in snake.body:
            if (y, x) == snake.head[0]:
                self.grid[y][x] = 'H'
            else:
                self.grid[y][x] = 'B'

    def place_food(self, food):
        y, x = food
        self.grid[y][x] = 'F'

    def place_obstacles(self, obstacles):
        for obstacle in obstacles:
            y, x = obstacle
            self.grid[y][x] = 'O'
            self.obstacles.append(obstacle)