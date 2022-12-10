from sys import _current_frames
import pygame
from pygame.locals import *
import numpy as np
import random
from queue import PriorityQueue
import time

# define color
COLOR_YELLOW = (241, 235, 156)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 191, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_PINK = (255, 115, 150)
COLOR_PURPLE = (128, 0, 128)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)


# define font
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)


# create the screen
width = 1000
height = 800
tile = 50
rows = height//tile
cols = width//tile
screen = pygame.display.set_mode((width, height))
# screen.fill(COLOR_YELLOW)
clock = pygame.time.Clock()

pygame.display.set_caption('Maze solver')
FPS = 30


class cell():
    def __init__(self, x, y,):
        self.x, self.y = x, y
        self.visit = False
        self.walls = {'top': True, 'right': True,
                      'bottom': True, 'left': True}

    def draw(self):
        x, y = self.x*tile, self.y*tile
        if self.visit:
            pygame.draw.rect(screen, COLOR_YELLOW,
                             (x, y, tile, tile))

        if self.walls['top']:
            pygame.draw.line(screen, COLOR_GREEN,
                             (x, y), (x+tile, y), 4)

        if self.walls['right']:
            pygame.draw.line(screen, COLOR_GREEN, (x+tile,
                             y), (x+tile, y+tile), 4)

        if self.walls['bottom']:
            pygame.draw.line(screen, COLOR_GREEN, (x, y +
                             tile), (x+tile, y+tile), 4)

        if self.walls['left']:
            pygame.draw.line(screen, COLOR_GREEN,
                             (x, y), (x, y+tile), 4)

    def current_cell_draw(self):
        x, y = self.x*tile, self.y*tile
        pygame.draw.rect(screen, COLOR_BLUE,
                         (x+4, y+4, tile-4, tile-4))

    def index(self, x, y):
        if x < 0 or y < 0 or x > cols-1 or y > rows-1:
            return False
        return grid_cells[x + y * cols]

    def check_neighbors_cells(self):
        neighbors = []

        top = self.index(self.x, self.y-1)
        right = self.index(self.x+1, self.y)
        bottom = self.index(self.x, self.y+1)
        left = self.index(self.x-1, self.y)

        if top and not top.visit:
            neighbors.append(top)
        if right and not right.visit:
            neighbors.append(right)
        if bottom and not bottom.visit:
            neighbors.append(bottom)
        if left and not left.visit:
            neighbors.append(left)

        if neighbors:
            return random.choice(neighbors)
        else:
            return False

    # print("("+str(self.x)","+self.y+")")


def display_cell_number():
    temp = []
    for i in range(rows):
        for j in range(cols):
            temp.append((i, j))

    return temp


def remove_walls(current, next):
    a = current.x - next.x
    if a == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    elif a == 1:
        current.walls['left'] = False
        next.walls['right'] = False

    b = current.y - next.y
    if b == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False
    elif b == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False


def heruistic_manhattan(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1-x2)+abs(y1-y2))


def display_start_end(end, start):
    pygame.draw.rect(screen, COLOR_PURPLE,
                     ((start[1]*tile)+4, (start[0]*tile)+4, tile-4, tile-4))
    pygame.draw.rect(screen, COLOR_CYAN,
                     ((end[1]*tile)+4, (end[0]*tile)+4, tile-4, tile-4))
    pygame.display.update()


def reconstruct_path(came_from, end, start):
    tile_t = tile/4
    while end in came_from:
        end = came_from[end]
        pygame.draw.rect(screen, COLOR_PINK,
                         ((end[1]*tile)+tile_t, (end[0]*tile)+tile_t, tile_t, tile_t))
    pygame.display.update()


def a_star_algortihm():
    grid = display_cell_number()
    # value of start and end should not exceed maximum value i.e rows and cols
    start = (0, 0)
    end = (7, 7)

    open_set = PriorityQueue()
    came_from = {}

    g_score = {cell: float('inf') for cell in grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in grid}
    f_score[start] = heruistic_manhattan(start, end)

    open_set_hash = [start]

    open_set.put((f_score[start], heruistic_manhattan(start, end), start))

    while not open_set.empty():
        present_cell = open_set.get()

        if present_cell[2] == end:
            return came_from, end, start

        k = present_cell[2][0] * cols + present_cell[2][1]
        open_set_hash.remove(present_cell[2])

        for d in 'top', 'right', 'bottom', 'left':
            if grid_cells[k].walls[d] == False:
                if d == 'top':
                    future_cell = (present_cell[2][0]-1, present_cell[2][1])
                if d == 'right':
                    future_cell = (present_cell[2][0], present_cell[2][1]+1)
                if d == 'bottom':
                    future_cell = (present_cell[2][0]+1, present_cell[2][1])
                if d == 'left':
                    future_cell = (present_cell[2][0], present_cell[2][1]-1)

                temp_g_score = g_score[present_cell[2]]+1

                if temp_g_score < g_score[future_cell]:
                    came_from[future_cell] = present_cell[2]
                    g_score[future_cell] = temp_g_score
                    f_score[future_cell] = temp_g_score + \
                        heruistic_manhattan(future_cell, end)

                    if future_cell not in open_set_hash:
                        open_set_hash.append(future_cell)
                        open_set.put((f_score[future_cell], heruistic_manhattan(
                            future_cell, end), future_cell))
    return None


grid_cells = [cell(col, row) for row in range(rows)for col in range(cols)]
current_cell = grid_cells[0]
stack = []
bool_astar = False
show_path = False

while True:
    clock.tick(FPS)
    [cell.draw() for cell in grid_cells]

    current_cell.visit = True
    current_cell.current_cell_draw()
    next_cell = current_cell.check_neighbors_cells()
    if next_cell:
        next_cell.visit = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    # display_cell_number()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_LCTRL:
                bool_astar = True
                came_from_t, end_t, start_t = a_star_algortihm()
            if event.key == K_RCTRL:
                show_path = True

    if bool_astar == True:
        display_start_end(end_t, start_t)
        if show_path == True:
            reconstruct_path(came_from_t, end_t, start_t)

    pygame.display.update()
    clock.tick(30)
