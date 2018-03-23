import pygame
import sys

import itertools

from board import Board

bg_color = (200, 200, 200)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

board = Board(10, 10, 10)

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 550))

basicfont = pygame.font.SysFont(None, 42)

digits = [
    basicfont.render('0', True, (20, 20, 20)),
    basicfont.render('1', True, (200, 0, 0)),
    basicfont.render('2', True, (0, 0, 200)),
    basicfont.render('3', True, (0, 150, 0)),
    basicfont.render('4', True, (155, 155, 0)),
    basicfont.render('5', True, (155, 0, 155)),
    basicfont.render('6', True, (0, 155, 155)),
    basicfont.render('7', True, (255, 0, 0)),
    basicfont.render('8', True, (0, 255, 0)),
    basicfont.render('9', True, (0, 0, 255)),
    basicfont.render(' ', True, (150, 150, 150))
]


def draw_digit(d=0, pos=(0, 0)):
    text = digits[d].get_rect()
    text.centerx, text.centery = pos[0], pos[1]

    screen.blit(digits[d], text)


def draw_screen():
    # Draw the score
    pygame.draw.rect(screen, white, (0, 0, 500, 50), 0)
    pygame.draw.rect(screen, black, (0, 0, 500, 50), 1)

    score_text_bg = white
    if board.game_won():
        score_text_bg = green
    if board.any_mines_revealed():
        score_text_bg = red

    score_text = basicfont.render('Score: {}'.format(board.score()), True, black, score_text_bg)
    score_text_rect = score_text.get_rect()
    score_text_rect.centery = 25
    score_text_rect.centerx = 250
    screen.blit(score_text, score_text_rect)

    # Draw the Board
    for i, j in itertools.product(range(board.height), range(board.width)):
        x = 50 * i
        y = 50 * j + 50
        if board.any_mines_revealed() and board.mines[i, j]:
            pygame.draw.rect(screen, red, (x, y, 50, 50), 0)

        if board.game_won() and board.mines[i, j]:
            pygame.draw.rect(screen, green, (x, y, 50, 50), 0)

        if not board.mines[i, j]:
            draw_digit(int(board.view[i, j]), (x + 25, y + 25))

        pygame.draw.rect(screen, black, (x, y, 50, 50), 1)


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            i, j = int(mx / 50), int((my - 50) / 50)

            board.reveal(i, j)

    screen.fill(bg_color)
    draw_screen()

    pygame.display.update()

