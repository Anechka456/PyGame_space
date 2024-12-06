import pygame
import sys
import random
from pygame.locals import *

width_of_board = 4
height_of_board = 4
block_size = 120
win_width = 800
win_height = 900
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
BASICFONTSIZE = 18
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
            message, MESSAGECOLOR, BGCOLOR, 5, 5)
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
    background_image = pygame.image.load('images/background_space.jpg')
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


def sliding_animation(board, direction, message, animationSpeed):
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

    for i in range(0, block_size, animationSpeed):
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


def generate_new_puzzle(numSlides):
    sequence = []
    board = start_playing()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None
    for i in range(numSlides):
        move = ramdom_moves(board, last_move)
        sliding_animation(board, move, 'Генерируется новый пазл...',
                          animationSpeed=int(block_size / 3))
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
                          animationSpeed=int(block_size / 2))
        take_turn(board, opp_moves)


def puzzle(sreen):
    global FPSCLOCK, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, IMAGES, DISPLAYSURF
    DISPLAYSURF = sreen
    pygame.init()
    original_images = [pygame.image.load(f'images/grigorievich/{i}.png') for i in range(1, 16)]
    IMAGES = [pygame.transform.scale(image, (block_size, block_size)) for image in original_images]
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Puzzles')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

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