import json
import os
import random
import sys

import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()
size = width, height = 830, 900
win_width = 800
win_height = 900
screen = pygame.display.set_mode(size)
running = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class StartWindow:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((size[0], size[1]))
        pygame.display.set_caption("Space puzzles")
        icon = pygame.image.load("data/icon.png")
        pygame.display.set_icon(icon)
        self.font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(300, 300, 200, 100)
        self.author_text = "Автор: Максимова Анна"
        self.coauthor_text = "Соавторы: Фирсов Дмитрий и Филипов Кирилл"
        self.title_game = "Space puzzles"

    def draw(self):
        background_image = pygame.image.load('data/background_space.jpg')
        background_image = pygame.transform.scale(background_image, (830, 900))
        self.screen.blit(background_image, (0, 0))

        # Рисуем овальный фон вокруг кнопки
        pygame.draw.ellipse(self.screen, (0, 0, 150), self.start_button.inflate(40, 40))
        pygame.draw.ellipse(self.screen, (0, 0, 200), self.start_button.inflate(20, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 255), self.start_button.inflate(0, 0))
        button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
        self.screen.blit(button_text, (self.start_button.x, self.start_button.y + 30))

        # Отображаем текст
        author_surface = self.font.render(self.author_text, True, (0, 0, 0))
        coauthor_surface = self.font.render(self.coauthor_text, True, (0, 0, 0))
        title_game = pygame.font.Font(None, 74).render(self.title_game, True, (255, 255, 255))

        self.screen.blit(title_game, (230, 100))
        self.screen.blit(author_surface, (30, 800))
        self.screen.blit(coauthor_surface, (30, 850))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button.collidepoint(event.pos):
                            running = False

            self.draw()


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
    background_image = pygame.image.load('data/background_space.jpg')
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

    background_image = pygame.image.load('data/background_space.jpg')
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
                if mx >= 0 and my >= 0 and x < len(board[0]) and y < len(
                        board) and mx % size2 <= size and my % size2 <= size:
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


def check_exit_req():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        pygame.event.post(event)


def start_playing():
    counter = 1
    board = []
    for x in range(width_of_board):
        column = []
        for y in range(height_of_board):
            column.append(counter)
            counter += width_of_board
        board.append(column)
        counter -= width_of_board * (height_of_board - 1) + width_of_board - 1

    board[width_of_board - 1][height_of_board - 1] = BLANK
    return board


def get_blank_position(board):
    for x in range(width_of_board):
        for y in range(height_of_board):
            if board[x][y] == BLANK:
                return (x, y)


def take_turn(board, move):
    blankx, blanky = get_blank_position(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def is_valid_move(board, move):
    blankx, blanky = get_blank_position(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
        (move == DOWN and blanky != 0) or \
        (move == LEFT and blankx != len(board) - 1) or \
        (move == RIGHT and blankx != 0)


def ramdom_moves(board, last_move=None):
    valid_moves = [UP, DOWN, LEFT, RIGHT]

    if last_move == UP or not is_valid_move(board, DOWN):
        valid_moves.remove(DOWN)
    if last_move == DOWN or not is_valid_move(board, UP):
        valid_moves.remove(UP)
    if last_move == LEFT or not is_valid_move(board, RIGHT):
        valid_moves.remove(RIGHT)
    if last_move == RIGHT or not is_valid_move(board, LEFT):
        valid_moves.remove(LEFT)

    return random.choice(valid_moves)


def get_left_top_of_tile(block_x, block_y):
    left = XMARGIN + (block_x * block_size) + (block_x - 1)
    top = YMARGIN + (block_y * block_size) + (block_y - 1)
    return (left, top)


def get_spot_clicked(board, x, y):
    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            left, top = get_left_top_of_tile(block_x, block_y)
            tile_rect = pygame.Rect(left, top, block_size, block_size)
            if tile_rect.collidepoint(x, y):
                return (block_x, block_y)
    return (None, None)


def draw_board(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        text_renderign, text_in_rect = make_text(
            message, MESSAGECOLOR, BGCOLOR, 5, 5, size=18)
        DISPLAYSURF.blit(text_renderign, text_in_rect)

    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            if board[block_x][block_y]:
                draw_block(block_x, block_y, board[block_x][block_y])

    left, top = get_left_top_of_tile(0, 0)
    width = width_of_board * block_size
    height = height_of_board * block_size
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5,
                                                top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)


def draw_block(block_x, block_y, number, adjx=0, adjy=0):
    left, top = get_left_top_of_tile(block_x, block_y)
    DISPLAYSURF.blit(IMAGES[number - 1], (left + adjx, top + adjy))


def make_text(text, color, background_color, top, left, size=None):
    background_image = pygame.image.load('data/background_space.jpg')
    background_image = pygame.transform.scale(background_image, (830, 900))
    DISPLAYSURF.blit(background_image, (0, 0))
    if size is None:
        text_rendering = BASICFONT.render(text, True, color, background_color)
    else:
        font = pygame.font.Font('freesansbold.ttf', size)
        text_rendering = font.render(text, True, color, background_color)
    text_in_rect = text_rendering.get_rect()
    text_in_rect.topleft = (top, left)
    return (text_rendering, text_in_rect)


def sliding_animation(board, direction, message, animation_speed):
    blankx, blanky = get_blank_position(board)
    if direction == UP:
        move_in_xaxis = blankx
        move_in_yaxis = blanky + 1
    elif direction == DOWN:
        move_in_xaxis = blankx
        move_in_yaxis = blanky - 1
    elif direction == LEFT:
        move_in_xaxis = blankx + 1
        move_in_yaxis = blanky
    elif direction == RIGHT:
        move_in_xaxis = blankx - 1
        move_in_yaxis = blanky

    draw_board(board, message)
    base_surf = DISPLAYSURF.copy()
    take_left, take_top = get_left_top_of_tile(move_in_xaxis, move_in_yaxis)
    pygame.draw.rect(base_surf, BGCOLOR, (take_left,
                                          take_top, block_size, block_size))

    for i in range(0, block_size, animation_speed):
        check_exit_req()
        DISPLAYSURF.blit(base_surf, (0, 0))
        if direction == UP:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, -i)
        if direction == DOWN:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, i)
        if direction == LEFT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], -i, 0)
        if direction == RIGHT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_new_puzzle(num_slides):
    sequence = []
    board = start_playing()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None
    for i in range(num_slides):
        move = ramdom_moves(board, last_move)
        sliding_animation(board, move, 'Генерируется новый пазл...',
                          animation_speed=int(block_size / 3))
        take_turn(board, move)
        sequence.append(move)
        last_move = move
    return (board, sequence)


def rst_animation(board, all_moves):
    reverse_moves = all_moves[:]
    reverse_moves.reverse()

    for move in reverse_moves:
        if move == UP:
            opp_moves = DOWN
        elif move == DOWN:
            opp_moves = UP
        elif move == RIGHT:
            opp_moves = LEFT
        elif move == LEFT:
            opp_moves = RIGHT
        sliding_animation(board, opp_moves, '',
                          animation_speed=int(block_size / 2))
        take_turn(board, opp_moves)


def puzzle(screen, fio, number_image):
    global FPSCLOCK, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, IMAGES, DISPLAYSURF
    DISPLAYSURF = screen
    pygame.init()
    original_images = [pygame.image.load(f'images/{fio}/{i}.png') for i in range(1, number_image)]
    IMAGES = [pygame.transform.scale(image, (block_size, block_size)) for image in original_images]
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Puzzles')
    BASICFONT = pygame.font.Font('freesansbold.ttf', basicfontsize)

    RESET_SURF, RESET_RECT = make_text(
        'Сброс', TEXT, BGCOLOR, win_width - 130, win_height - 530, size=25)
    NEW_SURF, NEW_RECT = make_text(
        'Новая игра', TEXT, BGCOLOR, win_width - 130, win_height - 500, size=25)

    main_board, solution_seq = generate_new_puzzle(80)
    SOLVEDBOARD = start_playing()
    all_moves = []
    while True:
        slide_to = None
        msg = 'Щелкните по блоку или используйте клавиши со стрелками для перемещения блока.'
        if main_board == SOLVEDBOARD:
            msg = 'Решено!'
            draw_board(main_board, msg)
            pygame.display.update()
            break
        draw_board(main_board, msg)

        check_exit_req()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = get_spot_clicked(
                    main_board, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        rst_animation(main_board, all_moves)
                        all_moves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        main_board, solution_seq = generate_new_puzzle(80)
                        all_moves = []
                else:
                    blankx, blanky = get_blank_position(main_board)
                    if spotx == blankx + 1 and spoty == blanky:
                        slide_to = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slide_to = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slide_to = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and is_valid_move(main_board, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and is_valid_move(main_board, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and is_valid_move(main_board, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and is_valid_move(main_board, DOWN):
                    slide_to = DOWN

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    rst_animation(main_board, solution_seq + all_moves)
                    all_moves = []

        if slide_to:
            sliding_animation(
                main_board, slide_to, 'Щелкните по блоку или используйте клавиши '
                                      'со стрелками для перемещения блока.', 8)
            take_turn(main_board, slide_to)
            all_moves.append(slide_to)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def final_window():
    font = pygame.font.SysFont('Arial', 48)
    button_font = pygame.font.SysFont('Arial', 36)

    # Функция для отрисовки кнопки
    def draw_button(text, x, y, width, height, color):
        final_button = pygame.Rect(x, y, width, height)

        pygame.draw.ellipse(screen, (0, 0, 150), final_button.inflate(40, 40))
        pygame.draw.ellipse(screen, (0, 0, 200), final_button.inflate(20, 20))
        pygame.draw.ellipse(screen, (0, 0, 255), final_button.inflate(0, 0))

        text_surface = button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    while True:
        background_image = pygame.image.load('data/background_space.jpg')
        background_image = pygame.transform.scale(background_image, (830, 900))
        screen.blit(background_image, (0, 0))

        # Отрисовка заголовка
        title_surface = font.render('Игра окончена!', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(width // 2, height // 3))
        screen.blit(title_surface, title_rect)

        # Отрисовка кнопок
        draw_button('Рестарт', width // 4 - 50, height // 2, 150, 50, (0, 0, 255))
        draw_button('Выход', 3 * width // 4 - 50, height // 2, 150, 50, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Проверка нажатия кнопок
                if (width // 4 - 50 < mouse_x < width // 4 + 100 and
                        height // 2 < mouse_y < height // 2 + 50):
                    return True
                elif (3 * width // 4 - 50 < mouse_x < 3 * width // 4 + 100 and
                      height // 2 < mouse_y < height // 2 + 50):
                    return False

        pygame.display.flip()

width_of_board = 3
height_of_board = 3
block_size = 160
basicfontsize = 10

FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BGCOLOR = DARKTURQUOISE
TILECOLOR = BLUE
TEXTCOLOR = WHITE
BORDERCOLOR = RED
TEXT = GREEN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = BLUE

XMARGIN = int((win_width - (block_size * width_of_board + (width_of_board - 1))) / 2)
YMARGIN = int((win_height - (block_size * height_of_board + (height_of_board - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

StartWindow(size).run()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    memory(screen, 2)
    show_card(screen, 'data/cards/1.json')
    puzzle(screen, 'gagarin', 9)
    show_card(screen, 'data/cards/6.json')

    width_of_board = 4
    height_of_board = 4
    block_size = 120
    basicfontsize = 18

    memory(screen, 4)
    show_card(screen, 'data/cards/2.json')
    puzzle(screen, 'grigorievich', 16)
    show_card(screen, 'data/cards/4.json')

    width_of_board = 5
    height_of_board = 5
    block_size = 100
    basicfontsize = 18

    memory(screen, 6)
    show_card(screen, 'data/cards/3.json')
    puzzle(screen, 'mikhailovich', 25)
    show_card(screen, 'data/cards/5.json')

    if final_window():
        continue
    else:
        pygame.quit()
        sys.exit()
