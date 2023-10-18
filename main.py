import pygame
import random

pygame.init()

WINDOW_SIZE = (540, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (96, 216, 232)

FONT_SMALL = pygame.font.Font(None, 28)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_LARGE = pygame.font.Font(None, 48)

board = [[0 for x in range(9)] for y in range(9)]

def generate_puzzle():
    for i in range(9):
        for j in range(9):
            board[i][j] = 0

    for i in range(0, 9, 3):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(values)
        for j in range(3):
            for k in range(3):
                board[i+j][i+k] = values.pop()



    for i in range(200):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] == 0:
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(values)
            for value in values:
                if is_valid(row, col, value):
                    board[row][col] = value
                    break

    for i in range(50):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            temp = board[row][col]
            board[row][col] = 0
            if not is_valid(row, col, temp):
                board[row][col] = temp


def draw_board():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                pygame.draw.rect(screen, WHITE, (j*60, i*60, 60, 60))
                text = FONT_LARGE.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j*60+20, i*60+10))
            else:
                pygame.draw.rect(screen, LIGHT_BLUE, (j*60, i*60, 60, 60))
    for i in range(10):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (0, i*60), (540, i*60), thickness)
        pygame.draw.line(screen, BLACK, (i*60, 0), (i*60, 540), thickness)


def highlight_cell(row, col):
    pygame.draw.rect(screen, GRAY, (col*60, row*60, 60, 60), 3)


def fill_cell(row, col, value):
    board[row][col] = value



def is_valid(row, col, value):
    # Check row
    for i in range(9):
        if board[row][i] == value:
            return False

    for i in range(9):
        if board[i][col] == value:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row+i][box_col+j] == value:
                return False

    return True

def solve():
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for value in range(1, 10):
                    if is_valid(row, col, value):
                        board[row][col] = value
                        solve()
                        board[row][col] = 0
                return
    draw_board()
    pygame.display.update()

def show_result():
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, WHITE, (j*60, i*60, 60, 60))
            text = FONT_LARGE.render(str(board[i][j]), True, BLACK)
            screen.blit(text, (j*60+20, i*60+10))
    pygame.display.update()


running = True
selected_row = None
selected_col = None

generate_puzzle()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            selected_row = pos[1] // 60
            selected_col = pos[0] // 60
        elif event.type == pygame.KEYDOWN:
            if selected_row is not None and selected_col is not None:
                if event.unicode.isdigit() and int(event.unicode) != 0:
                    if is_valid(selected_row, selected_col, int(event.unicode)):
                        fill_cell(selected_row, selected_col, int(event.unicode))
                        selected_row = None
                        selected_col = None
                    else:
                       
                        text = FONT_SMALL.render("Invalid value!", True, BLACK)
                        screen.blit(text, (10, 550))
                        pygame.display.update()
                elif event.key == pygame.K_BACKSPACE:
                    fill_cell(selected_row, selected_col, 0)
                    selected_row = None
                    selected_col = None
                elif event.key == pygame.K_RETURN:
                    solve()
                elif event.key == pygame.K_SPACE:
                    show_result()
                elif event.key == pygame.K_n:
                    generate_puzzle()

   
    draw_board()

 
    if selected_row is not None and selected_col is not None:
        highlight_cell(selected_row, selected_col)


    pygame.display.update()

pygame.quit()
