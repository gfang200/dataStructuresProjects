#! /usr/bin/env python

import sys, time, random
import pygame

e_aplh = "abcdefghijklmnopqrstuvwxyz"
dna_alph = "ACGT"

# generate random string drawn from the given alphabet and of a given length
def gen_random_string(alphabet, length):
    a_len = len(alphabet)
    ret = ""
    for n in range(length):
        ret += alphabet[random.randint(0, a_len-1)]
    return ret

# print gen_random_string(e_aplh, 5)

SPACE_CHAR = '_'
SPACE_PENALTY = -1

# the scoring function
def s(x, y, enable_graphics=True):
    if x == SPACE_CHAR or y == SPACE_CHAR:
        return SPACE_PENALTY
    elif x == y:
        return 2
    else:
        return -2

TILE_SIZE = 40
tile_color = (255, 255, 255)
highlight_color = (120, 129, 250)

def init_board(m, n):
    screen = pygame.display.set_mode(((m+2)*TILE_SIZE, (n+2)*TILE_SIZE))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Dot Board')
    pygame.font.init()
    font = pygame.font.Font(None, 15)
    return screen, font

def create_tile(font, text, color):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill(color)
    b1 = font.render(text, 1, (0, 0, 0))
    tile.blit(b1, (TILE_SIZE/2, TILE_SIZE/2))
    return tile

def render_board(board, font, s1, s2, F):
    for i in range(len(s1)):
        tile = create_tile(font, s1[i], tile_color)
        board.blit(tile, ((i+2)*TILE_SIZE, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (TILE_SIZE, 0))
    for j in range(len(s2)):
        tile = create_tile(font, s2[j], tile_color)
        board.blit(tile, (0, (j+2)*TILE_SIZE))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, TILE_SIZE))
    for (x,y) in sorted(F.keys()):
        tile = create_tile(font, str(F[(x,y)]), tile_color)
        board.blit(tile, ((x+1)*TILE_SIZE, (y+1)*TILE_SIZE))
    
def seq_align(X, Y):
    #helper score functions
    def aScore(i, j):
        if i == 0:
            if j == 0:
                return 0
            return float("-infinity")
        
        else:
            return board[i-1][j][0] - 1

    def bScore(i, j):
        if j == 0:
            if i == 0:
                return 0
            return float("-infinity")
        else:
            return board[i][j-1][0] - 1

    def cScore(i, j):
        if i == 0:
            if j == 0:
                return 0
            return float("-infinity")
        if j == 0:
            if i == 0:
                return 0
            return float("-infinity")

        if Y[i-1] == X[j-1]:
            return board[i-1][j-1][0] + 2
        else:
            return board[i-1][j-1][0] - 2

    #traverse the board backwards to get the strings     
    def traverse():
        return traverse_helper([], [], (y_length, x_length))
    
    def traverse_helper(x, y, coord):
        if coord == (0, 0):
            return(x, y)
        
        direction = board[coord[0]][coord[1]][1]
        if direction == "a":
            y.append(Y[coord[0]-1])
            x.append("_")
            newCoord = (coord[0]-1, coord[1])
        elif direction == "b":
            y.append("_")
            x.append(X[coord[1]-1])
            newCoord = (coord[0], coord[1]-1)
        else:
            y.append(Y[coord[0]-1])
            x.append(X[coord[1]-1])
            newCoord = (coord[0]-1, coord[1]-1)

        return traverse_helper(x, y, newCoord)


    #start main def
    x_length = len(X)
    y_length = len(Y)

    #generate empty board
    board = []
    for i in range(y_length + 1):
        board.append([])
        for j in range(x_length + 1):
            board[i].append(None)
        
    #score the board
    for i in range(y_length + 1):
        for j in range(x_length + 1):
            #a is for coming from the left
            #b is for coming from the top
            #c is for coming from the diagonal
            a = aScore(i, j)
            b = bScore(i, j)
            c = cScore(i, j)
            direction = ""

            score = max(a, b, c)
            if score == a:
                direction = "a"
            elif score == b:
                direction = "b"
            else:
                direction = "c"

            board[i][j] = (score, direction)  

    pair = traverse()
    
    #pair is reversed, need to flip them
    return (pair[0][::-1], pair[1][::-1])

if len(sys.argv) == 2 and sys.argv[1] == 'test':
    f=open('tests.txt', 'r');tests= eval(f.read());f.close()
    cnt = 0; passed = True
    for ((s1, s2), (a1, a2)) in tests:
        (ret_a1, ret_a2) = seq_align(s1, s2, False)
        if (ret_a1 != a1) or (ret_a2 != a2):
            print("test#" + str(cnt) + " failed...")
            passed = False
        cnt += 1
    if passed: print("All tests passed!")
elif len(sys.argv) == 2 and sys.argv[1] == 'gentests':
    tests = []
    for n in range(25):
        m = random.randint(8, 70); n = random.randint(8, 70)
        (s1, s2) = (gen_random_string(dna_alph, m), gen_random_string(dna_alph, n))
        (a1, a2) = seq_align(s1, s2, False)
        tests.append(((s1, s2), (a1, a2)))
    f=open('tests.txt', 'w');f.write(str(tests));f.close()
else:
    l = [('ACACACTA', 'AGCACACA'), ('IMISSMISSISSIPI', 'MYMISSISAHIPPIE')]
    enable_graphics = True
    if enable_graphics: pygame.init()
    for (s1, s2) in l:
        print 'sequences:'
        print (s1, s2)
        
        m = len(s1)
        n = len(s2)
        
        print 'alignment: '
        print seq_align(s1, s2, enable_graphics)
    
    if enable_graphics: pygame.quit()

