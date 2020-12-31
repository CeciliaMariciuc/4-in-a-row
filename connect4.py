import random

import numpy as np
import pygame
import sys

PLAYER1 = 0
PLAYER2 = 1
COMPUTER = 1
SQUARE_SIZE = 60
SQUARE_COLOR = (0, 0, 153)
BLACK = (0, 0, 0)
EMPTY_SQUARE = (255, 255, 255)
PLAYER1_SQUARE = (255, 255, 26)
PLAYER2_SQUARE = (255, 26, 26)
PIECE_RADIUS = (SQUARE_SIZE / 2 - 5)


def create_board(rows, cols):
    board = np.zeros((rows, cols))
    return board


def put_piece(board, piece, col, maxrows):
    clear_row = 0
    for row in range(maxrows):
        if board[row][col] == 0:
            clear_row = row
            break
    board[clear_row][col] = piece
    return clear_row


def valid_move(board, col, maxrows, maxcols):
    if col < 0 or col >= maxcols:
        return False
    return board[maxrows - 1][col] == 0


def check_winner(board, last_row, last_col, piece, maxrows, maxcols):
    # check row
    sequence_length = 0
    for col in range(maxcols):
        if board[last_row][col] == piece:
            sequence_length += 1
            if sequence_length == 4:
                return piece
        else:
            sequence_length = 0
    # check col
    sequence_length = 0
    for row in range(maxrows):
        if board[row][last_col] == piece:
            sequence_length += 1
            if sequence_length == 4:
                return piece
        else:
            sequence_length = 0
    # check principal diagonal
    row = last_row
    col = last_col
    sequence_length = 0
    while row < maxrows and col < maxcols and board[row][col] == piece:
        row += 1
        col += 1
        sequence_length += 1

    row = last_row
    col = last_col
    while row >= 0 and col >= 0 and board[row][col] == piece:
        row -= 1
        col -= 1
        sequence_length += 1
    sequence_length -= 1

    if sequence_length >= 4:
        return piece
    # check secondary diagonal
    row = last_row
    col = last_col
    sequence_length = 0
    while row >= 0 and col < maxrows and board[row][col] == piece:
        row -= 1
        col += 1
        sequence_length += 1

    row = last_row
    col = last_col
    while row < maxrows and col >= 0 and board[row][col] == piece:
        row += 1
        col -= 1
        sequence_length += 1
    sequence_length -= 1
    if sequence_length >= 4:
        return piece
    return -1


def piece_color(piece):
    if piece == 0:
        return EMPTY_SQUARE
    elif piece == 1:
        return PLAYER1_SQUARE
    elif piece == 2:
        return PLAYER2_SQUARE
    return BLACK


def draw_board(screen, board, maxrows, maxcols):
    for col in range(maxcols):
        for row in range(maxrows):
            pygame.draw.rect(screen, SQUARE_COLOR,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, piece_color(board[row][col]),
                               (col * SQUARE_SIZE + int(SQUARE_SIZE / 2),
                                row * SQUARE_SIZE + SQUARE_SIZE + int(SQUARE_SIZE / 2)),
                               PIECE_RADIUS)

    pygame.display.update()


def run_game_pvp(maxrows, maxcols):
    pygame.init()
    font_won = pygame.font.SysFont('Arial', 30)
    font_info = pygame.font.SysFont('Arial', 20)
    screen_size = (maxcols * SQUARE_SIZE, (maxrows + 1) * SQUARE_SIZE)
    screen = pygame.display.set_mode(screen_size)

    game_over = False
    current_board = create_board(maxrows, maxcols)
    draw_board(screen, current_board, maxrows, maxcols)
    player_turn = PLAYER1
    print(np.flip(current_board, 0))
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x_axis = event.pos[0]
                pygame.draw.rect(screen, BLACK, (0, 0, maxcols * SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(screen, piece_color(player_turn + 1), (x_axis, int(SQUARE_SIZE / 2)), PIECE_RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, maxcols * SQUARE_SIZE, SQUARE_SIZE))
                if player_turn == PLAYER1:
                    piece = PLAYER1 + 1
                else:
                    piece = PLAYER2 + 1
                move = int(event.pos[0] / SQUARE_SIZE)

                if valid_move(current_board, move, maxrows, maxcols):
                    row = put_piece(current_board, piece, move, maxrows)
                    player_turn = 1 - player_turn

                    if check_winner(current_board, row, move, piece, maxrows, maxcols) == piece:
                        message = font_won.render("Player " + str(piece) + " won!", True, piece_color(piece))
                        screen.blit(message, (40, 10))
                        print("Player " + str(piece) + " won!")
                        game_over = True
                else:
                    message = font_info.render("The move is not valid! Please try again!", True, piece_color(piece))
                    screen.blit(message, (40, 10))
                    print("The move is not valid! Please try again!")
                print(np.flip(current_board, 0))
                draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)

                if game_over:
                    pygame.time.wait(2000)


def level1_computer(board, maxrows, maxcols):
    valid_col = False
    move = 0
    while not valid_col:
        move = random.randint(0, maxcols - 1)
        valid_col = valid_move(board, move, maxrows, maxcols)
    return move


def get_first_turn(first_player):
    if first_player == "computer":
        return COMPUTER
    else:
        return PLAYER1


def run_game_pvc(maxrows, maxcols, first_player):
    pygame.init()
    font_won = pygame.font.SysFont('Arial', 30)
    font_info = pygame.font.SysFont('Arial', 20)
    screen_size = (maxcols * SQUARE_SIZE, (maxrows + 1) * SQUARE_SIZE)
    screen = pygame.display.set_mode(screen_size)

    game_over = False
    current_board = create_board(maxrows, maxcols)
    draw_board(screen, current_board, maxrows, maxcols)
    player_turn = get_first_turn(first_player)
    print(np.flip(current_board, 0))
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x_axis = event.pos[0]
                pygame.draw.rect(screen, BLACK, (0, 0, maxcols * SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(screen, piece_color(player_turn + 1), (x_axis, int(SQUARE_SIZE / 2)), PIECE_RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, maxcols * SQUARE_SIZE, SQUARE_SIZE))
                if player_turn == PLAYER1:
                    piece = PLAYER1 + 1
                else:
                    break
                move = int(event.pos[0] / SQUARE_SIZE)

                if valid_move(current_board, move, maxrows, maxcols):
                    row = put_piece(current_board, piece, move, maxrows)
                    player_turn = 1 - player_turn

                    if check_winner(current_board, row, move, piece, maxrows, maxcols) == piece:
                        message = font_won.render("You won!", True, piece_color(piece))
                        screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 30))
                        print("You won!")
                        game_over = True
                else:
                    message = font_info.render("The move is not valid! Please try again!", True, piece_color(piece))
                    screen.blit(message, (5, SQUARE_SIZE / 2 - 20))
                    print("The move is not valid! Please try again!")
                print(np.flip(current_board, 0))
                draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)

                if game_over:
                    pygame.time.wait(2000)
                    sys.exit()
        if player_turn == COMPUTER:
            move = level1_computer(current_board, maxrows, maxcols)
            piece = COMPUTER + 1
            row = put_piece(current_board, piece, move, maxrows)
            player_turn = 1 - player_turn

            if check_winner(current_board, row, move, COMPUTER + 1, maxrows, maxcols) == piece:
                message = font_won.render("Computer won!", True, piece_color(piece))
                screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 30))
                print("Computer won!")
                game_over = True
            print(np.flip(current_board, 0))
            pygame.time.wait(1000)
            draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)
            if game_over:
                pygame.time.wait(2000)


# run_game_pvp(6, 6)
run_game_pvc(6, 6, "computer")
