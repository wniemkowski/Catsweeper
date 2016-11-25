import random
import pygame
import time
from Images import Tile, eTileType


class Board:
    def __init__(self, boardSize, tileSize, spacing, pooCount):
        self.Spacing = spacing
        self.BoardSize = boardSize
        self.pointsBoardHeight = 50
        self.Tiles = self.CreateBoard(self.BoardSize, tileSize)
        self.PooCount = pooCount
        self.generatePoos()
        self.setCats()
        self.gameStart = time.time()
        self.gameover = False

    def Draw(self):
        for tiles in self.Tiles:
            display.blit(tiles.GetImage(), (tiles.X, tiles.Y))

    def DrawPoints(self):
        notMarkedPoos = self.PooCount - sum(1 for tile in self.Tiles if tile.isMarked)
        currTime = time.time() - self.gameStart
        text = pygame.font.Font(None, 36).render("poos: " + str(notMarkedPoos), True, (255, 255, 255))
        timeText = pygame.font.Font(None, 36).render("time: " + str(int(currTime)), True, (255, 255, 255))
        display.blit(text, [10,self.pointsBoardHeight/2 - 10])
        display.blit(timeText, [(20 + self.Spacing) * self.BoardSize, self.pointsBoardHeight/2 - 10])

    def CreateBoard(self, boardSize, tileSize):
        tiles = []
        for col in range(0, boardSize):
            for row in range(0, boardSize):
                tile = Tile(row * tileSize + self.Spacing * row,
                            col * tileSize + self.Spacing * col + self.pointsBoardHeight,
                            tileSize,
                            eTileType.uncovered)
                tiles.append(tile)
        return tiles

    def crash(self):
        text = pygame.font.Font(None, 36).render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_x = display.get_width() / 2 - text_rect.width / 2
        text_y = display.get_height() / 2 - text_rect.height / 2
        display.blit(text, [text_x, text_y])
        self.gameover = True

    def showBlanks(self, tileId):
        neightbours = {k: v for k, v in self.getNeightbours(tileId).iteritems() if self.Tiles[v].isCovered}

        for x in neightbours:
            self.Tiles[neightbours[x]].isCovered = False
            if (self.Tiles[neightbours[x]].Type == eTileType.catNeutral):
                self.showBlanks(neightbours[x])

    def getClickedTile(self, mousePos):
        for tileId in range(0, self.Tiles.__len__(), 1):
            if (self.Tiles[tileId].isClicked(mousePos)):

                if (self.Tiles[tileId].isMarked or not self.Tiles[tileId].isCovered):
                    continue

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

    def MarkTile(self, mousePos):
        for tileId in range(0, self.Tiles.__len__(), 1):
            if (self.Tiles[tileId].isClicked(mousePos) and self.Tiles[tileId].isCovered == True):
                self.Tiles[tileId].setMarked(not self.Tiles[tileId].isMarked)

def main():
    pygame.init()
    tileSize = 30
    boardSize = 10
    pooCount = 10
    spacing = 2
    clock = pygame.time.Clock()
    global display
    display = pygame.display.set_mode([boardSize * (tileSize + spacing), boardSize * (tileSize + spacing) + 50])
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
                board.MarkTile(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 1):  # RIGHT AND LEFT
                pass

        display.fill((0, 0, 0))
        if (board.gameover):
            board.crash()
        else:
            board.Draw()
            board.DrawPoints()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
