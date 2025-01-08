import random

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        # Set to True if you would like to run gradescope against the challenge AI!
        # Leave as False if you would like to run the gradescope tests faster for debugging.
        # You can still get full credit with this set to False
        return False
    
    def move(self, state, move, piece):
        new_state = [row.copy() for row in state]

        if len(move) == 1:
            row, col = move[0]
            new_state[row][col] = piece
        elif len(move) == 2:
            new_row, new_col = move[0]
            old_row, old_col = move[1]
            new_state[old_row][old_col] = ' '
            new_state[new_row][new_col] = piece 

        return new_state


    def minimax(self, state, depth, is_maximizing_player, alpha, beta, max_depth):
        game_value = self.game_value(state)
        if depth == max_depth or game_value != 0:
            return self.get_hs(state)

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_succs(state, self.my_piece):
                new_state = self.move(state, move, self.my_piece)
                eval = self.minimax(new_state, depth + 1, False, alpha, beta, max_depth)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha: #pruning Process
                    break
            return max_eval
        # I got the pseudo code from geeks for geeks, I just needed a skeleton to help. If we cannot use
        # an external site like I did here, then I would prefer to keep my previous submission that I did fully myself: 
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # But I still had to figure out how this applies to our project because it is not exact.
        else:
            min_eval = float('inf')
            for move in self.get_succs(state, self.opp):
                new_state = self.move(state, move, self.opp)
                eval = self.minimax(new_state, depth + 1, True, alpha, beta, max_depth)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:#pruning process
                    break
            return min_eval

    def get_hs(self, state):
        ai = self.pieces[0]
        player = self.pieces[1] 
        h_val = 0

        #diags
        diagonals = [[state[i][i] for i in range(5)], [state[i][4-i] for i in range(5)]]
        for diag in diagonals:
            ai_curr_val = diag.count(ai)
            player_curr_val = diag.count(player)
            if ai_curr_val == 4:
                h_val += 4 #Chatgpt suggested adding different penalties for different circumstances like this. I chose some different values based on situations here.
            elif player_curr_val == 4:
                h_val -= 4
            elif ai_curr_val == 3 and player_curr_val == 0:
                h_val += 3
            elif player_curr_val == 3 and ai_curr_val == 0:
                h_val -= 3 
            elif ai_curr_val == 2 and player_curr_val == 0:
                h_val += 2
            elif player_curr_val == 2 and ai_curr_val == 0:
                h_val -= 2

        #rows
        for row in state:
            ai_curr_val = row.count(ai) # get number of ai players in a row
            player_curr_val = row.count(player) #get number of 'player' players to contrast
            if ai_curr_val == 4:
                h_val += 4 #Chatgpt suggested adding different penalties for different circumstances like this. I chose some different values based on situations here.
            elif player_curr_val == 4:
                h_val -= 4
            elif ai_curr_val == 3 and player_curr_val == 0:
                h_val += 3
            elif player_curr_val == 3 and ai_curr_val == 0:
                h_val -= 3 
            elif ai_curr_val == 2 and player_curr_val == 0:
                h_val += 2
            elif player_curr_val == 2 and ai_curr_val == 0:
                h_val -= 2

        #columns
        for col in range(5):
            column = [state[row][col] for row in range(5)]
            ai_curr_val = column.count(ai)
            player_curr_val = column.count(player)
            if ai_curr_val == 4:
                h_val += 4 #Chatgpt suggested adding different penalties for different circumstances like this. I chose some different values based on situations here.
            elif player_curr_val == 4:
                h_val -= 4
            elif ai_curr_val == 3 and player_curr_val == 0:
                h_val += 3
            elif player_curr_val == 3 and ai_curr_val == 0:
                h_val -= 3 
            elif ai_curr_val == 2 and player_curr_val == 0:
                h_val += 2
            elif player_curr_val == 2 and ai_curr_val == 0:
                h_val -= 2

        #squares
        for row in range(4):  
            for col in range(4): 
                square = [state[row][col], state[row][col + 1],state[row + 1][col], state[row + 1][col + 1]]
                ai_curr_val = square.count(ai)
                user_curr_val = square.count(player)
            if ai_curr_val == 4:
                h_val += 4 #Chatgpt suggested adding different penalties for different circumstances like this. I chose some different values based on situations here.
            elif user_curr_val == 4:
                h_val -= 4
            elif ai_curr_val == 3 and user_curr_val == 0:
                h_val += 3
            elif user_curr_val == 3 and ai_curr_val == 0:
                h_val -= 3 
            elif ai_curr_val == 2 and user_curr_val == 0:
                h_val += 2
            elif user_curr_val == 2 and ai_curr_val == 0:
                h_val -= 2

        return h_val

    def make_move(self, state, max_depth=3):
        '''Selects the best move for the AI, considering the state of the game.'''
        
        best_move = None
        best_h_val = float('-inf')
        count_non_spaces = sum(1 for row in state for cell in row if cell != ' ')

        drop_phase = count_non_spaces < 8

        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        move_instance = [row.copy() for row in state]
                        move_instance[row][col] = self.my_piece
                        h_val = self.get_hs(move_instance)
                        if h_val > best_h_val:
                            best_h_val = h_val
                            best_move = [(row, col)]
        else:
            best_move = self.minimax_move(state, max_depth)

        return best_move
    
    def minimax_move(self, state, max_depth):
        best_move = None
        best_value = float('-inf')
        for move in self.get_succs(state, self.my_piece):
            new_state = self.move(state, move, self.my_piece)
            move_value = self.minimax(new_state, 0, False, float('-inf'), float('inf'), max_depth)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move

    def get_succs(self, state, piece):
        moves = []
        size = len(state)
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        def in_bounds(x, y):
            return 0 <= x < size and 0 <= y < size
        for row in range(size):
            for col in range(size):
                if state[row][col] == ' ':
                    moves.append([(row, col)])
                elif state[row][col] == piece:
                    for dx, dy in directions:
                        new_row, new_col = row + dx, col + dy
                        if in_bounds(new_row, new_col) and state[new_row][new_col] == ' ':
                            moves.append([(new_row, new_col), (row, col)])
        return moves
    

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1
                if state[i][j+3] != ' ' and state[i][j+3] == state[i+1][j+2] == state[i+2][j+1] == state[i+3][j]:
                    return 1 if state[i][j+3] == self.my_piece else -1
        # TODO: check box wins
        for row in range(4):
            for col in range(4): # goes through every square
                square = {state[row][col], state[row][col+1], state[row+1][col], state[row+1][col+1]}
                if len(square) == 1 and ' ' not in square:
                    return 1 if square.pop() == self.my_piece else -1
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()