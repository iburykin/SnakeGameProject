from SourceCode.GameLogic import GameLogic

class SnakeGame:
    def __init__(self, size, nickname):
        self.size = size
        self.nickname = nickname
        self.game_logic = GameLogic(self.size, self.size, self.nickname)

    def start_game(self):
        self.game_logic = GameLogic(self.size, self.size, self.nickname)

    def move_snake(self, direction):
        self.game_logic.snake.direction = direction
        self.game_logic.move_snake()

    def get_state(self):
        state = self.game_logic.get_state()
        return state
