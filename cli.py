import random

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
        
    def start_game(self):
        self.Black[0] = 15
        self.White[12] = 15
        
    def roll_dices(self):
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
            return self.White[from_pos] > 0 and self.Black[(from_pos + dice) % 24] == 0
        else:
            return self.Black[from_pos] > 0 and self.White[(from_pos - dice) % 24] == 0
    
    def move_piece(self, from_pos, to_pos):
        dice = (to_pos - from_pos) % 24
        
        if self.white_turn and (from_pos, to_pos) in self.wMoves:
            self.White[from_pos] -= 1
            self.white_dices.remove(dice)
            if from_pos + dice >= 12 and from_pos < 12:
                self.white_out += 1
                print(f"White piece moved out!")
            else:
                self.White[(from_pos + dice) % 24] += 1
            
            if self.white_dices:
                self.calculate_moves(set(self.white_dices))
            else:
                self.wMoves = []
                print("\nWhite has no more moves. Passing to Black.")
                self.white_turn = False
                
        elif not self.white_turn and (from_pos, to_pos) in self.bMoves:
            self.Black[from_pos] -= 1
            self.black_dices.remove(dice)
            if from_pos + dice >= 24:
                self.black_out += 1
                print(f"Black piece moved out!")
            else:
                self.Black[from_pos + dice] += 1
            
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
    
    def calculate_moves(self, dices):
        self.wMoves = []
        self.bMoves = []
        for dice in dices:
            if self.white_turn and dice in self.white_dices:
                from_poss = [i for i, value in enumerate(self.White) if value != 0]
                for from_pos in from_poss:
                    if self.is_valid_move(from_pos, dice):
                        self.wMoves.append((from_pos, (from_pos + dice) % 24))
                    elif (from_pos < 12 and from_pos + dice >= 12):
                        self.wMoves.append((from_pos, 24))
                        
            elif not self.white_turn and dice in self.black_dices:
                from_poss = [i for i, value in enumerate(self.Black) if value != 0]
                for from_pos in from_poss:
                    if self.is_valid_move(from_pos, dice):
                        self.bMoves.append((from_pos, from_pos + dice))
                    elif (from_pos + dice >= 24):
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

def main():
    board = Board()
    board.start_game()
    
    print("=" * 50)
    print("Welcome to Long Backgammon (Nard)!")
    print("=" * 50)
    print("\nWhite (○) starts at position 12")
    print("Black (●) starts at position 0")
    print("\nCommands:")
    print("  'roll' - Roll the dice")
    print("  'move <from> <to>' - Move a piece (e.g., 'move 12 16')")
    print("  'moves' - Show available moves")
    print("  'board' - Show the board")
    print("  'quit' - Exit the game")
    
    board.print_board()
    
    while not board.game_over:
        current_player = "White" if board.white_turn else "Black"
        print(f"\n--- {current_player}'s turn ---")
        
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