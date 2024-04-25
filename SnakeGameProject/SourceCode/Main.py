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
                                (element_x_indentation + self.block_size - offset, element_y_indentation + self.block_size - offset)
                            ])
                        elif snake.direction == 'DOWN':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size // 2, element_y_indentation + self.block_size - offset)
                            ])
                        elif snake.direction == 'LEFT':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + self.block_size - offset, element_y_indentation + offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation + self.block_size - offset),
                                (element_x_indentation + offset, element_y_indentation + self.block_size // 2)
                            ])
                        elif snake.direction == 'RIGHT':
                            pygame.draw.polygon(self.screen, self.snake_head_color, [
                                (element_x_indentation + offset, element_y_indentation + offset),
                                (element_x_indentation + offset, element_y_indentation + self.block_size - offset),
                                (element_x_indentation + self.block_size - offset, element_y_indentation + self.block_size // 2)
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
        font = pygame.font.SysFont(None, int(self.frame_width / 2.5))
        speed_text = font.render(f"Speed: {speed:.2f} squares per second", True, self.color_text)
        self.screen.blit(speed_text, (10, self.height * self.block_size + self.frame_width * 1.5))

        # Draw player's name and score
        font_player = pygame.font.SysFont(None, int(self.frame_width / 2.5))
        player_text = font_player.render(f"Player: {player_name}", True, self.color_text)
        self.screen.blit(player_text, (10, 5))

        font_score = pygame.font.SysFont(None, int(self.frame_width / 2))
        score_text = font_score.render(f"Score: {len(snake.body) - 3}", True, self.color_text)
        player_text_height = font_player.size(f"Player: {player_name}")[1]
        self.screen.blit(score_text, (10, player_text_height + self.frame_width // 3))

        pygame.display.update()


class StartWindow:
    def __init__(self):
        pygame.display.set_caption("Welcome to Snake Game")
        screen_info = pygame.display.Info()
        self.width = screen_info.current_w * 2 // 3
        self.height = screen_info.current_h * 2 // 3
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 32)
        self.color_background = (24, 78, 119)
        self.color_inactive = (26, 117, 159)
        self.color_active = (52, 160, 164)
        self.color_nickname_field = self.color_inactive
        self.color_text = (181, 228, 140)
        self.active = None
        self.nickname_text = ''
        self.size_num = '5'
        self.done = False
        self.cursor_visible = False
        self.cursor_timer = 1
        self.color_up_button = self.color_inactive
        self.color_down_button = self.color_inactive
        self.target_input_box_width = 100
        self.input_box = pygame.Rect(self.width // 2 - 100, self.height // 2 - 100, self.target_input_box_width, 32)
        self.size_up_button = pygame.Rect(self.width // 2 + 50, self.height // 2 + 30, 30, 15)
        self.size_down_button = pygame.Rect(self.width // 2 + 50, self.height // 2 + 45, 30, 15)
        self.button = pygame.Rect(self.width // 2 - 75, self.height // 2 + 150, 200, 50)

    def draw_window(self):
        self.screen.fill(self.color_background)  # Background color
        nickname_txt_surface = self.font.render(self.nickname_text, True, self.color_text)
        size_num_txt_surface = self.font.render(self.size_num, True, self.color_text)
        self.screen.blit(nickname_txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.screen.blit(size_num_txt_surface, (self.input_box.x + 5, self.size_up_button.y + 5))
        pygame.draw.rect(self.screen, self.color_nickname_field, self.input_box, 2)

        # Draw the texts
        font = pygame.font.Font(None, 32)
        text = font.render("Enter your nickname:", 1, self.color_text)
        self.screen.blit(text, (self.width // 2 - 100, self.height // 2 - 140))

        font = pygame.font.Font(None, 28)  # Smaller font for the size selection text
        text = font.render("Choose the size of the map:", 1, self.color_text)
        self.screen.blit(text, (self.width // 2 - 100, self.size_up_button.y - 30))

        # Calculate the width of nickname_text
        text_width, _ = self.font.size(self.nickname_text)

        # Adjust the width of input_box1 based on the width of nickname_text
        self.target_input_box_width = max(140, text_width + 20)  # Add 20 for some padding

        # Draw the buttons
        self.draw_button()

        # Draw the cursor
        if self.active == 'box1' and self.cursor_visible:
            pygame.draw.line(self.screen, self.color_active,
                             (self.input_box.x + 10 + self.font.size(self.nickname_text)[0], self.input_box.y + 5),
                             (self.input_box.x + 10 + self.font.size(self.nickname_text)[0],
                              self.input_box.y + self.input_box.h - 5), 2)

        pygame.display.flip()

        if self.active == 'box1' and self.cursor_visible:
            pygame.draw.line(self.screen, self.color_active, (self.input_box.x + 10, self.input_box.y + 5),
                             (self.input_box.x + 10, self.input_box.y + self.input_box.h - 5), 2)

        # Animate the change in width
        if self.input_box.w < self.target_input_box_width:
            self.input_box.w += 1
        elif self.input_box.w > self.target_input_box_width:
            self.input_box.w -= 1

    def draw_button(self):
        font = pygame.font.Font(None, 32)
        text = font.render("Start the game", 1,
                           (217, 237, 146) if self.nickname_text and self.size_num else self.color_background)
        pygame.draw.rect(self.screen, (82, 182, 154) if self.nickname_text and self.size_num else self.color_background, self.button)
        self.screen.blit(text, (self.button.x + 30, self.button.y + 10))

        # Draw size up and down buttons
        pygame.draw.rect(self.screen, self.color_up_button, self.size_up_button)
        pygame.draw.rect(self.screen, self.color_down_button, self.size_down_button)
        font = pygame.font.Font(None, 22)
        text = font.render("+", 1, self.color_text)
        self.screen.blit(text, (self.size_up_button.x + 10, self.size_up_button.y))
        text = font.render("-", 1, self.color_text)
        self.screen.blit(text, (self.size_down_button.x + 12, self.size_down_button.y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = 'box1'
                elif self.size_up_button.collidepoint(event.pos):
                    self.size_num = str(min(25, int(self.size_num) + 1))
                    self.color_up_button = self.color_active
                elif self.size_down_button.collidepoint(event.pos):
                    self.size_num = str(max(5, int(self.size_num) - 1))
                    self.color_down_button = self.color_active
                elif self.button.collidepoint(event.pos) and self.nickname_text and self.size_num:
                    print(self.nickname_text, self.size_num)
                    return self.nickname_text, int(self.size_num)
                else:
                    self.active = None
                self.color_nickname_field = self.color_active if self.active == 'box1' else self.color_inactive
                self.color_up_button = self.color_active if self.size_up_button.collidepoint(
                    event.pos) else self.color_inactive
                self.color_down_button = self.color_active if self.size_down_button.collidepoint(
                    event.pos) else self.color_inactive
            if event.type == pygame.KEYDOWN:
                self.cursor_timer = 0  # Reset the cursor timer
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active == 'box1':
                            self.nickname_text = self.nickname_text[:-1]
                    else:
                        if self.active == 'box1':
                            if len(self.nickname_text) < 15:
                                self.nickname_text += event.unicode
                            else:
                                self.show_error_message("The nickname should not be longer than 15 characters!")
                                self.nickname_text = ''
        self.cursor_timer += 1
        if self.cursor_timer % 300 == 0:
            self.cursor_visible = not self.cursor_visible
        return None, None

    def show_error_message(self, message):
        font = pygame.font.Font(None, 30)
        text = font.render(message, 1, (200, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 50))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before clearing the message


class SnakeGame:
    def __init__(self):
        self.game_logic = None
        self.gui = None
        self.start_window = StartWindow()
        self.player_name, self.size = None, None

    def run_game(self):
        while not self.start_window.done:
            self.start_window.draw_window()
            self.player_name, self.size = self.start_window.handle_events()
            if self.player_name and self.size:
                break

        if self.player_name is None or self.size is None:
            return  # Ending the game if the start window was closed.

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

        print("Game Over!")
        print(f"Score: {len(self.game_logic.snake.body) - 3}")


pygame.init()
game = SnakeGame()
game.run_game()
pygame.quit()
