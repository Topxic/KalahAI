from game import Kalah


class KalahAI:
    def __init__(self, maxSearchDepth, isUpperPlayer):
        self.maxSearchDepth = maxSearchDepth
        self.isUpperPlayer = isUpperPlayer

    def getValidMoves(self, game: Kalah) -> list[int]:
        """
        Returns a list of valid moves for the current player.

        :param game: The current game state.
        :return: A list of valid moves for the current player.
        """

        validMoves = []
        for i in range(game.pitsPerPlayer):
            idx = i + game.pitsPerPlayer + 1 if self.isUpperPlayer else i
            if game.pits[idx] > 0:
                validMoves.append(idx)

        return validMoves

    def getMove(self, game: Kalah) -> int:
        """
        Searches for the best move for the current player
        using the minimax algorithm with alpha-beta pruning.

        :param game: The current game state.
        :return: The best move for the current player.
        """

        bestMove = None
        bestScore = float('-inf')
        for move in self.getValidMoves(game):
            score = self.minimax(game, move, self.maxSearchDepth, float('-inf'), float('inf'), True)
            if score > bestScore:
                bestMove = move
                bestScore = score

        # AI is losing in every searched move
        if bestMove is None:
            bestMove = self.getValidMoves(game)[0]

        return bestMove
    
    def evaluate(self, game: Kalah) -> float:
        """
        Evaluates the current game state for the current player.

        :param game: The current game state.
        :return: The score of the current game state.
        """

        # Check if game is finished
        if game.gameOver:
            score = game.getScore()
            if self.isUpperPlayer and score[1] > score[0]:
                return float('inf')
            elif not self.isUpperPlayer and score[1] < score[0]:
                return float('inf')
            elif self.isUpperPlayer and score[1] < score[0]:
                return float('-inf')
            elif not self.isUpperPlayer and score[1] > score[0]:
                return float('-inf')
            else:
                return 0

        # Calculate score
        lowerStoreIdx = game.pitsPerPlayer
        upperStoreIdx = 2 * game.pitsPerPlayer + 1
        if self.isUpperPlayer:
            score = game.pits[upperStoreIdx] - game.pits[lowerStoreIdx]
        else:
            score = game.pits[lowerStoreIdx] - game.pits[upperStoreIdx]
        return score
    
    def minimax(self, game: Kalah, move: int, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> float:
        """
        Searches for the best move for the current player
        using the minimax algorithm with alpha-beta pruning.

        :param game: The current game state.
        :param move: The move to be evaluated.
        :param depth: The current search depth.
        :param alpha: The current alpha value.
        :param beta: The current beta value.
        :param maximizingPlayer: True if the current player is the AI, False otherwise.
        :return: The score of the move.
        """

        # Copy state and perform move
        newGame = Kalah(game.pitsPerPlayer)
        newGame.pits = game.pits.copy()
        newGame.gameOver = game.gameOver
        newGame.pick(move, self.isUpperPlayer)

        # Evaluate game state
        if depth == 0 or newGame.gameOver:
            return self.evaluate(newGame)

        # Search for best move
        bestScore = float('-inf') if maximizingPlayer else float('inf')
        for move in self.getValidMoves(newGame):
            score = self.minimax(newGame, move, depth - 1, alpha, beta, not maximizingPlayer)
            if maximizingPlayer:
                bestScore = max(bestScore, score)
                if bestScore > beta:
                    break
                alpha = max(alpha, bestScore)
            else:
                bestScore = min(bestScore, score)
                if bestScore < alpha:
                    break
                beta = min(beta, bestScore)

        return bestScore
    