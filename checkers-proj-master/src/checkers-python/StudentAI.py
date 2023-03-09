from random import randint
from BoardClasses import Move
from BoardClasses import Board
from TimeCheck import TimeCheck
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.time = TimeCheck()
    def get_move(self,move):
        self.time.start()       # Start the timer
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        # Get all possible moves for this iteration
        moves = self.board.get_all_possible_moves(self.color)
        """
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        """

        # For each possible move, perform a greedy search (check if we lose a piece with the move)
        best_score = -10000  # For holding the value of the current best move
        best_1move = Move([])  # For holding the current best move, according to one step lookahead
        if self.time.check_time() >= 450:   # 7 minutes and 30 seconds
            depth = 2
        else:
            depth = 5
        for moveset in moves:
            for move in moveset:
                self.board.make_move(move,self.color)
                eval = self._evaluate(self.color)
                if eval > best_score:
                    best_1move = move
                    best_score = eval
                self.board.undo()

        best_move = best_1move # For holding the current best move

        # Search through the best move first
        self.board.make_move(best_1move, self.color)
        best_score = self._search(self.color, depth, -1000, 1000)
        self.board.undo()

        for moveset in moves:
            for move in moveset:
                if move == best_1move:
                    continue
                self.board.make_move(move,self.color)
                eval = self._search(self.color, depth, -1000, 1000)
                self.board.undo()       # Backtracking

                if eval > best_score:
                    best_score = eval
                    best_move = move

                elif eval == best_score:
                    if randint(0,1) == 1:
                        best_score = eval
                        best_move = move

        # Update the AI's board with the best move
        self.board.make_move(best_move, self.color)

        # Return the best move as found in the search algorithm
        self.time.pause()       # Pause the timer
        return best_move

    def _search(self, player, depth, alpha, beta):
        # Check if the desired depth has been reached, or if the game has ended
        if depth == 0 or self.board.is_win(player) != 0:
            return self._evaluate(player)

        # Get the next player's color
        if player == 1:
            nxt = 2
        else:
            nxt = 1

        # For each move that this player can take, search through the move
        moves = self.board.get_all_possible_moves(nxt)
        for moveset in moves:
            for move in moveset:
                self.board.make_move(move, nxt)
                eval = self._search(nxt, depth-1, alpha, beta)
                self.board.undo()       # Backtracking

                # Alpha beta pruning; depending on whose turn it is, update values accordingly
                if nxt == self.color:       # MAX node
                    alpha = max(alpha, eval)
                    if (alpha >= beta):     # If alpha >= beta, this path will not be taken, and so can be pruned
                        break

                else:                       # MIN node
                    beta = min(beta, eval)
                    if (alpha >= beta):
                        break

        # Depending on whose move it is, return either the max value (alpha) or min value (beta)
        if nxt == self.color:
            return alpha
        else:
            return beta

    def _king_cnt(self, color):
        # Running sum of kings
        kings = 0
        for row in range(self.board.row):
            for col in range(self.board.col):
                checker = self.board.board[row][col]
                if checker.color == color and checker.is_king:
                    kings += 1
        return kings

    def _evaluate(self, player):
        # Variable to check if someone won
        win = self.board.is_win(player)
        # If this is a tie state, return a good score: 100
        if win == -1:
            return 100
        # If this is a winning state, return a high or low value based on who won
        elif win:
            if player == self.color:        # This AI has won
                return 1000
            else:                           # The other player has won
                return -1000

        # Otherwise, return the difference in checker pieces
        if self.color == 1:     # AI is black
            return (self.board.black_count + self._king_cnt(1)) - (self.board.white_count + self._king_cnt(2))
        else:                   # AI is white
            return (self.board.white_count + self._king_cnt(2)) - (self.board.black_count + self._king_cnt(1))