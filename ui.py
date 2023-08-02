import pygame
from pygame_button import Button

from ai import KalahAI
from config import *
from game import Kalah, Player

GAP_SIZE = 10
TEXT_PADDING = 30
BUTTON_COLOR = (111, 1, 1)
BUTTON_STYLE = {
    "hover_color": (162, 2, 2),
    "clicked_color": (212, 2, 2),
    "clicked_font_color": (0, 0, 0),
}

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
    def __init__(self, game: Kalah, ai1: KalahAI = None, ai2: KalahAI = None):
        self.game = game
        self.ai1 = ai1
        self.ai2 = ai2
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

        # Add new game button 
        y = GAP_SIZE + tileHeight + GAP_SIZE + tileHeight + GAP_SIZE
        self.button = Button(
            (GAP_SIZE, y, 100, 25), BUTTON_COLOR, 
            self.reset, text='Reset', **BUTTON_STYLE
        )

    def reset(self):
        self.game.reset()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.pitSpritesGroupe.draw(self.screen)

        # Draw active turn info
        if self.game.isOver:
            upper = self.game.getScore(Player.UPPER)
            lower = self.game.getScore(Player.LOWER)
            if lower < upper:
                info = 'Upper wins'
            elif lower > upper:
                info = 'Lower wins'
            else:
                info = 'Draw'
        else:
            info = 'Upper turn' if self.game.currentPlayer == Player.UPPER else 'Lower turn'

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

    def run(self):
        running = True
        lastClickedIdx = -1

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.button.check_event(event)

            clickedIdx = -1
            # AI-1 turn
            if self.ai1 is not None and not self.game.isOver and self.game.currentPlayer == self.ai1.player:
                clickedIdx = self.ai1.getMove(self.game)
            # AI-2 turn
            elif self.ai2 is not None and not self.game.isOver and self.game.currentPlayer == self.ai2.player:
                clickedIdx = self.ai2.getMove(self.game)
            # Check if user clicked on a pit
            else:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        for i in range(len(self.pitSprites)):
                            pit = self.pitSprites[i]
                            if not pit.isStore and pit.rect.collidepoint(event.pos):
                                clickedIdx = i
                                print(f'Player for {self.game.currentPlayer} chose pit {i}')
                                break

            # Play and mark selected pit
            if clickedIdx != -1 and not self.game.isOver:
                try:
                    self.game.playPit(clickedIdx)
                    self.pitSprites[lastClickedIdx].image = PIT_IMAGE
                    self.pitSprites[clickedIdx].image = HIGHLIGHTED_PIT_IMAGE
                    lastClickedIdx = clickedIdx
                except Exception as e:
                    print(e)
                                          
            self.draw()
            self.button.update(self.screen)
            pygame.display.update()

        pygame.quit()
    

kalah = Kalah(SEEDS_PER_PIT, PITS_PER_PLAYER, Player.LOWER)
ai1 = KalahAI(AI_MAX_DEPTH, Player.UPPER)
ai2 = KalahAI(AI_MAX_DEPTH, Player.LOWER)
board = Board(kalah, ai1) # AI vs Human
# board = Board(kalah, ai1, ai2)  # AI vs AI
board.run()
