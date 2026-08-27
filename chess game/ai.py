def evaluate(board):
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000}
    score = 0
    for row in board.board:
        for piece in row:
            if piece != "--":
                val = values[piece[1]]
                score += val if piece[0] == 'b' else -val
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate(board), None

    color = 'b' if maximizing else 'w'
    best_move = None
    moves = board.get_all_moves(color)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = board.copy()
            new_board.make_move(move)
            eval, _ = minimax(new_board, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = board.copy()
            new_board.make_move(move)
            eval, _ = minimax(new_board, depth-1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def find_best_move(board, color):
    _, move = minimax(board, 2, float('-inf'), float('inf'), color == 'b')
    return move
