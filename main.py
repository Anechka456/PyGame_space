import pygame
import memory
import puzzle1
import puzzle2
import puzzle3
import card

# Инициализация Pygame
pygame.init()
size = width, height = 830, 900
screen = pygame.display.set_mode(size)

# Цикл обработки событий
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    memory.memory(screen, 2)
    card.show_card(screen, 'data/cards/1.json')
    puzzle1.puzzle(screen)
    card.show_card(screen, 'data/cards/6.json')

    memory.memory(screen, 4)
    card.show_card(screen, 'data/cards/2.json')
    puzzle2.puzzle(screen)
    card.show_card(screen, 'data/cards/4.json')

    memory.memory(screen, 6)
    card.show_card(screen, 'data/cards/3.json')
    puzzle3.puzzle(screen)
    card.show_card(screen, 'data/cards/5.json')

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
