# HIT137 - Assignment 2 Keith Yardley & Mark Zeroni
#                       ******   Tetris   ******

### Instructions ###
# Left and right arrows move figures accordingly. Up arrow rotates the figure. Press "C" to hold the piece or swap it with the currently held piece.
# Down arrow speeds up the figures descent. Escape starts game again. Click the "X" to Quit.

#CHANGES TO BE MADE
    #Make pieces come in proper order - DONE
    #Give pieces proper colors - DONE
    #Next pieces - DONE
    #Hold pieces - DONE
    #Seperate lines cleared and score
    #Pause button
    #High scores
    #Instruction menu
    #Speed up after x score (or blocks placed to award multiple line clears)

# Package imports
import pygame
import random

# Defines colors of shapes
colours = [
    (0,0,0),        #Black - needed to fix bug with teal pieces disappearing
    (65, 241, 241), #Teal - if this was first it would be index 0 and thus disappear once placed
    (0, 47, 246),   #Blue
    (238, 158, 0),  #Orange
    (243,237,0),    #Yellow
    (78,238,0),     #Green
    (152, 44, 246), #Purple
    (234, 0, 0),    #Red
]

#Class for shape generation
class Figure:
    figures = [
        [[4,5,6,7],[2,6,10,14],[8,9,10,11],[1,5,9,13]], #I tetromino (4 long shape)
        [[0,4,5,6],[2,1,5,9],[4,5,6,10],[1,5,9,8]],     #J tetromino
        [[4,5,6,2],[1,5,9,10],[8,4,5,6],[0,1,5,9]],     #L tetromino
        [[1,2,5,6]],                                    #O tetromino (cube)
        [[1,2,4,5],[1,5,6,10],[8,9,5,6],[0,4,5,9]],     #S tetromino
        [[1,4,5,6],[1,5,6,9],[4,5,6,9],[1,4,5,9]],      #T tetromino
        [[0,1,5,6],[2,6,5,9],[4,5,9,10],[1,5,4,8]]      #Z tetromino
    ]

    def __init__(self, x, y, piece):
        self.x = x
        self.y = y
        self.type = piece
        self.color = piece + 1
        self.rotation = 0

    def image(self):
        '''Returns the current shape position (rotation) in a 4x4 grid as a list of numbers'''
        return self.figures[self.type][self.rotation] #Rotation of figure upon generation

    def rotate(self):
        '''Iterates through the list of rotations for a particular shape'''
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])  #floor division used to loop around

class Tetris:
    level = 1
    x = 160
    y = 60
    zoom = 20
    figure = None
    next_figure = None
    held_figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.lines_cleared = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        global current, count, joined_list
        if count > 6:
            joined_list = joined_list[7:] + random.sample(current, 7)
            count = 0
        piece = joined_list[count]
        count += 1
        self.figure = Figure(3, 0, piece)

    def next_piece(self):
        global joined_list, count
        piece = joined_list[count]
        self.next_figure = Figure(12, 1, piece)

    def swap_held_piece(self):
        if self.held_figure == None:
            self.held_figure = Figure(-5, 1, self.figure.type)
            self.new_figure()
        else:
            #Current type
            held_type = self.held_figure.type
            self.held_figure = Figure(-6, 1, self.figure.type)
            self.figure = Figure(3, 0, held_type)

    def intersects(self):
        intersection = False
        for i in range(4):      #i represents row
            for j in range(4):  #j represents column
                if i * 4 + j in self.figure.image():                #numerical position in grid
                    if (i + self.figure.y >= self.height or                         #All test if occupied grid position is out of bounds
                            j + self.figure.x >= self.width or
                            j + self.figure.x < 0 or
                            self.field[i + self.figure.y][j + self.figure.x] > 0):
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):     #Checks each row
            zeros = 0
            for j in range(self.width):     #Checks each space in row
                if self.field[i][j] == 0:   #If space is empty:
                    zeros = 1
            if zeros == 0:                  #If there are no empty spaces
                lines += 1
                for k in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
        self.score += lines ** 2    #Clearing multiple lines at once gives a better score
        self.lines_cleared += lines

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        self.next_piece()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        '''Moves shape dx squares to the right, stopping if it intersects with the boundries or another piece'''
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        '''Rotates shape clockwise, stopping if it intersects with the boundries or another piece'''
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define colors that are not shapes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Defines size of the screen
size = (520, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris - Yardley & Zeroni") # Can remove name if you want I think it's a nice touch

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0     #Used for dropping speed

current = [0,1,2,3,4,5,6]
count = 0
joined_list = random.sample(current, 7)+random.sample(current, 7)

pressing_down = False

while not done:

    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_c:
                game.swap_held_piece()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
                counter = 0

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK) # Sets background to black to assist with ease of playing for long term.

    for i in range(game.height):    #Draws grid pattern
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:    #If there is something in the current square:
                pygame.draw.rect(screen, colours[game.field[i][j]], #Draw a rect with the associated color
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    #Held Window
    pygame.draw.rect(screen, GRAY, [game.x - game.zoom * 6, game.y, game.zoom*4, game.zoom*4], 1)
    #Next Window
    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * 12, game.y, game.zoom*4, game.zoom*4], 1)

    if game.figure is not None: #Draw figure if it exists
        for i in range(4):
            for j in range(4):
                p = i * 4 + j   #Go through each square in the figure's 4x4 grid
                if p in game.figure.image():
                    pygame.draw.rect(screen, colours[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    if game.next_figure is not None: #Draw next figure if it exists
        for i in range(4):
            for j in range(4):
                p = i * 4 + j   #Go through each square in the figure's 4x4 grid
                if p in game.next_figure.image():
                    pygame.draw.rect(screen, colours[game.next_figure.color],
                                     [game.x + game.zoom * (j + game.next_figure.x) + 1,
                                      game.y + game.zoom * (i + game.next_figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    if game.held_figure is not None: #Draw held figure if it exists
        for i in range(4):
            for j in range(4):
                p = i * 4 + j   #Go through each square in the figure's 4x4 grid
                if p in game.held_figure.image():
                    pygame.draw.rect(screen, colours[game.held_figure.color],
                                     [game.x + game.zoom * (j + game.held_figure.x) + 1,
                                      game.y + game.zoom * (i + game.held_figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("SCORE: " + str(game.score), True, WHITE)
    text_game_over = font1.render("GAME OVER", True, WHITE)
    text_game_over1 = font1.render("  Press ESC", True, (0, 255, 255))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
