from bs4 import BeautifulSoup
import sys
import requests
import pygame
from WordPanel import WordPanel

# https://en.wikipedia.org/wiki/Valorant
# https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors

WIDTH, HEIGHT = 600, 600
FPS = 60

def getWordCounts():
    url = input('Enter wiki link: ')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    commonWords = getCommonWords()
    wordsToStrip = ' ,.:;\'"?![]\n\t(){}1234567890-_~`–&%'
    wordsDict = dict()

    tags = soup.find_all('p')
    for tag in tags:
        for word in tag.text.split(" "):
            word = word.strip(wordsToStrip).lower()
            if word not in commonWords and word != "":
                wordsDict[word] = wordsDict.get(word, 0) + 1

    return sortDict(wordsDict, reverse=True)

def getCommonWords():
    commonWords = set()
    with open('common words.txt', 'r') as f:
        for line in f:
            commonWords.add(line.strip())
    return commonWords 

def sortDict(D, *, reverse):
    return {k: v for k, v in sorted(D.items(), key=lambda item: item[1], reverse=reverse)}

def drawWindow(window):
    window.fill('white')
    WordPanel.drawAll(window)
    pygame.display.update()

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Webscraper')  
clock = pygame.time.Clock()
wordCounts = getWordCounts()
WordPanel.setFirstNWordPanels(wordCounts)

while True: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    drawWindow(window)