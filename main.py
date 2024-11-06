import pygame
from src.game import Game

header_text = """Keys:
	Left - Lower maximum distance
	Right - Increase maximum distance
	R - create a new maze
        M - change display mode
	Esc - Exit"""


def main():
    pygame.display.init()
    pygame.font.init()
    game = Game()
    print(header_text)
    game.loop()


if __name__ == "__main__":
    main()
