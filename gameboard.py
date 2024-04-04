class BoardClass:
    """Information about tic-tac-toe board.

    Board information is meant to be client and server-side. 
    
    Attributes:
    name (str): Player user name.
    name2 (str): Player 2 user name.
    player (boolean): True if P1 (Client), False if P2 (Server).
    _last (str): Last player to have a turn. At first, it will be P2.
    _turn (boolean): P1's turn if True.
    _wins (int): # of wins for whatever shell creates a board object.
    _losses (int): # of losses.
    _ties (int): # of ties.
    _games (int): # of total games played and completed.
    _board (list[[str, str, str], [str, str, str], [str, str, str]]): 2D data structure representing a tic-tac-toe board.
    
    """

    def __init__(self, userName:str, userName2:str, player:bool, turn:bool=True,
                 win:int=0, loss:int=0, tie:int=0, game:int=0) -> None:
        """Start a game."""
        self.name = userName
        self.name2 = userName2
        self.player = player
        self._last = userName2
        self._turn = turn
        self._wins = win
        self._losses = loss
        self._ties = tie
        self._games = game
        self._board = ['-', '-', '-', '-', '-', '-', '-' , '-', '-']
        

    def updateGamesPlayed(self) -> None:
        """Make sure the game total is up to date."""
        self._games = self._wins + self._losses + self._ties


    def resetGameBoard(self) -> None:
        """Reset board, turn and last turn to default."""
        self._board = ['-', '-', '-', '-', '-', '-', '-' , '-', '-']
        self._turn = True
        self._last = self.name2


    def updateGameBoard(self, pos: int) -> None:
        """Take input from current player and update board and turn.

        Parameters:
        pos (int): int within 0-8 representing board position
        
        """
        if self._turn: 
            symbol = 'x' # Player 1.
        else:
            symbol = 'o' # Player 2.

        self._board[pos] = symbol # Replace position with symbol.

        self._turn = not(self._turn) # Pass turn onto next player.

        # Last move is turned into who just went.
        if self._last == self.name2: 
            self._last = self.name
        elif self._last == self.name:
            self._last = self.name2

    def isWinner(self) -> bool:
        """Check if last move is a game-winning move. Update wins and losses.

        Returns boolean stating whether or not last move won the game.
        
        """
        xWin = ['x', 'x', 'x']
        oWin = ['o', 'o', 'o']
        p1Flag = False
        p2Flag = False
        
        # Check for wins for respective players.
        if ([self._board[0], self._board[1], self._board[2]] == xWin or # Rows
            [self._board[3], self._board[4], self._board[5]] == xWin or
            [self._board[6], self._board[7], self._board[8]] == xWin or
            [self._board[0], self._board[3], self._board[6]] == xWin or # Columns
            [self._board[1], self._board[4], self._board[7]] == xWin or
            [self._board[2], self._board[5], self._board[8]] == xWin or
            [self._board[0], self._board[4], self._board[8]] == xWin or # Diagonal
            [self._board[2], self._board[4], self._board[6]] == xWin):
            p1Flag = True
        elif ([self._board[0], self._board[1], self._board[2]] == oWin or # Rows
              [self._board[3], self._board[4], self._board[5]] == oWin or
              [self._board[6], self._board[7], self._board[8]] == oWin or
              [self._board[0], self._board[3], self._board[6]] == oWin or # Columns
              [self._board[1], self._board[4], self._board[7]] == oWin or
              [self._board[2], self._board[5], self._board[8]] == oWin or
              [self._board[0], self._board[4], self._board[8]] == oWin or # Diagonal
              [self._board[2], self._board[4], self._board[6]] == oWin):
            p2Flag = True

        # Update count for wins and losses.
        if p1Flag: # Player 1 wins.
            if self.player:
                self._wins += 1 
            else:
                self._losses += 1
            return True
        elif p2Flag: # Player 2 wins.
            if self.player:
                self._losses += 1
            else:
                self._wins += 1
            return True
        else:
            return False

   
    def boardIsFull(self) -> None:
        """Check if board is full. If full, add to ties.

        Returns boolean stating if there is a tie or not.
        
        """
        # Copypasted code to ensure no wins (isWinner() caused unnecessary counting).
        xWin = ['x', 'x', 'x']
        oWin = ['o', 'o', 'o']
        winFlag = False
        
        # Check for Player 1 wins.
        if ([self._board[0], self._board[1], self._board[2]] == xWin or # Rows
            [self._board[3], self._board[4], self._board[5]] == xWin or
            [self._board[6], self._board[7], self._board[8]] == xWin or
            [self._board[0], self._board[3], self._board[6]] == xWin or # Columns
            [self._board[1], self._board[4], self._board[7]] == xWin or
            [self._board[2], self._board[5], self._board[8]] == xWin or
            [self._board[0], self._board[4], self._board[8]] == xWin or # Diagonal
            [self._board[2], self._board[4], self._board[6]] == xWin or
            [self._board[0], self._board[1], self._board[2]] == oWin or # Rows
            [self._board[3], self._board[4], self._board[5]] == oWin or
            [self._board[6], self._board[7], self._board[8]] == oWin or
            [self._board[0], self._board[3], self._board[6]] == oWin or # Columns
            [self._board[1], self._board[4], self._board[7]] == oWin or
            [self._board[2], self._board[5], self._board[8]] == oWin or
            [self._board[0], self._board[4], self._board[8]] == oWin or # Diagonal
            [self._board[2], self._board[4], self._board[6]] == oWin):
            winFlag = True

        # Make sure no win and full board.
        if not(winFlag):
            if '-' not in self._board:
                self._ties += 1
                return True
            else:
                return False

    def printBoard(self) -> None:
        """Print out the board"""
        print(f'{self._board[0]} | {self._board[1]} | {self._board[2]}')
        print('---------')
        print(f'{self._board[3]} | {self._board[4]} | {self._board[5]}')
        print('---------')
        print(f'{self._board[6]} | {self._board[7]} | {self._board[8]}')
        
    
    def computeStats(self) -> list:
        """Return all info about the board."""
        stats = [self.name,self.name2,self._games,self._wins,self._losses,self._ties]
        return stats

    def getTurn (self) -> bool:
        """Print out whose turn it is

        Returns a boolean indicative of whose turn it is.
        """
        return self._turn
