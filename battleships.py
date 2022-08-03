#  LEGEND: 
#  S - SHIP 
#  X - HIT 
#  . - WATER 
#  # - MISS 

import random
import time 

VALID_COORDINATES = [1,2,3,4,5,6]
VALID_ORIENTATION = ['V','H']
NUMBER_OF_SHIPS = 5
SHIP_LENGTHS = [3,2,2,1,1,1,1]

class Board: 

    def __init__(self, board):
        self.board = board

    def print_board(self):
        print('')
        coord_ui_top = [' ', 1, 2, 3, 4, 5, 6]
        print('  '.join(map(str, coord_ui_top)))
        ui_counter = 1
        for row in self.board:
            if len(row) < 7:
                row.insert(0, ui_counter)
                ui_counter += 1
            print('  '.join(map(str, row)))
            row.pop(0)
        print('')
    
    def separator(): print('------------------------')

class Ship: 

    def __init__(self, board):
        self.board = board
    
    def set_ai_ships(self):
        self.ships_hit = 0
        for self.ship_length in SHIP_LENGTHS: 
            while True:
                self.row, self.column, self.orientation = random.randint(1,6), random.randint(1,6), random.choice(['V','H'])
                if Ship.is_valid_to_set(self):
                    if Ship.is_neighbour(self) == False:
                        if Ship.is_overlapping(self) == False:
                            if self.orientation == 'V': 
                                for self.row_set in range(self.row-1, self.row-1 + self.ship_length):
                                    self.board[self.row_set][self.column-1] = 'S'
                            else: 
                                for self.column_set in range(self.column-1, self.column-1 + self.ship_length):
                                    self.board[self.row-1][self.column_set] = 'S'
                            break
                        else: continue
                    else: continue
                else: continue 
        return self.board
    
    def set_user_ships(self):
        self.ships_hit = 0
        for self.ship_length in SHIP_LENGTHS:
            while True:
                Board.separator()
                print(f'LENGTH OF SHIP TO PLACE: {self.ship_length}')
                Board.separator()
                Ship.user_input(self)
                if Ship.is_valid_to_set(self):
                    if Ship.is_neighbour(self) == False:
                        if Ship.is_overlapping(self) == False:
                            if self.orientation == 'V': 
                                for self.row_set in range(self.row-1, self.row-1 + self.ship_length):
                                    self.board[self.row_set][self.column-1] = 'S'
                            else: 
                                for self.column_set in range(self.column-1, self.column-1 + self.ship_length):
                                    self.board[self.row-1][self.column_set] = 'S'
                            break
                        else: 
                            Board.separator()
                            Board.print_board(self)
                            print('You cannot place a ship there! Try again.')
                            continue 
                    else:
                        Board.separator()
                        Board.print_board(self)
                        print('You cannot place a ship next to another ship!. Try again.')
                        continue
                else:
                    Board.separator()
                    Board.print_board(self)
                    print("Your ship doesn't fit on the board! Try again.")
                    continue
            Board.print_board(self)
        return self.board

    def user_input(self):
        while True:
            try:
                self.row, self.column, self.orientation = int(input('Type in row -> ')), int(input('Type in column -> ')), input('Type in orientation. V - for vertical, H - for horizontal -> ').upper()
                while self.row not in VALID_COORDINATES or self.column not in VALID_COORDINATES or self.orientation not in VALID_ORIENTATION:
                    Board.separator()
                    print('Please enter a number between 1-6 and a valid orientation: V or H')
                    self.row, self.column, self.orientation = int(input('Type in row -> ')), int(input('Type in column -> ')), input('Type in orientation. V - for vertical, H - for horizontal -> ').upper()
                break    
            except ValueError: 
                print('Please enter a number between 1-6')
                continue

    def user_input_shoot(self):
        self.row, self.column = int(input('Type in row -> ')), int(input('Type in column -> '))
        while self.row not in VALID_COORDINATES or self.column not in VALID_COORDINATES:
            Board.separator()
            print('Please enter a number between 1-6')
            self.row, self.column = int(input('Type in row -> ')), int(input('Type in column -> '))

    def is_valid_to_set(self):
        if self.orientation == 'V':
            return False if self.row-1 + self.ship_length-1 >= 6 else True
        else: return False if self.column-1 + self.ship_length-1 >= 6 else True
    
    def is_neighbour(self):
        count_check = 0
        if self.orientation == 'V':
            for self.row_set in range(self.row-1, self.row-1 + self.ship_length):
                try:
                    if self.row_set-1 >= 0:
                        if self.board[self.row_set-1][self.column-1] == 'S': #CHECK FOR TOP NEIGHBOR
                            count_check +=1
                except IndexError: pass
                try:
                    if self.board[self.row_set+1][self.column-1] == 'S': #CHECK FOR BOTTOM NEIGHBOUR
                        count_check +=1
                except IndexError: pass
                try: 
                    if self.column-2 >= 0:
                        if self.board[self.row_set][self.column-2] == 'S': #CHECK FOR LEFT NEIGHBOUR
                            count_check +=1
                except IndexError: pass
                try:
                    if self.board[self.row_set][self.column] == 'S':  #CHECK FOR RIGHT NEIGHBOUR
                        count_check +=1
                except IndexError: pass
            if count_check > 0: return True
        else:
            for self.column_set in range(self.column-1, self.column-1 + self.ship_length):
                try:
                    if self.row-2 >= 0:
                        if self.board[self.row-2][self.column_set] == 'S': #CHECK FOR TOP NEIGHBOUR
                            count_check +=1
                except IndexError: pass
                try: 
                    if self.board[self.row][self.column_set] == 'S': #CHECK FOR BOTTOM NEIGHBOUR 
                        count_check +=1
                except IndexError: pass
                try: 
                    if self.column_set-1 >= 0:
                        if self.board[self.row-1][self.column_set-1] == 'S': #CHECK FOR LEFT NEIGHBOUR
                            count_check +=1
                except IndexError: pass
                try:
                    if self.board[self.row-1][self.column_set+1] == 'S':  #CHECK FOR RIGHT NEIGHBOUR
                        count_check +=1
                except IndexError: pass
            if count_check > 0: return True
    
        return False

    def is_overlapping(self):
        if self.orientation == 'V':
            for i in range(self.row-1, self.row-1 + self.ship_length):
                return True if self.board[i][self.column-1] == 'S' else False
        else:
            for i in range(self.column-1, self.column-1 + self.ship_length):
                return True if self.board[self.row-1][i] == 'S' else False
    
    def check_for_game_over(self):
        return True if self.ships_hit == 11 else False

    def guess_user_ship(self):
        self.row, self.column = random.randint(1,6), random.randint(1,6)
        while self.board[self.row-1][self.column-1] == 'X' or self.board[self.row-1][self.column-1] == '#':
            self.row, self.column = random.randint(1,6), random.randint(1,6)

        if self.board[self.row-1][self.column-1] == 'S':
            self.board[self.row-1][self.column-1] = 'X'
            self.ships_hit += 1
            Board.separator()
            print("He hit your ship!")
            Board.separator()
        else: 
            self.board[self.row-1][self.column-1] = '#'
            Board.separator()
            print('Your opponent tried to hit your ship and he missed.')
            Board.separator()

    def guess_ai_ship(self, guess_board):
        print('GUESS OPPONENT SHIP!')
        Board.print_board(guess_board)
        Ship.user_input_shoot(self)
        while self.board[self.row-1][self.column-1] == 'X' or self.board[self.row-1][self.column-1] == '#':
            Ship.user_input_shoot(self)
        if self.board[self.row-1][self.column-1] == 'S':
            self.board[self.row-1][self.column-1] = 'X'
            guess_board.board[self.row-1][self.column-1] = 'X'
            self.ships_hit += 1
            Board.separator()
            print("You've hit an opponents ship!")
            Board.separator()
        else: 
            self.board[self.row-1][self.column-1] = '#'
            guess_board.board[self.row-1][self.column-1] = '#'
            Board.separator()
            print("You've missed.")
            Board.separator()

class Game:   
    def run_game(): 
        random.seed(time.time())
        ai_board = Board([['.']*6 for i in range(6)])
        user_board = Board([['.']*6 for i in range(6)])
        starting_board = Board([['.']*6 for i in range(6)])
        guess_board = Board([['.']*6 for i in range(6)])

        #set ships
        Ship.set_ai_ships(ai_board)
        Board.print_board(starting_board)
        print("""Welcome, Player! BOT "Jack the Sparrow" is challenging you to a game of Battleships!
Are u ready? If so, let's put these skills to the test, shall we?""")

        # ai_board.print_board() # DEBUG
        Ship.set_user_ships(user_board)

        while True:
            Ship.guess_user_ship(user_board)
            Ship.guess_ai_ship(ai_board, guess_board)
            if Ship.check_for_game_over(ai_board) or Ship.check_for_game_over(user_board):
                break
        if Ship.check_for_game_over(user_board):
            Board.separator()
            print('You have lost.')
            Board.separator()
            print('ENEMY BOARD WITH YOUR SHOTS: ')
            Board.print_board(ai_board)
            Board.separator()
            print('YOUR BOARD WITH ENEMY SHOTS: ')
            Board.print_board(user_board)
        elif Ship.check_for_game_over(ai_board):
            Board.separator()
            print('You won!')
            Board.separator()
            print('ENEMY BOARD: ')
            Board.separator
            Board.print_board(guess_board)
            print('YOUR BOARD WITH ENEMY BULLETS: ')
            Board.separator
            Board.print_board(user_board)

if __name__ == "__main__":
    Game.run_game()