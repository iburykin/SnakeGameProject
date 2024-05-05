import pygame
class EndGameWindow:
    def __init__(self, width, height, game_result):
        pygame.display.set_caption("Game Over")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('end_game_window', 32)
        self.color_background = (24, 78, 119)
        self.color_inactive = (26, 117, 159)
        self.color_active = (52, 160, 164)
        self.color_text = (181, 228, 140)
        self.game_result = game_result
        self.save_exit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 50, 200, 50)
        self.play_again_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 110, 200, 50)
        self.done = False

    def draw_window(self):
        self.screen.fill(self.color_background)  # Background color

        # Draw the game result message
        font = pygame.font.Font(None, 32)
        text = font.render(self.game_result, 1, self.color_text)
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 100))

        # Draw the buttons
        self.draw_button("Save the game and exit", self.save_exit_button)
        self.draw_button("Play again", self.play_again_button)

        pygame.display.flip()

    def draw_button(self, message, button):
        font = pygame.font.Font(None, 32)
        text = font.render(message, 1, self.color_text)
        pygame.draw.rect(self.screen, self.color_active, button)
        self.screen.blit(text, (button.x + 30, button.y + 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.save_exit_button.collidepoint(event.pos):
                    print("Save the game and exit")
                    return "save_exit"
                elif self.play_again_button.collidepoint(event.pos):
                    print("Play again")
                    return "play_again"
        return None