import random
import pygame
from Images import Tile, eTileType, SpriteFactory
from time import sleep, time


class Board:
    def __init__(self, boardSize, tileSize, spacing, pooCount):
        self.Spacing = spacing
        self.BoardSize = boardSize
        self.Tiles = self.CreateBoard(self.BoardSize, tileSize)
        self.PooCount = pooCount
        self.generatePoos()
        self.setCats()
        self.gameover = False

    def Draw(self):
        for tiles in self.Tiles:
            display.blit(tiles.GetImage(), (tiles.X, tiles.Y))

    def CreateBoard(self, boardSize, tileSize):
        tiles = []
        for col in range(0, boardSize):
            for row in range(0, boardSize):
                tile = Tile(row * tileSize + self.Spacing * row,
                            col * tileSize + self.Spacing * col,
                            tileSize,
                            eTileType.uncovered)
                tiles.append(tile)
        return tiles

    def crash(self):
        self.text = pygame.font.Font(None, 36).render("Game Over", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_x = display.get_width() / 2 - self.text_rect.width / 2
        self.text_y = display.get_height() / 2 - self.text_rect.height / 2
        display.blit(self.text, [self.text_x, self.text_y])
        self.gameover = True

        # print 'umarles ale jeszcze nie umiem Ci tego napisac'

    def showBlanks(self, tileId):
        neightbours = {k: v for k, v in self.getNeightbours(tileId).iteritems() if self.Tiles[v].isCovered}

        for x in neightbours:
            self.Tiles[neightbours[x]].isCovered = False
            if (self.Tiles[neightbours[x]].Type == eTileType.catNeutral):
                self.showBlanks(neightbours[x])

    def getClickedTile(self, mousePos):
        for tileId in range(0, self.Tiles.__len__(), 1):
            if (self.Tiles[tileId].isClicked(mousePos)):
                self.neightbours = self.getNeightbours(tileId)
                self.Tiles[tileId].isCovered = False

                if (self.Tiles[tileId].Type == 0):
                    print 'BLANK'
                    self.showBlanks(tileId)

                if (self.Tiles[tileId].Type == eTileType.poo):
                    print 'KUPA'
                    self.crash()

                if (self.Tiles[tileId].Type > 0):
                    print 'Kotel'

                return self.Tiles[tileId]

    def generatePoos(self):
        seq = random.sample(xrange(0, self.Tiles.__len__()), self.PooCount)
        for pooId in seq:
            self.Tiles[pooId].SetType(eTileType.poo)

    def setCats(self):
        for tileId in range(0, self.Tiles.__len__(), 1):
            catLevel = 0
            if (self.Tiles[tileId].Type == eTileType.poo):
                continue
            neightboursIds = self.getNeightbours(tileId)
            for id in neightboursIds.values():
                if (self.Tiles[id].Type == eTileType.poo):
                    catLevel += 1

            self.Tiles[tileId].SetType(catLevel)

    def getNeightbours(self, tileId):
        allNeightbours = {
            'upperLeft': tileId - self.BoardSize - 1,
            'upperMiddle': tileId - self.BoardSize,
            'upperRight': tileId - self.BoardSize + 1,
            'MiddleLeft': tileId - 1,
            'MiddleRight': tileId + 1,
            'lowerLeft': tileId + self.BoardSize - 1,
            'lowerMiddle': tileId + self.BoardSize,
            'lowerRight': tileId + self.BoardSize + 1
        }

        if (tileId <= self.BoardSize):
            allNeightbours['upperLeft'] = None
            allNeightbours['upperMiddle'] = None
            allNeightbours['upperRight'] = None

        if (tileId >= self.BoardSize ** 2 - self.BoardSize):
            allNeightbours['lowerLeft'] = None
            allNeightbours['lowerMiddle'] = None
            allNeightbours['lowerRight'] = None

        if (tileId % self.BoardSize == 0):
            allNeightbours['upperLeft'] = None
            allNeightbours['MiddleLeft'] = None
            allNeightbours['lowerLeft'] = None

        if (tileId % self.BoardSize == self.BoardSize - 1):
            allNeightbours['upperRight'] = None
            allNeightbours['MiddleRight'] = None
            allNeightbours['lowerRight'] = None

        return {k: v for k, v in allNeightbours.items() if v}


def main():
    pygame.init()
    tileSize = 30
    boardSize = 10
    pooCount = 10
    spacing = 2
    clock = pygame.time.Clock()
    global display
    display = pygame.display.set_mode([boardSize * (tileSize + spacing), boardSize * (tileSize + spacing)])
    board = Board(boardSize, tileSize, spacing, pooCount)
    running = True
    while running:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0):  # LEFT BUTTON
                if (board.gameover):
                    board = Board(boardSize, tileSize, spacing, pooCount)
                else:
                    board.getClickedTile(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (0, 0, 1):  # RIGHT BUTTON
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 1):  # RIGHT AND LEFT
                pass

        display.fill((0, 0, 0))
        if (board.gameover):
            board.crash()
        else:
            board.Draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
