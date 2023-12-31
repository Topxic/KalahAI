from game import Kalah, Player
from config import *


class KalahAI:
    def __init__(self, maxSearchDepth, player: Player):
        if maxSearchDepth < 1:
            raise ValueError('maxSearchDepth must be at least 1')
        self.maxSearchDepth = maxSearchDepth
        self.player = player
    
    def evaluate(self, game: Kalah, maximizingPlayer: Player) -> float:
        """
        Evaluates the current game state for the current player.

        :param game: The current game state.
        :param maximizingPlayer: Player that is trying to maximize his move.
        :return: The score of the current game state.
        """

        upperScore = game.getScore(Player.UPPER)
        lowerScore = game.getScore(Player.LOWER)

        score = 0

        # Check if game is finished
        if game.isOver:
            if maximizingPlayer == Player.UPPER and upperScore > lowerScore:
                score = 1000 # return float('inf')
            elif maximizingPlayer == Player.LOWER and lowerScore > upperScore:
                score = 1000 # return float('inf')
            elif upperScore == lowerScore:
                score = 0
            else:
                score = -1000 # return float('-inf')

        # Calculate score
        if maximizingPlayer == Player.UPPER:
            score += upperScore - lowerScore
        else:
            score += lowerScore - upperScore
        return score

    def getMove(self, game: Kalah) -> int:
        """
        Searches for the best move for the current player.
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
            score = self.minimax(game, move, self.maxSearchDepth - 1, float('-inf'), float('inf'), game.currentPlayer, [])
            if score > bestScore:
                bestScore = score
                bestMove = move

        print(f'AI for {self.player} chose pit {bestMove} with score {bestScore}')
        return bestMove
    
    def minimax(self, game: Kalah, move: int, depth: int, alpha: float, beta: float, maximizingPlayer: Player, moveHistory: list[int]) -> float:
        """
        Searches for the best move for the current player in the
        game tree using the minimax algorithm with alpha-beta pruning.

        :param game: The current game state.
        :param move: The move to be evaluated.
        :param depth: The current depth of the search tree.
        :param alpha: The alpha value of the alpha-beta pruning.
        :param beta: The beta value of the alpha-beta pruning.
        :param maximizingPlayer: Player that is trying to maximize his move.
        :param moveHistory: The history of moves made to reach the current game state.
        :return: The score of the current game state.
        """
        
        # Make move
        gameCopy = game.copy()
        gameCopy.playPit(move)
        moveHistory += [move]

        if gameCopy.isOver or depth == 0:
            value = self.evaluate(gameCopy, maximizingPlayer)
            if DEBUG_SEARCH_TREE and self.maxSearchDepth - depth <= DEBUG_DEPTH:
                print(f'Leave node | {"MAX" if not maximizingPlayer else "MIN"} | {value:4} | {moveHistory}')
            return value

        # Perform minimax
        if gameCopy.currentPlayer == maximizingPlayer:
            value = float('-inf')
            for move in gameCopy.getValidMoves():
                value = max(value, self.minimax(gameCopy, move, depth - 1, alpha, beta, maximizingPlayer, moveHistory.copy()))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            if DEBUG_SEARCH_TREE and self.maxSearchDepth - depth <= DEBUG_DEPTH:
                print(f'Inner node | {"MAX" if not maximizingPlayer else "MIN"} | {value:4} | {moveHistory}')
            return value
        
        else:
            value = float('inf')
            for move in gameCopy.getValidMoves():
                value = min(value, self.minimax(gameCopy, move, depth - 1, alpha, beta, maximizingPlayer, moveHistory.copy()))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            if DEBUG_SEARCH_TREE and self.maxSearchDepth - depth <= DEBUG_DEPTH:
                print(f'Inner node | {"MAX" if not maximizingPlayer else "MIN"} | {value:4} | {moveHistory}')
            return value
    