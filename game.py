class Board:
    def __init__(self, pitsPerPlayer: int):
        """
        Initialize the board with the given number of pits per player.
        The index of the board begins in the bottom left corner and increments counter-clockwise.

        :param pitsPerPlayer: The number of pits per player.
        """

        self.pitsPerPlayer = pitsPerPlayer
        self.pits = ([4] * pitsPerPlayer + [0]) * 2
        self.gameOver = False;

    def pick(self, pit: int, isUpperPlayer: bool) -> bool:
        """
        Pick the seeds of the given pit and distribute them counter-clockwise.

        :param pit: Index of the pit to pick.
        :return: True if the player gets another turn, False otherwise.
        """

        # Check if game is over
        if self.gameOver:
            raise ValueError('Game is over.')

        # Check if pit is valid
        if 0 > pit or pit >= self.pitsPerPlayer:
            raise ValueError('Invalid pit index.')

        # Offset index to skip store and offset if lower player
        if isUpperPlayer:
            pit += self.pitsPerPlayer + 1

        if self.pits[pit] == 0:
            raise ValueError('Pit is empty.')

        lowerStoreIdx = self.pitsPerPlayer
        upperStoreIdx = 2 * self.pitsPerPlayer + 1

        # Keep placing seeds counter-clockwise
        seeds = self.pits[pit]
        self.pits[pit] = 0
        while seeds > 0:
            pit = (pit + 1) % len(self.pits)

            # If the last seed falls into a empty pit on the player's side, 
            # the player captures this seed and all seeds in the opposite pit (the other player’s pit) and puts them in his store.
            if seeds == 1 and self.pits[pit] == 0 and pit != lowerStoreIdx and pit != upperStoreIdx:
                if isUpperPlayer:
                    self.pits[upperStoreIdx] += 1 + self.pits[2 * self.pitsPerPlayer - pit + 1]
                else:
                    self.pits[lowerStoreIdx] += 1 + self.pits[2 * self.pitsPerPlayer - pit + 1]
                self.pits[2 * self.pitsPerPlayer - pit + 1] = 0
            else:
                self.pits[pit] += 1
            seeds -= 1

        # Game finishes if one player has no seeds left
        self.gameOver = sum(self.pits[:self.pitsPerPlayer]) == 0 or sum(self.pits[self.pitsPerPlayer + 1:2 * self.pitsPerPlayer + 1]) == 0

        # Opposite player collects all remaining seeds on his side
        if self.gameOver:
            self.pits[lowerStoreIdx] += sum(self.pits[:self.pitsPerPlayer])
            self.pits[upperStoreIdx] += sum(self.pits[self.pitsPerPlayer + 1:2 * self.pitsPerPlayer + 1])
            self.pits[:self.pitsPerPlayer] = [0] * self.pitsPerPlayer
            self.pits[self.pitsPerPlayer + 1:2 * self.pitsPerPlayer + 1] = [0] * self.pitsPerPlayer

        # Player gets another turn if last seed was placed in his store
        return (not isUpperPlayer and pit == self.pitsPerPlayer) or (isUpperPlayer and pit == 2 * self.pitsPerPlayer + 1)
    
    def print(self):
        print(f'Upper Player: {self.pits[self.pitsPerPlayer + 1:][::-1]}')
        print(f'Lower Player: {self.pits[:self.pitsPerPlayer + 1]}\n')

    def getScore(self):
        return self.pits[self.pitsPerPlayer], self.pits[2 * self.pitsPerPlayer + 1]


board = Board(6)
i = 0
while not board.gameOver:
    board.print()
    player = 'Upper' if i % 2 == 0 else 'Lower'
    pit = int(input(f'{player} player pick a pit: '))
    repeat = board.pick(pit, i % 2 == 0)
    if not repeat:
        i += 1
board.print()
score = board.getScore()
print(f'Upper player {score[1]}')
print(f'Lower player {score[0]}')
