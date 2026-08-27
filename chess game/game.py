import pygame
from board import Board
from ai import find_best_move

class Game:
    def __init__(self, screen):
        self.board = Board()
        self.screen = screen
        self.selected = None
        self.valid_moves = []
        self.turn = 'w'
        self.running = True
        
    def check_game_over(self):
        kings = sum(row.count("wK") for row in self.board.board), sum(row.count("bK") for row in self.board.board)
        return kings[0] == 0 or kings[1] == 0
  
    def show_winner(self, font):
        if any("wK" in row for row in self.board.board):
         winner = "White Wins!" if not any("bK" in row for row in self.board.board) else None
        else:
         winner = "Black Wins!" if not any("wK" in row for row in self.board.board) else None

        if winner:
         overlay = pygame.Surface((640, 640))
         overlay.set_alpha(180)
         overlay.fill((0, 0, 0))
         self.screen.blit(overlay, (0, 0))
         text = font.render(winner, True, (255, 255, 255))
         self.screen.blit(text, text.get_rect(center=(320, 320)))
          
    def run(self):
      clock = pygame.time.Clock()
      font = pygame.font.SysFont("Arial", 36)
      while self.running:
        if self.check_game_over():
            self.board.draw(self.screen)
            pygame.display.flip()
            
            self.show_winner(font)
            pygame.time.wait(4000)
            self.running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.turn == 'w':
                x, y = pygame.mouse.get_pos()
                self.handle_click(y // 80, x // 80)

        if self.turn == 'b' and not self.check_game_over():
            move = find_best_move(self.board, 'b')
            if move:
                self.board.make_move(move)
                self.turn = 'w'

        self.board.draw(self.screen)
        pygame.display.flip()
        clock.tick(60)

    def handle_click(self, row, col):
        if self.selected:
            move = (self.selected, (row, col))
            if move in self.valid_moves:
                self.board.make_move(move)
                self.turn = 'b'
            self.selected = None
            self.valid_moves = []
        else:
            piece = self.board.get_piece(row, col)
            if piece and piece[0] == self.turn:
                self.selected = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)

    def show_winner_popup(self, winner):
       font = pygame.font.SysFont("Arial", 48)
       text = font.render(f"{winner} Wins!", True, pygame.Color("red"))
       rect = text.get_rect(center=(320, 320))
       pygame.draw.rect(self.screen, pygame.Color("white"), rect.inflate(20, 20))
       self.screen.blit(text, rect)
       pygame.display.flip()
       if winner:
        self.show_winner_popup(winner)
       pygame.time.wait(3000)
       self.running = False

def check_winner(self):
    kings = {"w": False, "b": False}
    for row in self.board:
        for piece in row:
            if piece == "wK":
                kings["w"] = True
            elif piece == "bK":
                kings["b"] = True

    if not kings["w"]:
        return "Black"
    elif not kings["b"]:
        return "White"
    else:
        return None

    


