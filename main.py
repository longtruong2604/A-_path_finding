import pygame
from src.game import Game


def main():
    pygame.init()
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
