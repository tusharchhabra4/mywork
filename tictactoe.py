import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_LINE_COLOR = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw grid lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

def available_moves():
    return [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]

def get_winner():
    for i in range(BOARD_ROWS):
        if all([cell == 'X' for cell in board[i]]):
            return 'X', (0, i), (2, i)
        if all([cell == 'O' for cell in board[i]]):
            return 'O', (0, i), (2, i)
    for col in range(BOARD_COLS):
        if all([board[row][col] == 'X' for row in range(BOARD_ROWS)]):
            return 'X', (col, 0), (col, 2)
        if all([board[row][col] == 'O' for row in range(BOARD_ROWS)]):
            return 'O', (col, 0), (col, 2)
    if all([board[i][i] == 'X' for i in range(BOARD_ROWS)]):
        return 'X', (0, 0), (2, 2)
    if all([board[i][i] == 'O' for i in range(BOARD_ROWS)]):
        return 'O', (0, 0), (2, 2)
    if all([board[i][BOARD_ROWS - i - 1] == 'X' for i in range(BOARD_ROWS)]):
        return 'X', (0, 2), (2, 0)
    if all([board[i][BOARD_ROWS - i - 1] == 'O' for i in range(BOARD_ROWS)]):
        return 'O', (0, 2), (2, 0)
    return None, None, None

def draw_win_line(start, end):
    start_pos = (start[0] * SQUARE_SIZE + SQUARE_SIZE // 2, start[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
    end_pos = (end[0] * SQUARE_SIZE + SQUARE_SIZE // 2, end[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, LINE_WIDTH * 2)

def is_full():
    return all(all(row) for row in board)

def minimax(is_maximizing):
    winner, _, _ = get_winner()
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for (row, col) in available_moves():
            board[row][col] = 'O'
            score = minimax(False)
            board[row][col] = None
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for (row, col) in available_moves():
            board[row][col] = 'X'
            score = minimax(True)
            board[row][col] = None
            best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = None
    for (row, col) in available_moves():
        board[row][col] = 'O'
        score = minimax(False)
        board[row][col] = None
        if score > best_score:
            best_score = score
            move = (row, col)
    return move

def restart():
    global board
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()

def show_popup(message):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(1500)

# Game loop
player_turn = True
running = True
draw_lines()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = 'X'
                winner, start, end = get_winner()
                if winner == 'X':
                    draw_figures()
                    draw_win_line(start, end)
                    pygame.display.update()
                    show_popup("Human wins!")
                    restart()
                elif is_full():
                    draw_figures()
                    pygame.display.update()
                    show_popup("Draw!")
                    restart()
                else:
                    player_turn = False

    if not player_turn:
        move = best_move()
        if move:
            board[move[0]][move[1]] = 'O'
        winner, start, end = get_winner()
        if winner == 'O':
            draw_figures()
            draw_win_line(start, end)
            pygame.display.update()
            show_popup("AI wins!")
            restart()
        elif is_full():
            draw_figures()
            pygame.display.update()
            show_popup("Draw!")
            restart()
        else:
            player_turn = True

    draw_figures()
    pygame.display.update()

pygame.quit()
sys.exit()