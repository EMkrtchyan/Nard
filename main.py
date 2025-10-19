import random
import copy

class Board:
    def __init__(self):
        self.Black = [0] * 24
        self.White = [0] * 24
        self.white_dices = []
        self.black_dices = []
        self.wMoves = []
        self.bMoves = []
        self.white_out = 0
        self.black_out = 0
        self.game_over = False
        self.white_turn = True
        self.head_moved = False
        
    def start_game(self):
        self.Black[0] = 15
        self.White[12] = 15
        
    def roll_dices(self):
        self.head_moved = False
        if self.wMoves or self.bMoves:
            print("There are unplayed moves")
            return False
        
        dice1 = self.roll_dice()
        dice2 = self.roll_dice()
        
        if dice1 == dice2:
            if self.white_turn:
                self.white_dices = [dice1] * 4
                self.calculate_moves([dice1]) 
            else:
                self.black_dices = [dice1] * 4
                self.calculate_moves([dice1])  
        else:
            if self.white_turn:
                self.white_dices = [dice1, dice2]
                self.calculate_moves(self.white_dices) 
            else:
                self.black_dices = [dice1, dice2]
                self.calculate_moves(self.black_dices)
        
        current_player = "White" if self.white_turn else "Black"
        current_dices = self.white_dices if self.white_turn else self.black_dices
        print(f"\n{current_player} rolled: {current_dices}")
        return True
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def is_valid_move(self, from_pos, dice):
        if self.white_turn:
            if self.head_moved and from_pos==12:
                return False
            
            return self.White[from_pos] > 0 and self.Black[(from_pos + dice) % 24] == 0
        else:
            if self.head_moved and from_pos==0:
                return False
            return self.Black[from_pos] > 0 and self.White[(from_pos + dice) % 24] == 0
    
    def move_piece(self, from_pos, to_pos):
        if to_pos == 24:
            # Moving out - find the dice that enables this move
            if self.white_turn:
                dice = None
                for d in self.white_dices:
                    if from_pos + d >= 12 and from_pos < 12:
                        dice = d
                        break
                if dice is None:
                    print("Invalid move!")
                    return False
            else:
                dice = None
                for d in self.black_dices:
                    if from_pos + d >= 24:
                        dice = d
                        break
                if dice is None:
                    print("Invalid move!")
                    return False
        else:
            dice = (to_pos - from_pos) % 24
        
        if self.white_turn and (from_pos, to_pos) in self.wMoves:
            self.White[from_pos] -= 1
            self.white_dices.remove(dice)
            if from_pos == 12:
                self.head_moved = True
            if to_pos == 24:
                self.white_out += 1
                print(f"White piece moved out!")
            else:
                self.White[to_pos] += 1
            
            if self.white_dices:
                self.calculate_moves(set(self.white_dices))
            else:
                self.wMoves = []
                print("\nWhite has no more moves. Passing to Black.")
                self.white_turn = False
                
        elif not self.white_turn and (from_pos, to_pos) in self.bMoves:
            self.Black[from_pos] -= 1
            self.black_dices.remove(dice)
            if from_pos == 0:
                self.head_moved = True
            if to_pos == 24:
                self.black_out += 1
                print(f"Black piece moved out!")
            else:
                self.Black[to_pos] += 1
            
            if self.black_dices:
                self.calculate_moves(set(self.black_dices))
            else:
                self.bMoves = []
                print("\nBlack has no more moves. Passing to White.")
                self.white_turn = True
        else:
            print("Invalid move!")
            return False
        
        return True
    
    def can_bear_off(self, is_white):
        """Check if player can bear off pieces (all pieces in home quadrant)"""
        if is_white:
            # White home quadrant is 6-11
            for i in range(24):
                if i < 6 or i >= 12:
                    if self.White[i] > 0:
                        return False
            return True
        else:
            # Black home quadrant is 18-23
            for i in range(18):
                if self.Black[i] > 0:
                    return False
            return True
    
    def calculate_moves(self, dices):
        self.wMoves = []
        self.bMoves = []
        for dice in dices:
            if self.white_turn and dice in self.white_dices:
                from_poss = [i for i, value in enumerate(self.White) if value != 0]
                can_bear_off_white = self.can_bear_off(True)
                
                for from_pos in from_poss:
                    to_pos = (from_pos + dice) % 24
                    if self.is_valid_move(from_pos, dice):
                        # Check if this move would go past the board
                        if can_bear_off_white and from_pos >= 6 and from_pos < 12 and from_pos + dice >= 12:
                            self.wMoves.append((from_pos, 24))  # Bear off
                        else:
                            self.wMoves.append((from_pos, to_pos))  # Regular move
                    elif can_bear_off_white and from_pos >= 6 and from_pos < 12:
                        # If in home quadrant but blocked, still allow bearing off if exceeds board
                        if from_pos + dice >= 12:
                            self.wMoves.append((from_pos, 24))
                        
            elif not self.white_turn and dice in self.black_dices:
                from_poss = [i for i, value in enumerate(self.Black) if value != 0]
                can_bear_off_black = self.can_bear_off(False)
                
                for from_pos in from_poss:
                    to_pos = from_pos + dice
                    if to_pos < 24 and self.is_valid_move(from_pos, dice):
                        self.bMoves.append((from_pos, to_pos))  # Regular move
                    elif can_bear_off_black and from_pos >= 18 and from_pos < 24:
                        # If in home quadrant and move exceeds board, bear off
                        if to_pos >= 24:
                            self.bMoves.append((from_pos, 24))
    
    def print_board(self):
        """Print ASCII representation of backgammon board"""
        max_height = 0
        for pos in range(24):
            total = self.Black[pos] + self.White[pos]
            max_height = max(max_height, total)
        
        print("\n┌─────────────────────────────────────────────────┐")
        print("│ 23 22 21 20 19 18 │ BAR │ 17 16 15 14 13 12 │")
        print("├─────────────────────────────────────────────────┤")
        
        for row in range(max_height):
            line = "│ "
            for pos in range(23, 17, -1):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            
            line += "│     │ "
            
            for pos in range(17, 11, -1):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            line += "│"
            print(line)
        
        print("│                   │     │                   │")
        
        for row in range(max_height - 1, -1, -1):
            line = "│ "
            for pos in range(6):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            
            line += "│     │ "
            
            for pos in range(6, 12):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            line += "│"
            print(line)
        
        print("├─────────────────────────────────────────────────┤")
        print("│  0  1  2  3  4  5 │ BAR │  6  7  8  9 10 11 │")
        print("└─────────────────────────────────────────────────┘")
        print(f"\nBlack (●): {sum(self.Black)} on board | {self.black_out} out")
        print(f"White (○): {sum(self.White)} on board | {self.white_out} out")
    
    def show_available_moves(self):
        current_player = "White" if self.white_turn else "Black"
        moves = self.wMoves if self.white_turn else self.bMoves
        
        if moves:
            print(f"\nAvailable moves for {current_player}:")
            for i, (from_pos, to_pos) in enumerate(moves, 1):
                if to_pos == 24:
                    print(f"{i}. From position {from_pos} to OUT")
                else:
                    print(f"{i}. From position {from_pos} to {to_pos}")
        else:
            print(f"\nNo available moves for {current_player}")
            self.white_turn = not self.white_turn


class MinimaxAI:
    def __init__(self, is_white, depth=3):
        self.is_white = is_white
        self.depth = depth
    
    def evaluate_board(self, board):
        """
        Evaluation function for board state.
        Positive values favor White, negative favor Black.
        """
        # Win/loss conditions
        if board.white_out == 15:
            return 10000
        if board.black_out == 15:
            return -10000
        
        score = 0
        
        # Pieces that have exited the board (most important)
        score += board.white_out * 100
        score -= board.black_out * 100
        
        # Progress towards exit (weighted by position)
        for i in range(24):
            if board.White[i] > 0:
                # For White: closer to 0-11 range is better (wrapping around)
                if i < 12:
                    progress = 12 - i
                else:
                    progress = 24 - i + 12
                score += board.White[i] * progress * 5
            
            if board.Black[i] > 0:
                # For Black: higher positions are better
                progress = i
                score -= board.Black[i] * progress * 5
        
        # Blockades (controlling positions)
        for i in range(24):
            if board.White[i] > 0 and board.Black[i] == 0:
                score += 2
            if board.Black[i] > 0 and board.White[i] == 0:
                score -= 2
        
        # Spread pieces (avoid clustering)
        white_positions = [i for i in range(24) if board.White[i] > 0]
        black_positions = [i for i in range(24) if board.Black[i] > 0]
        score += len(white_positions) * 1
        score -= len(black_positions) * 1
        
        return score
    
    def get_best_move(self, board):
        """Find the best move using minimax with alpha-beta pruning"""
        moves = board.wMoves if self.is_white else board.bMoves
        
        if not moves:
            return None
        
        best_move = None
        best_value = float('-inf') if self.is_white else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in moves:
            # Simulate move
            sim_board = self.simulate_move(board, move)
            
            # Evaluate the position after this move
            value = self.minimax(sim_board, self.depth - 1, alpha, beta, not self.is_white)
            
            # Update best move
            if self.is_white:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
        
        return best_move
    
    def minimax(self, board, depth, alpha, beta, maximizing_white):
        """Minimax algorithm with alpha-beta pruning"""
        # Terminal conditions
        if depth == 0 or board.white_out == 15 or board.black_out == 15:
            return self.evaluate_board(board)
        
        moves = board.wMoves if maximizing_white else board.bMoves
        
        # No moves available
        if not moves:
            return self.evaluate_board(board)
        
        if maximizing_white:
            max_eval = float('-inf')
            for move in moves:
                sim_board = self.simulate_move(board, move)
                eval = self.minimax(sim_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                sim_board = self.simulate_move(board, move)
                eval = self.minimax(sim_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def simulate_move(self, board, move):
        """Create a copy of the board and apply the move"""
        sim_board = copy.deepcopy(board)
        from_pos, to_pos = move
        
        if sim_board.white_turn:
            if to_pos == 24:
                # Moving out - find the dice that enables this move
                dice = None
                for d in sim_board.white_dices:
                    if from_pos + d >= 12 and from_pos < 12:
                        dice = d
                        break
            else:
                dice = (to_pos - from_pos) % 24
            
            if dice and dice in sim_board.white_dices:
                sim_board.White[from_pos] -= 1
                sim_board.white_dices.remove(dice)
                
                if from_pos == 12:
                    sim_board.head_moved = True
                
                if to_pos == 24:
                    sim_board.white_out += 1
                else:
                    sim_board.White[to_pos] += 1
                
                # Recalculate moves if dices remain
                if sim_board.white_dices:
                    sim_board.calculate_moves(set(sim_board.white_dices))
                else:
                    sim_board.wMoves = []
                    sim_board.white_turn = False
        else:
            if to_pos == 24:
                # Moving out - find the dice that enables this move
                dice = None
                for d in sim_board.black_dices:
                    if from_pos + d >= 24:
                        dice = d
                        break
            else:
                dice = (to_pos - from_pos) % 24
            
            if dice and dice in sim_board.black_dices:
                sim_board.Black[from_pos] -= 1
                sim_board.black_dices.remove(dice)
                
                if from_pos == 0:
                    sim_board.head_moved = True
                
                if to_pos == 24:
                    sim_board.black_out += 1
                else:
                    sim_board.Black[to_pos] += 1
                
                # Recalculate moves if dices remain
                if sim_board.black_dices:
                    sim_board.calculate_moves(set(sim_board.black_dices))
                else:
                    sim_board.bMoves = []
                    sim_board.white_turn = True
        
        return sim_board


def main():
    board = Board()
    board.start_game()
    
    print("=" * 50)
    print("Welcome to Long Backgammon (Nard) with AI!")
    print("=" * 50)
    print("\nWhite (○) starts at position 12")
    print("Black (●) starts at position 0")
    print("\nGame Modes:")
    print("  1. Human vs Human")
    print("  2. Human (White) vs AI (Black)")
    print("  3. AI (White) vs Human (Black)")
    print("  4. AI vs AI")
    
    mode = input("\nSelect mode (1-4): ").strip()
    
    white_ai = None
    black_ai = None
    
    if mode == "2":
        black_ai = MinimaxAI(is_white=False, depth=3)
    elif mode == "3":
        white_ai = MinimaxAI(is_white=True, depth=3)
    elif mode == "4":
        white_ai = MinimaxAI(is_white=True, depth=3)
        black_ai = MinimaxAI(is_white=False, depth=3)
    
    print("\nCommands:")
    print("  'roll' - Roll the dice")
    print("  'move <from> <to>' - Move a piece (e.g., 'move 12 16')")
    print("  'moves' - Show available moves")
    print("  'board' - Show the board")
    print("  'quit' - Exit the game")
    
    board.print_board()
    
    while not board.game_over:
        current_player = "White" if board.white_turn else "Black"
        current_ai = white_ai if board.white_turn else black_ai
        
        print(f"\n--- {current_player}'s turn ---")
        
        # AI turn
        if current_ai:
            if not board.wMoves and not board.bMoves:
                print(f"{current_player} (AI) is rolling...")
                board.roll_dices()
                board.show_available_moves()
            
            if board.wMoves or board.bMoves:
                print(f"{current_player} (AI) is thinking...")
                best_move = current_ai.get_best_move(board)
                
                if best_move:
                    from_pos, to_pos = best_move
                    if to_pos == 24:
                        print(f"{current_player} (AI) moves from {from_pos} to OUT")
                    else:
                        print(f"{current_player} (AI) moves from {from_pos} to {to_pos}")
                    board.move_piece(from_pos, to_pos)
                    board.print_board()
                    
                    if board.wMoves or board.bMoves:
                        board.show_available_moves()
        else:
            # Human turn
            command = input(f"{current_player}> ").strip().lower()
            
            if command == 'quit':
                print("Thanks for playing!")
                break
            
            elif command == 'roll':
                board.roll_dices()
                board.show_available_moves()
            
            elif command == 'board':
                board.print_board()
            
            elif command == 'moves':
                board.show_available_moves()
            
            elif command.startswith('move'):
                parts = command.split()
                if len(parts) == 3:
                    try:
                        from_pos = int(parts[1])
                        to_pos = int(parts[2])
                        if board.move_piece(from_pos, to_pos):
                            board.print_board()
                            if board.wMoves or board.bMoves:
                                board.show_available_moves()
                    except ValueError:
                        print("Invalid input! Use: move <from> <to>")
                else:
                    print("Invalid command! Use: move <from> <to>")
            
            else:
                print("Unknown command! Type 'roll', 'move <from> <to>', 'moves', 'board', or 'quit'")
        
        # Check win condition
        if board.white_out == 15:
            print("\n🎉 White wins!")
            board.game_over = True
        elif board.black_out == 15:
            print("\n🎉 Black wins!")
            board.game_over = True

if __name__ == "__main__":
    main()