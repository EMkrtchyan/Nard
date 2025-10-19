# This is a game of long backgammon also called Nard

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
            print("there are unplayed moves")
            return
        else: 
            dice1 = self.roll_dice()
            dice2 = self.roll_dice()
            
            if dice1 == dice2:
                if self.white_turn:
                    self.white_dices=[dice1]*4
                    self.calculate_moves([dice1]) 
                else:
                    self.black_dices=[dice1]*4
                    self.calculate_moves([dice1])  
            else:
                if self.white_turn:
                    self.white_dices=[dice1, dice2]
                    self.calculate_moves(self.white_dices) 
                else:
                    self.black_dices=[dice1, dice2]
                    self.calculate_moves(self.black_dices)  
           
        
        print(self.white_dices)
        print(self.black_dices)
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def is_valid_move(self, from_pos, dice):
        if self.white_turn:
            return self.White[from_pos] > 0 and self.Black[(from_pos + dice)%24] == 0
        else:
            return self.Black[from_pos] > 0 and self.White[(from_pos - dice)%24] == 0
    
    def move_piece(self, from_pos, to_pos, white_turn):
        dice = (to_pos-from_pos)%24
        
        if white_turn and (from_pos,to_pos) in self.wMoves:
            self.White[from_pos]-=1
            self.white_dices.remove(dice)
            if from_pos+dice>=12 and from_pos <12:
                self.white_out+=1
            else:
                self.White[(from_pos+dice)%24]+=1
            if self.white_dices:
                self.calculate_moves(self.white_dices)
                print(f"new moves:{self.wMoves}")
            else:
                self.wMoves = []
                print("no turns for white passing to black")
                white_turn = False
                
        elif not white_turn and (from_pos,to_pos) in self.bMoves:
            self.Black[from_pos]-=1
            self.black_dices.remove(dice)
            if from_pos+dice>=24:
                self.black_out+=1
            else:
                self.Black[(from_pos+dice)]+=1
            if self.black_dices:
                self.calculate_moves(self.black_dices)
                print(f"new moves:{self.bMoves}")
            else:
                self.bMoves = []
                print("no turns for black passing to white")
                self.white_turn = True
            
        else:
            print("Invalid move")
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
                        self.wMoves.append((from_pos,(from_pos+dice)%24))
                    elif (from_pos<12 and from_pos+dice>=12):
                        self.wMoves.append((from_pos,24))
                        
            elif not self.white_turn and dice in self.black_dices:
                from_poss = [i for i, value in enumerate(self.Black) if value != 0]
                if self.is_valid_move(from_pos, dice):
                    self.bMoves.append((from_pos,from_pos+dice))
                elif (from_pos+dice>=24):
                    self.bMoves.append((from_pos,24))

    
    def print_board(self):
        """Print ASCII representation of backgammon board"""
        
        # Find max stack height across all positions
        max_height = 0
        for pos in range(24):
            total = self.Black[pos] + self.White[pos]
            max_height = max(max_height, total)
        
        # Top half (positions 12-23, right to left)
        print("\n┌─────────────────────────────────────────────────┐")
        print("│ 23 22 21 20 19 18 │ BAR │ 17 16 15 14 13 12 │")
        print("├─────────────────────────────────────────────────┤")
        
        # Print top pieces (positions 12-23)
        for row in range(max_height):
            line = "│ "
            # Positions 23 down to 18
            for pos in range(23, 17, -1):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            
            line += "│     │ "
            
            # Positions 17 down to 12
            for pos in range(17, 11, -1):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            line += "│"
            print(line)
        
        # Middle bar
        print("│                   │     │                   │")
        
        # Print bottom pieces (positions 0-11)
        for row in range(max_height - 1, -1, -1):
            line = "│ "
            # Positions 0 to 5
            for pos in range(6):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            
            line += "│     │ "
            
            # Positions 6 to 11
            for pos in range(6, 12):
                if self.Black[pos] > row:
                    line += "●  "
                elif self.White[pos] > row:
                    line += "○  "
                else:
                    line += "   "
            line += "│"
            print(line)
        
        # Bottom half labels
        print("├─────────────────────────────────────────────────┤")
        print("│  0  1  2  3  4  5 │ BAR │  6  7  8  9 10 11 │")
        print("└─────────────────────────────────────────────────┘")
        print(f"\nBlack (●): {sum(self.Black)} pieces")
        print(f"White (○): {sum(self.White)} pieces")
        
board = Board()
board.start_game()
board.print_board()
board.roll_dices()
board.move_piece(12, 16, True)
board.move_piece(16, 22, True)
board.roll_dices()
board.print_board()
print(board.wMoves)