from enum import Enum


class Player(Enum):
    UPPER = 1
    LOWER = 2


class Kalah:
    def __init__(self, seedsPerPit: int, pitsPerPlayer: int, startingPlayer: Player):
        """
        Initialize the board with the given number of pits per player.
        The index of the board begins in the bottom left corner and increments counter-clockwise.

        :param pitsPerPlayer: The number of pits per player.
        """

        self.pitsPerPlayer = pitsPerPlayer
        self.seedsPerPit = seedsPerPit
        self.currentPlayer = startingPlayer
        self.pits = ([seedsPerPit] * pitsPerPlayer + [0]) * 2
        self.isOver = False
        self.lowerStoreIdx = pitsPerPlayer
        self.upperStoreIdx = 2 * pitsPerPlayer + 1

    def getPits(self, player: Player) -> list[int]:
        """
        Returns the pits of the given player.

        :param player: The player.
        :return: The pits of the given player.
        """

        if player == Player.UPPER:
            return self.pits[self.pitsPerPlayer + 1:self.upperStoreIdx]
        else:
            return self.pits[0:self.pitsPerPlayer]

    def playPit(self, pit: int) -> bool:
        """
        Pick the seeds of the given pit and distribute them counter-clockwise.
        Check for special cases:
        - If the last seed falls into a empty pit on the player's side, the player captures this seed and all seeds in the opposite pit (the other player's pit) and puts them in his store.
        - If the last seed falls into the player's store, the player gets another turn.

        :param pit: Index of the pit to pick.
        :return: True if the player gets another turn, False otherwise.
        """

        # Check if game is over
        if self.isOver:
            raise ValueError('Game is over.')

        # Check if pit is valid
        if 0 > pit or pit >= len(self.pits):
            raise ValueError(f'Pit {pit} index out of bounds.')

        # Pit is empty
        if self.pits[pit] == 0:
            raise ValueError(f'Pit {pit} is empty.')
                
        # Check if pit belongs to player
        upperPlayerConstraint = self.currentPlayer == Player.UPPER and pit > self.pitsPerPlayer
        lowerPlayerConstraint = self.currentPlayer == Player.LOWER and pit < self.pitsPerPlayer
        if not (upperPlayerConstraint or lowerPlayerConstraint):
            raise ValueError(f'Pit {pit} does not belong to {self.currentPlayer}.')

        # Keep placing seeds counter-clockwise
        seeds = self.pits[pit]
        self.pits[pit] = 0
        while seeds > 0:
            pit = (pit + 1) % len(self.pits)

            # If the last seed falls into a empty pit on the player's side,
            # the player captures this seed and all seeds in the opposite pit (the other player’s pit) and puts them in his store.
            lastSeed = seeds == 1 and self.pits[pit] == 0
            isStore = pit == self.lowerStoreIdx or pit == self.upperStoreIdx
            pitIsOnPlayerSide = (self.currentPlayer == Player.UPPER and pit > self.pitsPerPlayer) or (self.currentPlayer == Player.LOWER and pit < self.pitsPerPlayer)

            if lastSeed and not isStore and pitIsOnPlayerSide:
                distanceToRightStore = abs(self.pitsPerPlayer - pit)

                if pit > self.pitsPerPlayer and self.pits[pit - 2 * distanceToRightStore] > 0:
                    self.pits[self.upperStoreIdx] += 1 + self.pits[pit - 2 * distanceToRightStore]
                    self.pits[pit - 2 * distanceToRightStore] = 0
                elif pit < self.pitsPerPlayer and self.pits[pit + 2 * distanceToRightStore] > 0:
                    self.pits[self.lowerStoreIdx] += 1 + self.pits[pit + 2 * distanceToRightStore]
                    self.pits[pit + 2 * distanceToRightStore] = 0
                else:
                    self.pits[pit] += 1
            else:
                self.pits[pit] += 1
            seeds -= 1

        # Game finishes if one player has no seeds left
        upperSeeds = sum(self.getPits(Player.UPPER))
        lowerSeeds = sum(self.getPits(Player.LOWER))
        self.isOver = lowerSeeds == 0 or upperSeeds == 0

        # Opposite player collects all remaining seeds on his side
        if self.isOver:
            self.pits[self.lowerStoreIdx] += upperSeeds
            self.pits[self.upperStoreIdx] += lowerSeeds
            self.pits[:self.pitsPerPlayer] = [0] * self.pitsPerPlayer
            self.pits[self.pitsPerPlayer + 1:2 * self.pitsPerPlayer + 1] = [0] * self.pitsPerPlayer

        # Player gets another turn if last seed was placed in his store
        repeat = (pit == self.upperStoreIdx and self.currentPlayer == Player.UPPER) or (pit == self.lowerStoreIdx and self.currentPlayer == Player.LOWER)
        if not repeat:
            self.currentPlayer = Player.UPPER if self.currentPlayer == Player.LOWER else Player.LOWER

    def getScore(self, player: Player) -> int:
        """
        Get the score of the lower and upper player.

        :return: The score of the lower and upper player.
        """
        if player == Player.LOWER:
            return self.pits[self.lowerStoreIdx]
        else:
            return self.pits[self.upperStoreIdx]
        
    def getValidMoves(self) -> list[int]:
        """
        Get all valid moves for the current player.

        :return: A list of valid moves.
        """
        if self.isOver:
            return []

        if self.currentPlayer == Player.UPPER:
            return [i for i in range(self.pitsPerPlayer + 1, self.upperStoreIdx) if self.pits[i] > 0]
        else:
            return [i for i in range(0, self.pitsPerPlayer) if self.pits[i] > 0]

    def copy(self):
        obj = Kalah(self.seedsPerPit, self.pitsPerPlayer)
        obj.isOver = self.isOver
        obj.pits = self.pits.copy()
        obj.currentPlayer = self.currentPlayer
        return obj
