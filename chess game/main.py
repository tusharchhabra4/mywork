import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Chess AI")
    game = Game(screen)
    game.run() 

if __name__ == "__main__":
    main()
