import pygame, random
from math import *

WIDTH, HEIGHT = 600, 600
pygame.font.init() 
font = pygame.font.SysFont('arial', 16)

class WordPanel(object):
    panels = []
    lines = []
    NUM_WORDS = 50
    SHOW_HITBOXES = False
    DRAW_SPIRAL = False
    COLORS = [
        pygame.Color('#DE3745'), # red
        pygame.Color('#E3722F'), # orange
        pygame.Color('#679E5E'), # green
        pygame.Color('#0FC0BF'), # turquoise
        pygame.Color('#10E5DF') # cyan
    ]
    
    @classmethod
    def setFirstNWordPanels(cls, wordCounts):
        cls.panels = []
        for i, word in enumerate(sorted(wordCounts, key=wordCounts.get, reverse=True)):
            if i >= cls.NUM_WORDS: break
            x, y = WIDTH / 2, HEIGHT / 2
            spiralGen = cls.spiralGen(x, y)
            panel = WordPanel(x, y, word, wordCounts[word])
            while cls._checkIntersecting(panel):
                dx, dy = next(spiralGen)
                x += dx
                y += dy
                panel = WordPanel(x, y, word, wordCounts[word])
                cls.lines.append(((x-dx, y-dy), (x, y)))
            cls.panels.append(panel)
        
    # https://rosettacode.org/wiki/Archimedean_spiral#Python
    @staticmethod
    def spiralGen(cx, cy):
        spiralNum = 0
        NUM_INCR_PER_ROTATIONS = 36
        RADIUS = 0.5
        while True:
            t = spiralNum / (NUM_INCR_PER_ROTATIONS / 2) * pi
            dx = (1 + RADIUS * t) * cos(t)
            dy = (1 + RADIUS * t) * sin(t)
            yield dx, dy
            spiralNum += 1
            
    @classmethod
    def _checkIntersecting(cls, panel):
        for p in cls.panels:
            if p is panel: return False
            dx = abs(p.x - panel.x)
            dy = abs(p.y - panel.y)
            xIntercept = dx < (p.text.get_width() + panel.text.get_width()) / 2
            yIntercept = dy < (p.text.get_height() + panel.text.get_height()) / 2
            if xIntercept and yIntercept: return True
        return None
    
    @classmethod
    def drawAll(cls, window):
        for panel in cls.panels:
            panel.draw(window)
            if cls.SHOW_HITBOXES:
                panel.drawHitbox(window)
        
        if cls.DRAW_SPIRAL:
            for line in cls.lines:
                pygame.draw.line(window, 'black', line[0], line[1])
    
    def __init__(self, x, y, word, count):
        self.x, self.y = x, y
        self.word = word
        self.count = count
        self.fontSize = 12 + int(0.1 * self.count ** 1.5)
        font = pygame.font.SysFont('arial', self.fontSize)
        self.text = font.render(self.word, True, random.choice(self.COLORS))
    
    def draw(self, window):
        x = self.x - self.text.get_width() / 2
        y = self.y - self.text.get_height() / 2
        window.blit(self.text, (x, y))
        
    def drawHitbox(self, window):
        topLeft = (self.getLeft(), self.getTop())
        topRight = (self.getRight(), self.getTop())
        botLeft = (self.getLeft(), self.getBottom())
        botRight = (self.getRight(), self.getBottom())
        pygame.draw.line(window, 'red', topLeft, topRight)
        pygame.draw.line(window, 'red', topRight, botRight)
        pygame.draw.line(window, 'red', botRight, botLeft)
        pygame.draw.line(window, 'red', botLeft, topLeft)
        
    def getLeft(self): return self.x - self.text.get_width() / 2
    def getRight(self): return self.x + self.text.get_width() / 2
    def getTop(self): return self.y - self.text.get_height() / 2
    def getBottom(self): return self.y + self.text.get_height() / 2
