import pygame
import json
from load_image import load_image
import sys


class Card:
    def __init__(self, path):
        with open(path, 'r', encoding='utf8') as f:
            data = json.load(f)
        self.name = data["name"]
        self.description = data["description"]
        self.image = pygame.transform.scale(load_image(f'card_images/{data["image"]}'), (560, 560))

    def draw(self, screen):
        screen.blit(pygame.font.Font(None, 60).render(self.name, True, (139, 0, 255)), (20, 20))
        s, c = [], 0
        cs = 0
        for i in self.description.split():
            s.append(i)
            c += len(i)
            if c >= 30:
                screen.blit(pygame.font.Font(None, 40).render(' '.join(s), True, (102, 0, 255)), (20, 80 + cs * 30))
                s, c = [], 0
                cs += 1
        screen.blit(self.image, (20, 320))


def show_card(screen, path):
    background_image = pygame.image.load('images/background_space.jpg')
    background_image = pygame.transform.scale(background_image, (830, 900))
    card = Card(path)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        screen.blit(background_image, (0, 0))
        card.draw(screen)

        pygame.display.flip()
        clock.tick(60)
