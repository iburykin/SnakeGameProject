class Snake:
    def __init__(self, x, y):
        self.body = [(y, x), (y, x - 1), (y, x - 2)]
        self.head = [(y, x)]
        self.direction = 'RIGHT'

    def move(self, width, height):
        head = self.body[0]
        new_head = head
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