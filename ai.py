from game import Kalah, Player

DEBUG_SEARCH_TREE = False


class KalahAI:
    def __init__(self, maxSearchDepth, player: Player):
        if maxSearchDepth < 1:
            raise ValueError('maxSearchDepth must be at least 1')
        self.maxSearchDepth = maxSearchDepth
        self.player = player
    
    def evaluate(self, game: Kalah) -> float:
        """
        Evaluates the current game state for the current player.

        :param game: The current game state.
        :return: The score of the current game state.
        """

        upperScore = game.getScore(Player.UPPER)
        lowerScore = game.getScore(Player.LOWER)

        # Check if game is finished
        if game.isOver:
            if self.player == Player.UPPER and upperScore > lowerScore:
                return float('inf')
            elif self.player == Player.LOWER and lowerScore > upperScore:
                return float('inf')
            elif upperScore == lowerScore:
                return 0
            else:
                return float('-inf')

        # Calculate score
        if self.player == Player.UPPER:
            return upperScore - lowerScore
        else:
            return lowerScore - upperScore

    def getMove(self, game: Kalah) -> int:
        """
        Searches for the best move for the current player
        using the minimax algorithm with alpha-beta pruning.

        :param game: The current game state.
        :return: The best move for the current player.
        """

        # Check if game is finished
        if game.isOver:
            raise ValueError('Game is already over')

        moves = game.getValidMoves()
        bestScore = float('-inf')
        bestMove = moves[0]
        for move in moves:
            score = self.minimax(game, move, self.maxSearchDepth - 1, float('-inf'), float('inf'), False, [])
            if score > bestScore:
                bestScore = score
                bestMove = move

        print(f'AI for {self.player} chose pit {bestMove} with score {bestScore}')
        return bestMove
    
    def minimax(self, game: Kalah, move: int, depth: int, alpha: float, beta: float, maximizingPlayer: bool, moveHistory: list[int]) -> float:
        """
        Searches for the best move for the current player in the
        game tree using the minimax algorithm with alpha-beta pruning.

        :param game: The current game state.
        :param move: The move to be evaluated.
        :param depth: The current depth of the search tree.
        :param alpha: The alpha value of the alpha-beta pruning.
        :param beta: The beta value of the alpha-beta pruning.
        :param maximizingPlayer: True if the current player is the maximizing player, False otherwise.
        :param moveHistory: The history of moves made to reach the current game state.
        :return: The score of the current game state.
        """
        
        # Make move
        gameCopy = game.copy()
        prevPlayer = gameCopy.currentPlayer
        gameCopy.playPit(move)
        playerStays = gameCopy.currentPlayer == prevPlayer
        moveHistory += [move]

        if gameCopy.isOver or depth == 0:
            value = self.evaluate(gameCopy)
            if DEBUG_SEARCH_TREE:
                    print(f'Leave node: {value:4} | {moveHistory}')
            return value

        # Perform minimax
        if maximizingPlayer:
            value = float('-inf')
            for move in gameCopy.getValidMoves():
                value = max(value, self.minimax(gameCopy, move, depth - 1, alpha, beta, playerStays, moveHistory.copy()))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
                if DEBUG_SEARCH_TREE:
                    print(f'Inner node: {value:4} | {moveHistory}')
            return value
        
        else:
            value = float('inf')
            for move in gameCopy.getValidMoves():
                value = min(value, self.minimax(gameCopy, move, depth - 1, alpha, beta, not playerStays, moveHistory.copy()))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            if DEBUG_SEARCH_TREE:
                print(f'Inner node: {value:4} | {moveHistory}')
            return value
    