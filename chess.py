import random
import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Color for highlighting possible moves
PINK = (194, 145, 164)

# Chess pieces
PIECES = {
    'P': pygame.image.load('w_pawn.png'),  # White pawn
    'R': pygame.image.load('w_rook.png'),  # White rook
    'N': pygame.image.load('w_knight.png'), # White knight
    'B': pygame.image.load('w_bishop.png'), # White bishop
    'Q': pygame.image.load('w_queen.png'),  # White queen
    'K': pygame.image.load('w_king.png'),   # White king
    'p': pygame.image.load('b_pawn.png'),   # Black pawn
    'r': pygame.image.load('b_rook.png'),   # Black rook
    'n': pygame.image.load('b_knight.png'), # Black knight
    'b': pygame.image.load('b_bishop.png'), # Black bishop
    'q': pygame.image.load('b_queen.png'),  # Black queen
    'k': pygame.image.load('b_king.png')    # Black king
}

# Initial board setup
initial_board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("genChess")

board = initial_board
selected_piece = None
player_turn = 'white'

def draw_board(screen, selected_piece=None):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else PINK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if selected_piece and (row, col) in get_possible_moves_for_piece(board, selected_piece, player_turn):
                highlight_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, YELLOW, highlight_rect, 4)  # Highlight with a border
            
            piece = board[row][col]
            if piece != ' ':
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2 - PIECES[piece].get_width() // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2 - PIECES[piece].get_height() // 2
                if selected_piece == (row, col):
                    x -= 10
                    y -= 10
                    screen.blit(PIECES[piece], (x, y))
                else:
                    screen.blit(PIECES[piece], (x, y))

def is_valid_move(board, start, end, player):
    piece = board[start[0]][start[1]]
    target_piece = board[end[0]][end[1]]
    
    if not (0 <= end[0] < ROWS and 0 <= end[1] < COLS):
        return False
    
    if (player == 'white' and (piece.islower() or (target_piece.isupper() and target_piece != ' '))) or \
       (player == 'black' and (piece.isupper() or (target_piece.islower() and target_piece != ' '))):
        return False
    
    if piece.lower() == 'p':  
        return is_valid_pawn_move(board, start, end, player)
    elif piece.lower() == 'n': 
        return is_valid_knight_move(start, end)
    elif piece.lower() == 'b': 
        return is_valid_bishop_move(board, start, end)
    elif piece.lower() == 'r': 
        return is_valid_rook_move(board, start, end)
    elif piece.lower() == 'q': 
        return is_valid_queen_move(board, start, end)
    elif piece.lower() == 'k': 
        return is_valid_king_move(board, start, end)
    
    return False

def is_valid_pawn_move(board, start, end, player):
    direction = -1 if player == 'white' else 1
    start_row, start_col = start
    end_row, end_col = end

    row_diff = end_row - start_row
    col_diff = abs(end_col - start_col)

    if col_diff == 0:
        if board[end_row][end_col] == ' ':
            if row_diff == direction or (row_diff == 2 * direction and start_row == (6 if player == 'white' else 1)):
                return True
    elif col_diff == 1 and row_diff == direction:
        if board[end_row][end_col] != ' ':
            return True

    return False

def is_valid_knight_move(start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(board, start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    if row_diff != col_diff:
        return False
    step_row = 1 if end[0] > start[0] else -1
    step_col = 1 if end[1] > start[1] else -1
    current_row, current_col = start[0] + step_row, start[1] + step_col
    while (current_row, current_col) != end:
        if board[current_row][current_col] != ' ':
            return False
        current_row += step_row
        current_col += step_col
    return True

def is_valid_rook_move(board, start, end):
    if start[0] != end[0] and start[1] != end[1]:
        return False
    step_row = 0 if start[0] == end[0] else (1 if end[0] > start[0] else -1)
    step_col = 0 if start[1] == end[1] else (1 if end[1] > start[1] else -1)
    current_row, current_col = start[0] + step_row, start[1] + step_col
    while (current_row, current_col) != end:
        if board[current_row][current_col] != ' ':
            return False
        current_row += step_row
        current_col += step_col
    return True

def is_valid_queen_move(board, start, end):
    return is_valid_bishop_move(board, start, end) or is_valid_rook_move(board, start, end)

def is_valid_king_move(board, start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    return row_diff <= 1 and col_diff <= 1

def get_possible_moves_for_piece(board, start, player):
    possible_moves = []
    for end_row in range(ROWS):
        for end_col in range(COLS):
            if is_valid_move(board, start, (end_row, end_col), player):
                possible_moves.append((end_row, end_col))
    return possible_moves

def is_in_check(board, king_color):
    king_position = find_king_position(board, king_color)
    if king_position is None:
        return False
    
    opponent_color = 'black' if king_color == 'white' else 'white'
    
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if (king_color == 'white' and piece.islower()) or (king_color == 'black' and piece.isupper()):
                if is_valid_move(board, (row, col), king_position, opponent_color):
                    return True
    return False

def find_king_position(board, color):
    king = 'K' if color == 'white' else 'k'
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == king:
                return (row, col)
    return None

def is_checkmate(board, player):
    return is_in_check(board, player) and not has_legal_moves(board, player)

def has_legal_moves(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if (player == 'white' and piece.isupper()) or (player == 'black' and piece.islower()):
                for end_row in range(ROWS):
                    for end_col in range(COLS):
                        if is_valid_move(board, (row, col), (end_row, end_col), player):
                            temp_board = [row[:] for row in board]
                            temp_board[end_row][end_col] = temp_board[row][col]
                            temp_board[row][col] = ' '
                            if not is_in_check(temp_board, player):
                                return True
    return False

def evaluate_move(board, move):
    start, end = move
    piece = board[start[0]][start[1]]
    target_piece = board[end[0]][end[1]]
    
    score = 0
    
    if target_piece != ' ':
        if target_piece.lower() == 'q':  
            score += 9
        elif target_piece.lower() == 'r': 
            score += 5
        elif target_piece.lower() == 'b' or target_piece.lower() == 'n': 
            score += 3
        elif target_piece.lower() == 'p': 
            score += 1
    
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    if end in center:
        score += 2
    
    if target_piece == ' ':
        score -= 1
    
    return score

def prioritize_moves(legal_moves, board):
    scored_moves = [(move, evaluate_move(board, move)) for move in legal_moves]
    sorted_moves = sorted(scored_moves, key=lambda x: x[1], reverse=True)  
    top_moves = [move for move, score in sorted_moves[:3]]
    return top_moves if top_moves else legal_moves  

def bot_make_move(board):
    legal_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece.islower():  # Black pieces
                for end_row in range(ROWS):
                    for end_col in range(COLS):
                        if is_valid_move(board, (row, col), (end_row, end_col), 'black'):
                            temp_board = [r[:] for r in board]
                            temp_board[end_row][end_col] = temp_board[row][col]
                            temp_board[row][col] = ' '
                            if not is_in_check(temp_board, 'black'):
                                legal_moves.append(((row, col), (end_row, end_col)))
    
    if not legal_moves:
        return  
    prioritized_moves = prioritize_moves(legal_moves, board)
    if not prioritized_moves:
        return  

    move = random.choice(prioritized_moves)
    #move = random.choice(legal_moves)
    start, end = move
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = ' '
    
def check_pawn_promotion(board):
    """Check for pawns that need to be promoted."""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == 'P' and row == 0:  # White pawn reaches last rank
                print(f"White pawn detected at ({row}, {col}) for promotion")  # Debug print
                promote_pawn(board, row, col)
                print(f"After promotion, piece at ({row}, {col}) is: {board[row][col]}")  # Debug print
            elif piece == 'p' and row == 7:  # Black pawn reaches first rank
                print(f"Black pawn detected at ({row}, {col}) for promotion")  # Debug print
                promote_pawn(board, row, col)
                print(f"After promotion, piece at ({row}, {col}) is: {board[row][col]}")  # Debug print

def promote_pawn(board, row, col):
    """Promote a pawn to a queen at the given position."""
    if board[row][col].lower() == 'p':
        original_piece = board[row][col]
        if original_piece.isupper():  # White pawn
            board[row][col] = 'Q'  # Promote to queen
            print(f"Promoted white pawn at ({row}, {col}) to Queen")  # Debug print
        else:  # Black pawn
            board[row][col] = 'q'
            print(f"Promoted black pawn at ({row}, {col}) to Queen")  # Debug print
    else:
        print(f"Piece at ({row}, {col}) is not a pawn: {board[row][col]}")  # Debug print



def main():
    global board, selected_piece
    board = initial_board
    selected_piece = None  # No piece selected initially
    player_turn = 'white'  # Start with white's turn

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn == 'white':
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                
                if selected_piece is not None and selected_piece == (row, col):
                    selected_piece = None
                elif selected_piece is None:
                    piece = board[row][col]
                    if (player_turn == 'white' and piece.isupper()) or (player_turn == 'black' and piece.islower()):
                        selected_piece = (row, col)
                else:
                    start_row, start_col = selected_piece
                    end_row, end_col = row, col
                    if is_valid_move(board, (start_row, start_col), (end_row, end_col), player_turn):
                        temp_board = [r[:] for r in board]
                        temp_board[end_row][end_col] = temp_board[start_row][start_col]
                        temp_board[start_row][start_col] = ' '
                        check_pawn_promotion(board)
                        if not is_in_check(temp_board, player_turn):
                            board[end_row][end_col] = board[start_row][start_col]
                            board[start_row][start_col] = ' '
                            selected_piece = None
                            player_turn = 'black'

        if player_turn == 'black':
            bot_make_move(board)
            check_pawn_promotion(board)
            player_turn = 'white'

        if is_checkmate(board, 'white'):
            print("Checkmate! Black wins!")
            break
        elif is_checkmate(board, 'black'):
            print("Checkmate! White wins!")
            break

        screen.fill(BLACK)
        draw_board(screen, selected_piece)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

