import pygame

TILE = 80
IMAGES = {}

def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        img = pygame.image.load(f"pieces/{piece}.png")
        IMAGES[piece] = pygame.transform.scale(img, (TILE, TILE))

class Board:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP"] * 8,
            ["--"] * 8,
            ["--"] * 8,
            ["--"] * 8,
            ["--"] * 8,
            ["wP"] * 8,
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        load_images()

    def draw(self, screen):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(c*TILE, r*TILE, TILE, TILE))
                piece = self.board[r][c]
                if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(c*TILE, r*TILE, TILE, TILE))

    def get_piece(self, r, c):
        return self.board[r][c] if 0 <= r < 8 and 0 <= c < 8 else None

    def make_move(self, move):
        (sr, sc), (er, ec) = move
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = "--"

    def copy(self):
        from copy import deepcopy
        new_board = Board()
        new_board.board = deepcopy(self.board)
        return new_board

    def get_valid_moves(self, r, c):
        piece = self.board[r][c]
        if piece == "--":
            return []
        color, kind = piece[0], piece[1]
        directions = {
            'P': [(-1, 0), (-1, -1), (-1, 1)] if color == 'w' else [(1, 0), (1, -1), (1, 1)],
            'R': [(0, 1), (1, 0), (0, -1), (-1, 0)],
            'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'Q': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
            'K': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
            'N': [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
        }

        moves = []

        if kind == 'P':
            dir = 1 if color == 'b' else -1
            start_row = 1 if color == 'b' else 6
            # Forward
            if self.get_piece(r + dir, c) == "--":
                moves.append(((r, c), (r + dir, c)))
                if r == start_row and self.get_piece(r + 2*dir, c) == "--":
                    moves.append(((r, c), (r + 2*dir, c)))
            # Captures
            for dc in [-1, 1]:
                if 0 <= r + dir < 8 and 0 <= c + dc < 8:
                    target = self.get_piece(r + dir, c + dc)
                    if target != "--" and target[0] != color: # type: ignore
                        moves.append(((r, c), (r + dir, c + dc)))
        else:
            for dr, dc in directions[kind]:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if not (0 <= nr < 8 and 0 <= nc < 8):
                        break
                    target = self.get_piece(nr, nc)
                    if target == "--":
                        moves.append(((r, c), (nr, nc)))
                        if kind in ["N", "K"]:
                            break
                    elif target[0] != color: # type: ignore
                        moves.append(((r, c), (nr, nc)))
                        break
                    else:
                        break
        return moves

    def get_all_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c].startswith(color):
                    moves.extend(self.get_valid_moves(r, c))
        return moves



