import copy
import sys
import random
import itertools

# Constants for the players
PLAYER_L1 = 'L1'
PLAYER_L2 = 'L2'
NEUTRAL_PIECE_1 = 'N1'
NEUTRAL_PIECE_2 = 'N2'

# Initialize the board
def initialize_board():
    """Initialize the board with the starting pieces."""
    grid = [
        ['N1', 'L1', 'L1', '.'],
        ['.', 'L2', 'L1', '.'],
        ['.', 'L2', 'L1', '.'],
        ['.', 'L2', 'L2', 'N2']
    ]
    return grid

# Print the current board state
def print_board(grid):
    """Print the current board state."""
    for row in grid:
        print(" ".join(row))

# Find all positions of a given piece on the board
def find_positions(grid, piece):
    """Find all positions of the given piece on the board."""
    positions = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == piece:
                positions.append((r, c))
    return positions

# Generate legal moves for the player's L piece
def generate_legal_moves(grid, player):
    """Generate all legal moves for the player's L piece."""
    legal_moves = []
    l_piece = PLAYER_L1 if player == PLAYER_L1 else PLAYER_L2
    positions = find_positions(grid, l_piece)
    
    for (r, c) in positions:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_r, new_c = r + dr, c + dc
                if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and grid[new_r][new_c] == '.':
                    legal_moves.append((new_r, new_c))
    return legal_moves

# Check if the game is over
def game_over(grid):
    """Check if the game is over (the opponent has no legal moves)."""
    l1_moves = generate_legal_moves(grid, PLAYER_L1)
    l2_moves = generate_legal_moves(grid, PLAYER_L2)
    
    if not l1_moves:
        print("L2 wins! L1 has no moves left.")
        return True
    elif not l2_moves:
        print("L1 wins! L2 has no moves left.")
        return True
    
    return False

# Apply a move to the grid
def apply_move(grid, move, player):
    """Apply a move to the grid and return the new grid."""
    l_piece = 'L1' if player == PLAYER_L1 else 'L2'
    old_row, old_col = move[0], move[1]
    new_row, new_col = move[2], move[3]
    
    # Update the grid with the new positions
    grid[old_row][old_col] = '.'
    grid[new_row][new_col] = l_piece
    return grid

# Heuristic evaluation function
def heuristic_evaluation(grid):
    """Evaluate the board state for minimax."""
    score = 0
    for row in grid:
        for cell in row:
            if cell == 'L1':
                score += 1  # L1 gets a positive score
            elif cell == 'L2':
                score -= 1  # L2 gets a negative score
    return score

# Minimax with Alpha-Beta Pruning
def minimax(grid, depth, maximizing_player, alpha, beta):
    """Run the minimax algorithm with alpha-beta pruning."""
    if depth == 0 or game_over(grid):
        return heuristic_evaluation(grid)
    
    if maximizing_player:
        max_eval = float('-inf')
        legal_moves = generate_legal_moves(grid, PLAYER_L1)  # L1 moves
        for move in legal_moves:
            new_grid = copy.deepcopy(grid)
            new_grid = apply_move(new_grid, (move[0], move[1], move[2], move[3]), PLAYER_L1)
            eval = minimax(new_grid, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Prune the branch
        return max_eval
    else:
        min_eval = float('inf')
        legal_moves = generate_legal_moves(grid, PLAYER_L2)  # L2 moves
        for move in legal_moves:
            new_grid = copy.deepcopy(grid)
            new_grid = apply_move(new_grid, (move[0], move[1], move[2], move[3]), PLAYER_L2)
            eval = minimax(new_grid, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Prune the branch
        return min_eval

# AI Move (based on minimax)
def ai_move(grid):
    """Make the best move for the AI (L1) using minimax."""
    best_move = None
    best_value = float('-inf')
    legal_moves = generate_legal_moves(grid, PLAYER_L1)  # L1 moves for the AI
    for move in legal_moves:
        new_grid = copy.deepcopy(grid)
        new_grid = apply_move(new_grid, (move[0], move[1], move[2], move[3]), PLAYER_L1)
        move_value = minimax(new_grid, depth=3, maximizing_player=False, alpha=float('-inf'), beta=float('inf'))
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

# Play the game
def play_game():
    """Main function to play the L game."""
    grid = initialize_board()
    print("Initial Board:")
    print_board(grid)
    
    mode = input("Choose mode: (1) Human vs Human (2) Human vs AI (3) AI vs AI): ").strip()
    
    while not game_over(grid):
        print("\n--- New Turn ---")
        print_board(grid)
        
        if mode == '1':  # Human vs Human
            grid = move_L_piece(grid, PLAYER_L1)
            if game_over(grid): break
            grid = move_neutral_piece(grid, PLAYER_L1)
            if game_over(grid): break
            grid = move_L_piece(grid, PLAYER_L2)
            if game_over(grid): break
            grid = move_neutral_piece(grid, PLAYER_L2)
        
        elif mode == '2':  # Human vs AI
            grid = move_L_piece(grid, PLAYER_L1)  # Human's move
            if game_over(grid): break
            print("\nAI's Turn:")
            ai_move_choice = ai_move(grid)  # AI chooses a move
            if ai_move_choice is None:  # AI cannot move, game ends
                print("AI has no moves left.")
                break
            grid = apply_move(grid, ai_move_choice, PLAYER_L2)  # AI's move
            if game_over(grid): break
        
        elif mode == '3':  # AI vs AI
            ai_move_choice_1 = ai_move(grid)
            grid = apply_move(grid, ai_move_choice_1, PLAYER_L1)
            if game_over(grid): break
            ai_move_choice_2 = ai_move(grid)
            grid = apply_move(grid, ai_move_choice_2, PLAYER_L2)
    
    print("Game Over!")

if __name__ == "__main__":
    play_game()
