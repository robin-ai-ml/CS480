
class MinMaxSearch:
    def __init__(self, game):
        self.game = game

    """
        Search for the best move in the game state.

            Parameters:
                state (GameState): The current game state.

            Returns:
                tuple: A tuple containing the best move and the number of nodes explored.    
    """
    def search(self, state):
        nodes_cnt = 0
        player =  self.game.to_move(state)
        if(player == 'X'):
            _, move, nodes_cnt = self.max_value(state, nodes_cnt)
        
        elif (player == 'O'):
            _, move, nodes_cnt = self.min_value(state, nodes_cnt)

        return  move, nodes_cnt
    
    """
        Calculates the maximum value of a state in the game tree.

        Parameters:
            state (any): The current state in the game tree.
            nodes_cnt (int): The number of nodes explored so far.

        Returns:
            tuple: A tuple containing the maximum value of the state, the optimal move, and the updated number of nodes explored.
    """    
    def max_value(self, state, nodes_cnt):
        nodes_cnt += 1
        if self.game.is_terminal(state):
            return self.game.utility(state), None, nodes_cnt

        v = float('-inf')
        move = None
        for a in self.game.actions(state):
            new_states = self.game.result(state, a)
            v2, _, nodes_cnt = self.min_value(new_states, nodes_cnt)
            if v2 > v:
                v = v2
                move = a
        return v, move, nodes_cnt

    """
        Calculates the minimum value of a state in a game tree.

        Args:
            state (any): The current state in the game tree.
            nodes_cnt (int): The number of nodes explored so far.

        Returns:
            tuple: A tuple containing the minimum value of the state, the move that leads to the minimum value, and the updated number of nodes explored.
    """
    def min_value(self, state, nodes_cnt):
        nodes_cnt += 1
        if self.game.is_terminal(state):
            return self.game.utility(state), None, nodes_cnt

        v = float('inf')
        move = None
        for a in self.game.actions(state):
            new_states = self.game.result(state, a)
            v2, _, nodes_cnt = self.max_value(new_states, nodes_cnt)
            if v2 < v:
                v = v2
                move = a
        return v, move, nodes_cnt


class MinMaxWithAlphaBetaSearch:
    def __init__(self, game):
        self.game = game

    """
        Search for the best move in the game state.

            Parameters:
                state (GameState): The current game state.

            Returns:
                tuple: A tuple containing the best move and the number of nodes explored.    
    """
    def search(self, state):
        nodes_cnt = 0
        player =  self.game.to_move(state)
        if(player == 'X'):
            _, move, nodes_cnt = self.max_value(state, nodes_cnt, float('-inf'), float('inf'))
        
        elif (player == 'O'):
            _, move, nodes_cnt = self.min_value(state, nodes_cnt, float('-inf'), float('inf'))

        return  move, nodes_cnt


    """
        Calculates the maximum value of a state in the game tree.

        Parameters:
            state (any): The current state in the game tree.
            nodes_cnt (int): The number of nodes explored so far.
            alpha (float): the value of the best (highest-value) choice we have found so far at any choice point along the
                           path for MAX player (“at least”).
            beta (float):  the value of the best (lowest-value) choice we have found so far at any choice point along the
                           path for MIN player (“at most”)

        Returns:
            tuple: A tuple containing the maximum value of the state, the optimal move, and the updated number of nodes explored.
    """  
    def max_value(self, state, nodes_cnt, alpha, beta):
        nodes_cnt += 1
        if self.game.is_terminal(state):
            return self.game.utility(state), None, nodes_cnt

        v = float('-inf')
        move = None
        for a in self.game.actions(state):
            new_states = self.game.result(state, a)
            v2, _, nodes_cnt = self.min_value(new_states, nodes_cnt, alpha, beta)
            if v2 > v:
                v = v2
                move = a
                alpha = max(alpha, v)
            if v >= beta:# break as a pruning
                return v, move, nodes_cnt 
        return v, move, nodes_cnt


    """
        Calculates the minimum value of a state in the game tree.

        Parameters:
            state (any): The current state in the game tree.
            nodes_cnt (int): The number of nodes explored so far.
            alpha (float): the value of the best (highest-value) choice we have found so far at any choice point along the
                           path for MAX player (“at least”).
            beta (float):  the value of the best (lowest-value) choice we have found so far at any choice point along the
                           path for MIN player (“at most”)

        Returns:
            tuple: A tuple containing the maximum value of the state, the optimal move, and the updated number of nodes explored.
    """
    def min_value(self, state, nodes_cnt, alpha, beta):
        nodes_cnt += 1
        if self.game.is_terminal(state):
            return self.game.utility(state), None, nodes_cnt

        v = float('inf')
        move = None
        for a in self.game.actions(state):
            new_states = self.game.result(state, a)
            v2, _, nodes_cnt = self.max_value(new_states, nodes_cnt, alpha, beta)
            if v2 < v:
                v = v2
                move = a
                beta = min(beta, v)
            if v <= alpha:# break as a pruning
                return v, move, nodes_cnt 
        return v, move, nodes_cnt
    

class TicTacToe:

    """
        Initializes a new instance of the class.

        Parameters:
            first_player (str): The name of the first player. either 'X' or 'O'

        Returns:
            None
    """
    def __init__(self, first_player):

        self.board = [' '] * 9
        self.first_player = first_player

        self.winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
        (0, 4, 8), (2, 4, 6) # diagonals
        ]

    """
        Display the given board/state on the console.

        Parameters:
            board (list): A list representing the current state of the game board.

        Returns:
            None
    """
    def display_board(self, board):
        print(f'{board[0]}|{board[1]}|{board[2]}')
        print('-+-+-')
        print(f'{board[3]}|{board[4]}|{board[5]}')
        print('-+-+-')
        print(f'{board[6]}|{board[7]}|{board[8]}')

    """
        Returns a list of integers representing the available actions in the given state.

        Parameters:
            state (list): A list representing the current state of the game.

        Returns:
            list: A list of integers representing the available actions in the given state.
    """

    def actions(self, state):
        return [i+1 for i in range(9) if state[i] == ' '] #orderiing from  1 - 9 for computers

    """
        Determines the next player to move based on the current state of the game.

        Parameters:
            state (list): A list representing the current state of the game board.

        Returns:
            str: The next player to move, either 'X' or 'O'.
    """
    def to_move(self, state):
        count_x = state.count('X')
        count_o = state.count('O')
        
        if self.first_player == 'X':
            if count_x == count_o:
                return 'X'
            else:
                return 'O'
        elif self.first_player == 'O':
            if count_x == count_o:
                return 'O'
            else:
                return 'X'

    """
        Check if the given state is a terminal state.

        Parameters:
            state (list): The current state of the game board.

        Returns:
            bool: True if the state is a terminal state, False otherwise.
    """
    def is_terminal(self, state):
        for combo in self.winning_combinations:
            if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
                return True
        if ' ' not in state:
            return True
        return False


    """
        Calculates the utility of a given state in the game.

        Parameters:
            state (list): The current state of the game board.

        Returns:
            int: The utility value of the state. Returns 1 if 'X' wins, -1 if 'O' wins, and 0 if the game is a draw.
    """
    def utility(self, state):
        for combo in self.winning_combinations:
            if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
                winner =  state[combo[0]]
                if winner == 'X':
                    return 1
                elif winner == 'O':
                    return -1

        return 0
   
    """
        Updates the state of the game board by making a move.

        Parameters:
            state (list): The current state of the game board.
            action (int): The action to be taken on the game board.

        Returns:
            list: The updated state of the game board after the move.
    """
    def result(self, state, action):
        new_state = state[:]
        if new_state[action - 1] == ' ':
            new_state[action - 1] = self.to_move(new_state)
        return new_state

    """
        Returns the state of the board.
    """
    def state(self):
        return self.board
    
    """
        Move a piece on the board.

        Parameters:
            move (int): The position on the board where the piece should be moved.

        Returns:
            bool: True if the move is valid and was successfully executed, False otherwise.
    """
    def move(self, move):
        if self.board[move-1] == ' ':
            self.board[move-1] = self.to_move(self.board)
            return True
        else:
            return False

    """
        Returns the winner of the game if there is one.

        Returns:
            str or None: The winner of the game if there is one, None otherwise.
    """
    def get_winner(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        return None   
    
    """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
    """
    def is_game_over(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        if ' ' not in self.board:
            return True
        return False
   
from enum import Enum

class Algo(Enum):
    MINMAX = 1
    MINMAX_APHA_BETA = 2

class Player(Enum):
    HUMAN = 'X'
    COMPUTER = 'O'

class GameMode(Enum):
    HUMAN_VS_COMPUTER = 1
    COMPUTER_VS_COMPUTER = 2

"""
    Display game information based on the given algorithm, first player, and mode.

    Parameters:
        algo (str): The algorithm used for the game.
        first_player (str): The first player in the game.
        mode (str): The game mode.

    Returns:
        None
"""
def display_game_information(algo, first_player, mode):
    print('Xiaonan, Peng, A20554038 solution:')

    if algo == Algo.MINMAX.value:
        print('Algorithm: MinMax')
    elif algo == Algo.MINMAX_APHA_BETA.value:
        print('Algorithm: MinMax with alpha-beta pruning')

    if first_player == Player.HUMAN.value:
        print('First: X')
    elif first_player == Player.COMPUTER.value:
        print('First: O')

    if mode == GameMode.HUMAN_VS_COMPUTER.value:
        print('Mode: human  versus computer')
    elif mode == GameMode.COMPUTER_VS_COMPUTER.value:
        print('Mode: computer  versus computer')


import sys

if __name__ == '__main__':
   
    ''' Accept three (3) command line arguments, so your code could be executed with

            python CS480_P01_AXXXXXXXX.py ALGO FIRST MODE

            where:

                    ◦ CS480_P01_AXXXXXXXX.py is your python code file name,
                    ◦ ALGO specifies which algorithm the computer player will use:
                        ▪ 1  minmax_search,
                        ▪ 2  minmax_search with alpha-beta pruning,
                    ◦ FIRST specifies who begins the game:
                        ▪ X
                        ▪ O
                    ◦ MODE is mode in which your program should operate:
                        ▪ 1  human (X) versus computer (O)
                        ▪ 2  computer (X) versus computer (O)

            Example: python CS480_P01_A11111111.py 2 X 1   
    '''


    if len(sys.argv) != 4:
        print("ERROR: Not enough/too many/illegal input arguments.")
        sys.exit()

    algo = int(sys.argv[1])
    first_player = sys.argv[2].upper() #ingore case "X x O o" are valid
    mode = int(sys.argv[3])

    if algo not in [Algo.MINMAX.value, Algo.MINMAX_APHA_BETA.value] \
        or first_player not in [Player.HUMAN.value, Player.COMPUTER.value] \
        or mode not in [GameMode.HUMAN_VS_COMPUTER.value, GameMode.COMPUTER_VS_COMPUTER.value]:
        print("ERROR: Not enough/too many/illegal input arguments.")
        sys.exit()
    
    display_game_information(algo, first_player, mode)

    game = TicTacToe(first_player)

    if(algo == Algo.MINMAX.value):
        minmax = MinMaxSearch(game)
    elif(algo == Algo.MINMAX_APHA_BETA.value):
        minmax = MinMaxWithAlphaBetaSearch(game)

    if mode == GameMode.HUMAN_VS_COMPUTER.value:
        game.display_board(game.state())
        while not game.is_game_over():
            if game.to_move(game.state()) == Player.HUMAN.value:
                    try:
                        move = int(input("X's move. What is your move (possible moves at the moment are: {} enter 0 to exit the game)? " \
                                        .format(game.actions(game.state()))))
                        if move == 0:
                            sys.exit(0)
                        elif move not in game.actions(game.state()):
                            print("Invalid move. Please try again.")
                            continue
                    except ValueError:
                        print("Invalid move. Please try again.")
                        continue
                
            else:#==Player.COMPUTER
                move, nodes_generated = minmax.search(game.state())
                print("O's selected move: {}. Number of search tree nodes generated: {}".format(move, nodes_generated))
                
            game.move(move)
            game.display_board(game.state())

        #game is over here
        winner = game.get_winner()
        if winner == Player.HUMAN.value:
            print("X WON")
        elif winner == Player.COMPUTER.value:
            print("O WON")
        else:
            print("TIE")

    else:#==GameMode.COMPUTER_VS_COMPUTER
        while not game.is_game_over():
            if game.to_move(game.state()) == Player.HUMAN.value:
                move, nodes_generated = minmax.search(game.state())
                print("X's selected move: {}. Number of search tree nodes generated: {}".format(move, nodes_generated))

            else:
                move, nodes_generated = minmax.search(game.state())
                print("O's selected move: {}. Number of search tree nodes generated: {}".format(move, nodes_generated))

            game.move(move)
            game.display_board(game.state())
        #game is over here
        winner = game.get_winner()
        if winner == Player.HUMAN.value:
            print("X WON")
        elif winner == Player.COMPUTER.value:
            print("O WON")
        else:
            print("TIE")
