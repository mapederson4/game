import random

class TeekoPlayer:
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    piece_coord = dict()
    piece_coord["my_piece"] = set()

    def __init__(self):
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        return True

    def execute_Move(self, piece, choice, orig_state):
        updated = [row.copy() for row in orig_state]
        updated[choice[0][0]][choice[0][1]] = piece
        if len(choice) > 1:
            updated[choice[1][0]][choice[1][1]] = ' '
        return updated
    
    def get_succs(self, state, piece):
        succs = []
        piece_list = [(i, j) for i in range(5) for j in range(5) if state[i][j] == piece]
        
        if len(piece_list) < 4: #for drop phase
            return [[(i, j)] for i in range(5) for j in range(5) if state[i][j] == ' ']
        
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for pos in piece_list:
            for rowval, colval in moves:
                new_row=pos[0] + rowval
                new_col = pos[1] + colval
                if 0 <= new_row < 5 and 0 <= new_col < 5 and state[new_row][new_col] == ' ':
                    succs.append([(new_row, new_col), pos])
        return succs

    def minimax(self, state, depth, is_maximizing_player, alpha, beta, max_depth):
        game_value = self.game_value(state)
        
        if depth == max_depth or game_value != 0:
            return self.get_hs(state), None
        
        best_move = None
        if is_maximizing_player:
            max_eval = float('-inf')
            moves = self.get_succs(state, self.my_piece)
            moves.sort(key=lambda m: self.get_hs(self.execute_Move(self.my_piece, m, state)), reverse=True)
        # I got the pseudo code from geeks for geeks, I just needed a skeleton to help. If we cannot use
        # an external site like I did here, then I would prefer to keep a previous submission that I did fully myself: 
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # But I still had to figure out how this applies to our project because it is not exact.
            for move in moves:
                new_state = self.execute_Move(self.my_piece, move, state)
                eval, _ = self.minimax(new_state, depth + 1, False, alpha, beta, max_depth)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move #return both to debug here
        
        else:
            min_eval = float('inf')
            moves = self.get_succs(state, self.opp)
            moves.sort(key=lambda m: self.get_hs(self.execute_Move(self.opp, m, state)))
            
            for move in moves:
                new_state = self.execute_Move(self.opp, move, state)
                eval, _ = self.minimax(new_state, depth + 1, True, alpha, beta, max_depth)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_hs(self, state):
        h_val = 0
        
        #rows
        for row in state:
            for i in range(2):
                line = row[i:i+4]
                ai_curr_val = line.count(self.my_piece)
                player_curr_val = line.count(self.opp)
                empty = line.count(' ')

                if ai_curr_val == 4:
                    h_val += 100
                elif player_curr_val == 4:
                    h_val -= 100
                
                elif ai_curr_val == 3 and empty == 1:
                    h_val += 10
                elif player_curr_val == 3 and empty == 1:
                    h_val -= 12
                
                elif ai_curr_val == 2 and empty == 2:
                    h_val += 2
                elif player_curr_val == 2 and empty == 2:
                    h_val -= 3
                
                else:
                    h_val += ai_curr_val - player_curr_val

        #cols
        for col in range(5):
            for i in range(2):
                line = [state[i+j][col] for j in range(4)]
                ai_curr_val = line.count(self.my_piece)
                player_curr_val = line.count(self.opp)
                empty = line.count(' ')
                
                if ai_curr_val == 4:
                    h_val += 100
                elif player_curr_val == 4:
                    h_val -= 100
                elif ai_curr_val == 3 and empty == 1:
                    h_val += 10
                elif player_curr_val == 3 and empty == 1:
                    h_val -= 12
                elif ai_curr_val == 2 and empty == 2:
                    h_val += 2
                elif player_curr_val == 2 and empty == 2:
                    h_val -= 3
                else:
                    h_val += ai_curr_val - player_curr_val

        # diags
        for i in range(2):
            for j in range(2):
                #1
                diag = [state[i+k][j+k] for k in range(4)]
                ai_curr_val = diag.count(self.my_piece)
                player_curr_val = diag.count(self.opp)
                empty = diag.count(' ')
                
                if ai_curr_val == 4:
                    h_val += 100
                elif player_curr_val == 4:
                    h_val -= 100
                elif ai_curr_val == 3 and empty == 1:
                    h_val += 10
                elif player_curr_val == 3 and empty == 1:
                    h_val -= 12
                
                #2
                diag = [state[i+k][j+3-k] for k in range(4)]
                ai_curr_val = diag.count(self.my_piece)
                player_curr_val = diag.count(self.opp)
                empty = diag.count(' ')
                
                if ai_curr_val == 4:
                    h_val += 100
                elif player_curr_val == 4:
                    h_val -= 100
                elif ai_curr_val == 3 and empty == 1:
                    h_val += 10
                elif player_curr_val == 3 and empty == 1:
                    h_val -= 12

        #middle advantage
        if state[2][2] == self.my_piece:
            h_val += 3
        elif state[2][2] == self.opp:
            h_val -= 3

        return h_val

    def make_move(self, state, max_depth=4):
        piece_count = sum(1 for row in state for col in row if col != ' ')
        drop_phase = piece_count < 8
        
        if drop_phase:
            best_move = None
            best_value = float('-inf')
            
            best_position_list = [ # Chatgpt gave a suggestion after I still couldnt get tests passing.
                                    # the center should be prioritized especially in the drop phase so I did this here
                [(2, 2)],           # may or may not be necessary but I think it helps to start with these values
                
                [(1, 1), (1, 2), (1, 3),
                (2, 1),         (2, 3),
                (3, 1), (3, 2), (3, 3)],
                
                [(i, j) for i in range(5) for j in range(5)
                if (i, j) not in [(2, 2)] +
                                [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3),(3, 1), (3, 2), (3, 3)]]]
            positions = []
            for level in best_position_list:
                positions.extend(level)
                
            for pos in positions:
                if state[pos[0]][pos[1]] == ' ':
                    new_state = [row.copy() for row in state]
                    new_state[pos[0]][pos[1]] = self.my_piece
                    value = self.get_hs(new_state)
                    
                    if value > best_value:
                        best_value = value
                        best_move = [(pos[0], pos[1])]
            
            if best_move:
                self.piece_coord["my_piece"].add(best_move[0])
                self.piece_coord[best_move[0]] = 1
                return best_move
        
        value, best_move = self.minimax(state, 0, True, float('-inf'), float('inf'), max_depth)
        
        if best_move:
            if len(best_move) > 1:
                self.piece_coord["my_piece"].remove(best_move[1]) #tried to speed up runtime by saving pieces that have been laid
                del self.piece_coord[best_move[1]]                #this method seems successful
                self.piece_coord["my_piece"].add(best_move[0])
                self.piece_coord[best_move[0]] = 1
            else:
                self.piece_coord["my_piece"].add(best_move[0])
                self.piece_coord[best_move[0]] = 1
        
        return best_move

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