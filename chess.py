import random
import pygame
import sys
from functools import reduce

# Initialize pygame
pygame.init()
selected_piece = None

# Screen dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

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
pygame.display.set_caption("Chess")

def draw_board(screen):
    """Draw the chessboard and pieces."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            piece = board[row][col]
            if piece != ' ':
                # Check if this is the selected piece
                if (row, col) == selected_piece:
                    # Scale the image by 25% for highlighting
                    scaled_size = int(SQUARE_SIZE * 1.25)
                    x = col * SQUARE_SIZE + (SQUARE_SIZE - scaled_size) // 2
                    y = row * SQUARE_SIZE + (SQUARE_SIZE - scaled_size) // 2
                    screen.blit(PIECES[piece], pygame.Rect(x, y, scaled_size, scaled_size))
                else:
                    # Draw the piece normally
                    screen.blit(PIECES[piece], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def is_valid_move(board, start, end):
    piece = board[start[0]][start[1]]
    target_piece = board[end[0]][end[1]]
    
    # Check if the move is within bounds
    if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
        return False
    
    # Check if moving to the same square or capturing own piece
    if (piece.isupper() and target_piece.isupper()) or (piece.islower() and target_piece.islower()):
        return False
    
    # Determine piece type and check movement rules
    if piece.lower() == 'p':  # Pawn
        return is_valid_pawn_move(board, start, end)
    elif piece.lower() == 'n':  # Knight
        return is_valid_knight_move(start, end)
    elif piece.lower() == 'b':  # Bishop
        return is_valid_bishop_move(board, start, end)
    elif piece.lower() == 'r':  # Rook
        return is_valid_rook_move(board, start, end)
    elif piece.lower() == 'q':  # Queen
        return is_valid_queen_move(board, start, end)
    elif piece.lower() == 'k':  # King
        return is_valid_king_move(board, start, end)
    
    return False

def is_valid_pawn_move(board, start, end):
    piece = board[start[0]][start[1]]
    start_row, start_col = start
    end_row, end_col = end

    # Determine pawn color and direction
    if piece.isupper():  # White pawn
        direction = -1
        initial_row = 6
    else:  # Black pawn
        direction = 1
        initial_row = 1

    row_diff = end_row - start_row
    col_diff = abs(end_col - start_col)

    # Check for valid forward moves
    if col_diff == 0:
        # One square forward
        if row_diff == direction and board[end_row][end_col] == ' ':
            return True
        # Two squares forward (only on first move)
        elif row_diff == 2 * direction and start_row == initial_row and all(board[start_row + i * direction][start_col] == ' ' for i in range(1, 3)): 
            return True

    # Check for captures
    if col_diff == 1 and row_diff == direction:
        target_piece = board[end_row][end_col]
        if (piece.isupper() and target_piece.islower()) or (piece.islower() and target_piece.isupper()):
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
    step = 1 if end[0] > start[0] else -1
    for i in range(start[0] + step, end[0], step):
        if board[i][start[1] + ((i - start[0]) * (step if end[1] > start[1] else -step))] != ' ':
            return False
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


def get_legal_moves(board, player):
    legal_moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (player == 'white' and piece.isupper()) or (player == 'black' and piece.islower()):
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(board, (row, col), (end_row, end_col)):
                            legal_moves.append(((row, col), (end_row, end_col)))
    return legal_moves

# Bot move function
def is_in_check(board, king_color):
    """Determine if the king of the given color is under attack."""
    king_position = find_king_position(board, king_color)
    opponent_color = 'black' if king_color == 'white' else 'white'
    if king_position is None:
        return False
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (king_color == 'white' and piece.islower()) or (king_color == 'black' and piece.isupper()):
                if is_valid_move(board, (row, col), king_position):
                    return True
    return False

def find_king_position(board, color):
    """Find the position of the king for the given color."""
    king = 'K' if color == 'white' else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return (row, col)
    return None

def is_checkmate(board, player):
    """Determine if the current player is in checkmate."""
    return is_in_check(board, player) and not has_legal_moves(board, player)

def is_stalemate(board, player):
    """Determine if the current player is in stalemate."""
    return not is_in_check(board, player) and not has_legal_moves(board, player)

def has_legal_moves(board, player):
    """Check if the player has any legal moves."""
    legal_moves = get_legal_moves(board, player)
    return len(legal_moves) > 0

def evaluate_move(board, move):
    """Evaluate a move based on heuristics and return a score."""
    start, end = move
    piece = board[start[0]][start[1]]
    target_piece = board[end[0]][end[1]]
    
    score = 0
    
    # Prioritize capturing higher-value pieces
    if target_piece != ' ':
        if target_piece.lower() == 'q':  # Queen
            score += 9
        elif target_piece.lower() == 'r':  # Rook
            score += 5
        elif target_piece.lower() == 'b' or target_piece.lower() == 'n':  # Bishop or Knight
            score += 3
        elif target_piece.lower() == 'p':  # Pawn
            score += 1
    
    # Prioritize controlling the center (e.g., moves to center squares)
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    if end in center:
        score += 2
    
    # Penalize moving pieces unnecessarily (e.g., non-capturing moves)
    if target_piece == ' ':
        score -= 1
    
    return score

def prioritize_moves(legal_moves, board):
    """Prioritize moves based on their scores and return the top few."""
    scored_moves = [(move, evaluate_move(board, move)) for move in legal_moves]
    sorted_moves = sorted(scored_moves, key=lambda x: x[1], reverse=True)  # Sort by score
    
    # Keep only the top 3 moves (adjust as needed)
    top_moves = [move for move, score in sorted_moves[:3]]
    return top_moves if top_moves else legal_moves  # Fallback to all moves if no top moves

def bot_make_move(board):
    """Bot makes a prioritized move for black pieces."""
    legal_moves = get_legal_moves(board, 'black')
    if not legal_moves:
        return  # No legal moves available (stalemate or checkmate)
    
    prioritized_moves = prioritize_moves(legal_moves, board)
    if not prioritized_moves:
        return  # No prioritized moves available
    
    move = random.choice(prioritized_moves)  # Choose randomly from the top moves
    start, end = move
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = ' '


def print_board(board):
    for row in board:
        print(" ".join([str(cell) if cell != ' ' else '.' for cell in row]))
    print()


def main():
    global board, selected_piece
    board = initial_board
    selected_piece = None
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
                if selected_piece is None:
                    selected_piece = (row, col)  # Highlight the selected piece
                else:
                    end_row, end_col = row, col
                    start_row, start_col = selected_piece
                    if is_valid_move(board, (start_row, start_col), (end_row, end_col)):
                        board[end_row][end_col] = board[start_row][start_col]
                        board[start_row][start_col] = ' '
                        selected_piece = None  # Clear selection after moving
                        
                        # Check for checkmate or stalemate after white's move
                        if is_checkmate(board, 'black'):
                            print("Checkmate! White wins!")
                            return
                        elif is_stalemate(board, 'white'):
                            print("Stalemate! It's a draw.")
                            return
                        player_turn = 'black'  # Switch to black's turn

        if player_turn == 'black':
            bot_make_move(board)
            
            # Check for checkmate or stalemate after black's move
            if is_checkmate(board, 'white'):
                print("Checkmate! Black wins!")
                return
            elif is_stalemate(board, 'black'):
                print("Stalemate! It's a draw.")
                return
            player_turn = 'white'  # Switch back to white's turn

        screen.fill(BLACK)  # Clear the screen
        draw_board(screen)  # Draw the board with highlighted piece
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate

if __name__ == "__main__":
    main()

