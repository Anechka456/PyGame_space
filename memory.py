import pygame
from load_image import load_image
import random
import sys

IMAGE = None
LAST_OPEN = float('-inf')
MOVES = 12


class MemoryCard:
    def __init__(self, id_, size):
        self.id = id_
        self.image = pygame.transform.scale(load_image(f'memory/{id_}.jpg'), (size, size))
        self.open = False
        self.open_time = 0
        self.size = size

    def get_click(self):
        global IMAGE, LAST_OPEN, MOVES
        if not self.open:
            if IMAGE is None:
                IMAGE = self
            elif IMAGE != self:
                self.open = True
                IMAGE.open = True
                if self.id == IMAGE.id:
                    self.open_time = float('inf')
                    IMAGE.open_time = float('inf')
                else:
                    self.open_time = pygame.time.get_ticks()
                    IMAGE.open_time = pygame.time.get_ticks()
                    LAST_OPEN = pygame.time.get_ticks()
                    MOVES -= 1
                IMAGE = None

    def update(self):
        if pygame.time.get_ticks() - self.open_time >= 600:
            self.open = False

    def draw(self, screen, x, y):
        global IMAGE
        if IMAGE == self or self.open:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, (255, 204, 153), pygame.Rect(x, y, self.size, self.size), width=0)
        pygame.draw.rect(screen, (229, 81, 55), pygame.Rect(x, y, self.size, self.size), width=5)

    def __str__(self):
        return f'MemoryCard({self.id})'

    def __repr__(self):
        return f'MemoryCard({self.id})'


def memory(screen, n, top_text=''):
    global MOVES

    background_image = pygame.image.load('images/background_space.jpg')
    background_image = pygame.transform.scale(background_image, (830, 900))
    pygame.display.set_caption('Shifters')

    size2 = 800 // n
    size = int(size2 * 0.8)
    cards = []
    for i in range(n ** 2 // 2):
        cards.extend([MemoryCard(i, size) for _ in range(2)])
    random.shuffle(cards)

    board = [[] for _ in range(n)]
    for i, card in enumerate(cards):
        board[i // n].append(card)

    font = pygame.font.Font(None, 50)
    screen.blit(background_image, (0, 0))

    MOVES = int(n ** 2 * 0.75)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - LAST_OPEN >= 600:
                mx, my = event.pos
                mx, my = mx - 20, my - 110
                x, y = mx // size2, my // size2
                if mx >= 0 and my >= 0 and x < len(board[0]) and y < len(board) and mx % size2 <= size and my % size2 <= size:
                    board[y][x].get_click()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    running = False

        screen.blit(background_image, (0, 0))
        screen.blit(font.render(top_text, True, (255, 204, 153)), (40, 20))
        screen.blit(font.render(f'Осталось попыток: {MOVES}', True, (255, 204, 153)), (40, 60))
        for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j].update()
                board[i][j].draw(screen, (size2 // 7 + 5) + size2 * j, 110 + size2 * i)

        pygame.display.flip()
        clock.tick(60)

        if MOVES < 0:
            running = False
            memory(screen, n, 'Вы проиграли, попробуйте еще раз')
        elif all(map(lambda x: all(map(lambda y: y.open, x)), board)):
            running = False

