import pygame
from ai import KalahAI

from game import Kalah

GAP_SIZE = 10
TEXT_PADDING = 30
PIT_IMAGE = pygame.image.load("assets/pit-60x60.png")
HIGHLIGHTED_PIT_IMAGE = pygame.image.load("assets/highlighted-pit-60x60.png")
STORE_IMAGE = pygame.image.load("assets/store-60x60.png")


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, isStore):
        super().__init__()
        self.image = image
        self.isStore = isStore
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, game: Kalah, ai: KalahAI=None):
        self.game = game
        self.ai = ai
        tileWidth = PIT_IMAGE.get_rect().width
        tileHeight = PIT_IMAGE.get_rect().height
        self.width = GAP_SIZE + (tileWidth + GAP_SIZE) * (game.pitsPerPlayer + 1) + tileWidth + GAP_SIZE
        self.height = GAP_SIZE + tileHeight + GAP_SIZE + tileHeight + GAP_SIZE + TEXT_PADDING

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Kalah')
        self.font = pygame.font.SysFont('Arial', 20)


        # Create sprites in order of the game layout
        self.pitSprites = []
        # Lower row of pits
        for col in range(game.pitsPerPlayer):
            x = GAP_SIZE + (col + 1) * (tileWidth + GAP_SIZE)
            y = GAP_SIZE + (tileHeight + GAP_SIZE)
            self.pitSprites.append(Tile(PIT_IMAGE, x, y, False))
        # Right store
        x = self.width - (GAP_SIZE + tileWidth)
        y = GAP_SIZE + tileHeight // 2 + GAP_SIZE // 2
        self.pitSprites.append(Tile(PIT_IMAGE, x, y, True))
        # Upper row of pits reverse order
        for col in range(game.pitsPerPlayer):
            x = self.width - ((col + 2) * (tileWidth + GAP_SIZE))
            y = GAP_SIZE
            self.pitSprites.append(Tile(PIT_IMAGE, x, y, False))
        # Left store
        x = GAP_SIZE
        y = GAP_SIZE + tileHeight // 2 + GAP_SIZE // 2
        self.pitSprites.append(Tile(PIT_IMAGE, x, y, True))
        self.pitSpritesGroupe = pygame.sprite.Group(self.pitSprites)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.pitSpritesGroupe.draw(self.screen)

        # Draw active turn info
        if self.game.gameOver:
            score = self.game.getScore()
            if score[1] > score[0]:
                info = 'Upper wins'
            elif score[1] < score[0]:
                info = 'Lower wins'
            else:
                info = 'Draw'
        else:
            info = 'Upper turn' if self.uppersTurn else 'Lower turn'

        text = self.font.render(info, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height - TEXT_PADDING // 2)
        self.screen.blit(text, textRect)

        # Draw seeds in each pit
        for i in range(len(self.game.pits)):
            pitSprite = self.pitSprites[i]
            x = pitSprite.rect.x + pitSprite.rect.width / 2
            y = pitSprite.rect.y + pitSprite.rect.height / 2
            seeds = self.game.pits[i]
            text = self.font.render(str(seeds), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (x, y)
            self.screen.blit(text, textRect)

    def run(self, upperStarts):
        self.uppersTurn = upperStarts
        running = True
        lastClickedIdx = -1
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            clickedIdx = -1
            if self.uppersTurn and self.ai is not None and not self.game.gameOver:
                clickedIdx = ai.getMove(self.game)
            else:            
                # Check if user clicked on a pit
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        for i in range(len(self.pitSprites)):
                            pit = self.pitSprites[i]
                            if not pit.isStore and pit.rect.collidepoint(event.pos):
                                clickedIdx = i
                                break
                # Discard invalid moves
                if self.uppersTurn and clickedIdx < self.game.pitsPerPlayer:
                    clickedIdx = -1
                if not self.uppersTurn and clickedIdx >= self.game.pitsPerPlayer + 1:
                    clickedIdx = -1

            # Perfom move and evaluate turn
            if clickedIdx != -1 and not self.game.gameOver:
                playerName = 'Upper' if self.uppersTurn else 'Lower'
                print(f'{playerName} player clicked pit {clickedIdx}')
                newTurn = self.game.pick(clickedIdx, self.uppersTurn)
                if not newTurn:
                    self.uppersTurn = not self.uppersTurn
                # Mark selected pit
                self.pitSprites[lastClickedIdx].image = PIT_IMAGE
                self.pitSprites[clickedIdx].image = HIGHLIGHTED_PIT_IMAGE
                lastClickedIdx = clickedIdx
                                     
            self.draw()

            pygame.display.update()

        pygame.quit()
    

kalah = Kalah(6)
ai = KalahAI(8, True)
board = Board(kalah, ai)  
board.run(False)
