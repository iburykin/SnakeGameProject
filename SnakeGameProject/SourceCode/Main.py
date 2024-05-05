# main.py
import pygame
from SnakeGame import SnakeGame

def main():
    pygame.init()
    game = SnakeGame()
    game.run_game()
    pygame.quit()

if __name__ == "__main__":
    main()
