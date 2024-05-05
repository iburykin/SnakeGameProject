import pygame
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


# TODO: Implement the end game screen with the score, the option to play again and with ability to save the game.

