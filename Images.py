import pygame
import sys, os
from enum import Enum

_image_library = {}


class Tile():
    def __init__(self, x, y, size, type):
        self.X = x
        self.Y = y
        self.Size = size
        self.Type = type
        sf = SpriteFactory()
        self.image = sf.Create(self.Type, size)
        self.isCovered = True
        self.isMarked = False

    def isClicked(self, mousePos):
        if (mousePos[0] > self.X and mousePos[0] < self.X + self.Size + 2):
            if (mousePos[1] > self.Y and mousePos[1] < self.Y + self.Size + 2):
                return True

    def GetImage(self):
        if(self.isCovered and not self.isMarked):
            return SpriteFactory().Create(eTileType.uncovered,self.Size)
        else:
            return self.image

    def SetType(self,eTileType):
        self.Type = eTileType
        self.image = SpriteFactory().Create(eTileType,self.Size)

    def setMarked(self, isMarked):
        self.isMarked = isMarked
        if(isMarked):
            self.image = SpriteFactory().Create(eTileType.marked, self.Size)
        else:
            self.image = SpriteFactory().Create(self.Type,self.Size)

class eTileType(Enum):
    catNeutral = 0
    cat1 = 1
    cat2 = 2
    cat3 = 3
    cat4 = 4
    cat5 = 5
    cat6 = 6
    cat7 = 7
    cat8 = 8
    poo = 9
    uncovered = 10
    marked = 11


class SpriteFactory:
    def Create(self, tileType, size):
        return {
            10: self.get_image("images\\paw.png", size),
            11: self.get_image("images\\marked.png", size),
            1: self.get_image("images\\1_very_small.jpg", size),
            2: self.get_image("images\\2_very_small.jpg", size),
            3: self.get_image("images\\3_very_small.jpg", size),
            4: self.get_image("images\\4_very_small.jpg", size),
            5: self.get_image("images\\5_very_small.jpg", size),
            6: self.get_image("images\\6_very_small.jpg", size),
            7: self.get_image("images\\7_very_small.jpg", size),
            8: self.get_image("images\\8_very_small.jpg", size),
            9: self.get_image("images\\kupa_very_small.png", size),
            0: self.get_image("images\\0.png", size)
        }[tileType]

    def get_image(sefl, path, size):
        global _image_library
        image = _image_library.get(path)
        if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            image = pygame.transform.scale(image, (size, size))
            _image_library[path] = image
        return image
