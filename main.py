import pygame
from src.config import CELL_SIZE
from src.game import Game


def main():
    pygame.init()
    game = Game()
    game.loop()


if __name__ == "__main__":
    print(CELL_SIZE)
    main()
