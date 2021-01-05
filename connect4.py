import math
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
INF = 10000000
ALFA = - math.inf
BETA = math.inf


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
    while row >= 0 and col < maxcols and board[row][col] == piece:
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


def run_game_pvp(maxrows, maxcols, first_player):
    pygame.init()
    font_won = pygame.font.SysFont('Arial', 30)
    font_info = pygame.font.SysFont('Arial', 20)
    screen_size = (maxcols * SQUARE_SIZE, (maxrows + 1) * SQUARE_SIZE)
    screen = pygame.display.set_mode(screen_size)

    game_over = False
    current_board = create_board(maxrows, maxcols)
    draw_board(screen, current_board, maxrows, maxcols)
    if first_player == "human1":
        player_turn = PLAYER1
    else:
        player_turn = PLAYER2
    message = font_won.render("First player is: " + first_player, True, piece_color(player_turn + 1))
    screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 20))
    pygame.display.update()

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
                        screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 20))
                        print("Player " + str(piece) + " won!")
                        game_over = True
                else:
                    message = font_info.render("The move is not valid! Try again!", True, piece_color(piece))
                    screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 10))
                    print("The move is not valid! Try again!")
                print(np.flip(current_board, 0))
                draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)

                if len(cols_available(current_board, maxrows, maxcols)) == 0:
                    game_over = True
                if game_over:
                    pygame.time.wait(2000)


def level1_computer(board, maxrows, maxcols):
    valid_col = False
    move = 0
    while not valid_col:
        move = random.randint(0, maxcols - 1)
        valid_col = valid_move(board, move, maxrows, maxcols)
    pygame.time.wait(1000)
    return move


def level2_computer(board, maxrows, maxcols, move_count):
    if move_count % 2 == 0:
        return level1_computer(board, maxrows, maxcols)
    else:
        pygame.time.wait(500)
        return minimax(board, 4, True, ALFA, BETA, maxrows, maxcols)[0]


def get_first_turn(first_player):
    if first_player == "computer":
        return COMPUTER
    else:
        return PLAYER1


def score_sequence(sequence, player_piece, left_edge, right_edge):
    count_pieces = sequence.count(player_piece)
    if player_piece == 1:
        opponent_piece = 2
    else:
        opponent_piece = 1

    if count_pieces == 4:
        return INF
    if count_pieces == 3:
        if opponent_piece in sequence[1:3]:
            if left_edge is True or right_edge is True:
                count_pieces -= 2
            else:
                count_pieces -= 1
        else:
            count_pieces += 4
        return count_pieces ** 3
    if count_pieces == 2 or count_pieces == 1:
        count_pieces -= sequence.count(opponent_piece)
        if sequence.count(opponent_piece) >= 1:
            if left_edge is True and sequence[0] == player_piece:
                count_pieces -= 1
            if right_edge is True and sequence[3] == player_piece:
                count_pieces -= 1
        if count_pieces < 0:
            count_pieces = 0
        return count_pieces ** 3
    if sequence.count(opponent_piece) == 3 and sequence.count(0) == 1:
        return -1000
    return 0


def score_array(array, player_piece):
    score = 0
    for i in range(len(array) - 3):
        sequence = array[i: i + 4]
        right_edge = False
        left_edge = False
        if i == 0:
            left_edge = True
        if i == len(array) - 4:
            right_edge = True
        score += score_sequence(sequence, player_piece, left_edge, right_edge)
    return score


def heuristic_score(board, player_piece, maxrows, maxcols):
    score = 0
    for row in range(maxrows):
        row_array = [i for i in list(board[row, :])]
        score += score_array(row_array, player_piece)

    # transpose = np.transpose(board)
    for col in range(maxcols):
        col_array = [i for i in list(board[:, col])]
        score += score_array(col_array, player_piece)

    forward_diagonal = [[] for _ in range(maxrows + maxcols - 1)]
    backward_diagonal = [[] for _ in range(len(forward_diagonal))]
    min_backward_diagonal = -maxrows + 1

    for x in range(maxcols):
        for y in range(maxrows):
            forward_diagonal[x + y].append(board[y][x])
            backward_diagonal[x - y - min_backward_diagonal].append(board[y][x])

    for diagonal in range(len(forward_diagonal)):
        score += score_array(forward_diagonal[diagonal], player_piece)

    for diagonal in range(len(backward_diagonal)):
        score += score_array(backward_diagonal[diagonal], player_piece)
    return score


def get_best_move(board, player_piece, maxrows, maxcols):
    best_score = 0
    best_move = (0, 0)
    for col in range(maxcols):
        if valid_move(board, col, maxrows, maxcols):
            board_temp = np.copy(board)
            row = put_piece(board_temp, player_piece, col, maxrows)
            score = heuristic_score(board_temp, player_piece, maxrows, maxcols)
            print(col, score)
            if score > best_score:
                best_score = score
                best_move = (row, col)
    return best_move


def cols_available(board, maxrows, maxcols):
    cols = []
    for col in range(maxcols):
        if valid_move(board, col, maxrows, maxcols):
            cols.append(col)
    return cols


def game_won(board, maxrows, maxcols):
    for row in range(maxrows):
        for col in range(maxcols):
            if board[row][col] == COMPUTER + 1:
                if check_winner(board, row, col, COMPUTER + 1, maxrows, maxcols) == COMPUTER + 1:
                    return COMPUTER
            elif board[row][col] == PLAYER1 + 1:
                if check_winner(board, row, col, PLAYER1 + 1, maxrows, maxcols) == PLAYER1 + 1:
                    return PLAYER1
    return -1


def is_terminal(board, maxrows, maxcols):
    return (game_won(board, maxrows, maxcols) != -1) or len(cols_available(board, maxrows, maxcols)) == 0


def minimax(board, depth, maximizing_player, alpha, beta, maxrows, maxcols):
    if depth == 0:
        if is_terminal(board, maxrows, maxcols):
            won = game_won(board, maxrows, maxcols)
            if won == COMPUTER:
                return None, INF
            elif won == PLAYER1:
                return None, -INF
            else:
                return None, 0
        else:
            return None, heuristic_score(board, COMPUTER + 1, maxrows, maxcols)
    else:
        cols = cols_available(board, maxrows, maxcols)
        if len(cols) < 1:
            return None, 0
        if maximizing_player:
            score = - math.inf
            best_col = cols[0]
            for col in cols:
                board_temp = np.copy(board)
                put_piece(board_temp, COMPUTER + 1, col, maxrows)
                new_score = minimax(board_temp, depth - 1, False, alpha, beta, maxrows, maxcols)[1]
                if new_score > score:
                    score = new_score
                    best_col = col
                alpha = max(score, alpha)
                if alpha >= beta:
                    break
            return best_col, score
        else:
            score = math.inf
            best_col = cols[0]
            for col in cols:
                board_temp = np.copy(board)
                put_piece(board_temp, PLAYER1 + 1, col, maxrows)
                new_score = minimax(board_temp, depth - 1, True, alpha, beta, maxrows, maxcols)[1]
                if new_score < score:
                    score = new_score
                    best_col = col
                beta = min(score, beta)
                if alpha >= beta:
                    break
            return best_col, score


def get_move_level(level, board, maxrows, maxcols, move_count):
    if level == "slab":
        return level1_computer(board, maxrows, maxcols)
    elif level == "mediu":
        return level2_computer(board, maxrows, maxcols, move_count)
    else:
        pygame.time.wait(500)
        return minimax(board, 4, True, ALFA, BETA, maxrows, maxcols)[0]


def run_game_pvc(maxrows, maxcols, first_player, level):
    pygame.init()
    font_won = pygame.font.SysFont('Arial', 30)
    font_info = pygame.font.SysFont('Arial', 20)
    screen_size = (maxcols * SQUARE_SIZE, (maxrows + 1) * SQUARE_SIZE)
    screen = pygame.display.set_mode(screen_size)

    game_over = False
    current_board = create_board(maxrows, maxcols)
    draw_board(screen, current_board, maxrows, maxcols)
    player_turn = get_first_turn(first_player)

    message = font_won.render("First player is: " + first_player, True, piece_color(player_turn + 1))
    screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 20))
    pygame.display.update()

    print(np.flip(current_board, 0))

    computer_move_count = 0
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION and player_turn == PLAYER1:
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
                        screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 20))
                        print("You won!")
                        game_over = True
                else:
                    message = font_info.render("The move is not valid! Try again!", True, piece_color(piece))
                    screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 10))
                    print("The move is not valid! Try again!")
                print(np.flip(current_board, 0))
                draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)
        if player_turn == COMPUTER and game_over is not True:
            piece = COMPUTER + 1
            move = get_move_level(level, current_board, maxrows, maxcols, computer_move_count)
            computer_move_count += 1
            print(current_board)
            row = put_piece(current_board, piece, move, maxrows)
            player_turn = 1 - player_turn

            if check_winner(current_board, row, move, piece, maxrows, maxcols) == piece:
                message = font_won.render("Computer won!", True, piece_color(piece))
                screen.blit(message, (SQUARE_SIZE / 2, SQUARE_SIZE / 2 - 20))
                print("Computer won!")
                game_over = True
            print(np.flip(current_board, 0))
            draw_board(screen, np.flip(current_board, 0), maxrows, maxcols)
        if len(cols_available(current_board, maxrows, maxcols)) == 0:
            game_over = True
        if game_over:
            pygame.time.wait(2500)
