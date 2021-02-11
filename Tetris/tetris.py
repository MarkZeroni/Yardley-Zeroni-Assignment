# HIT137 - Assignment 2 Keith Yardley & Mark Zeroni
#                       ******   Tetris   ******

#MZ high score: 151, 87 lines cleared

#CHANGES TO BE MADE
    #Optimise
    #Remove debug code

# Package imports
import pygame
import random

# Defines colors of shapes - all rgb values are approximately accurate to the actual game.
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

class Figure:
    '''Generates a new shape, and can be used to get information about an already made shape.'''
    #List of points in a 4x4 grid that correspond to shapes and their rotations
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
    '''Generates the main game and contains many functions to manipulate shapes in the game.'''
    level = 1
    x = 160
    y = 60
    zoom = 20
    figure = None
    next_figure = None
    held_figure = None
    prediction_figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [] #Contains all grid spaces and the currently placed piece in them.
        self.score = 0
        self.lines_cleared = 0
        self.state = "start"
        for i in range(height):
            new_line = []   #Rows
            for j in range(width):
                new_line.append(0)  #Items in rows (initially nothing so all 0s)
            self.field.append(new_line)

    def new_figure(self):
        '''Creates a new piece from the list of pieces. Destroys the prediction piece so that it can be regenerated for the new piece.'''
        global current, count, joined_list
        if count > 6:
            joined_list = joined_list[7:] + random.sample(current, 7) #The list contains the next 14 figures, so that when all 7 types have been dropped,
            count = 0                                                 #the next piece will still work.
        piece = joined_list[count]
        count += 1
        self.figure = Figure(3, 0, piece)
        self.prediction_figure = None

    def prediction_piece(self):
        '''Generates a prediction piece at the location of and with the same rotation as the current piece. It then goes down until it intersects.'''
        self.prediction_figure = Figure(self.figure.x, self.figure.y, self.figure.type)
        self.prediction_figure.rotation = self.figure.rotation
        while not self.intersects(self.prediction_figure):
            self.prediction_figure.y += 1
        self.prediction_figure.y -= 1

    def next_piece(self):
        '''Finds the next piece from the list and defines it as an object.'''
        global joined_list, count
        piece = joined_list[count]
        self.next_figure = Figure(12, 1, piece)

    def swap_held_piece(self):
        '''Swaps the current held piece with the current falling piece.'''
        global swapped
        if swapped == False: #Can only swap once per piece.
            if self.held_figure == None:
                self.held_figure = Figure(-6, 1, self.figure.type)
                self.new_figure() #Can't swap if there is no piece to swap with.
            else:
                held_type = self.held_figure.type                   #Temporary storage of the held figure type.
                self.held_figure = Figure(-6, 1, self.figure.type)  #Overwrites the held figure with the current figure in play.
                self.figure = Figure(3, 0, held_type)               #Creates a new figure with the original held type.
            swapped = True

    def intersects(self, figure):
        '''Checks if the specified piece is intersecting a wall or placed pieces, and returns a boolean.'''
        intersection = False
        for i in range(4):      #i represents row
            for j in range(4):  #j represents column
                if i * 4 + j in figure.image():                #numerical position in grid
                    if (i + figure.y >= self.height or         #All test if occupied grid position is out of bounds
                            j + figure.x >= self.width or 
                            j + figure.x < 0 or
                            self.field[i + figure.y][j + figure.x] > 0):    #Checks if piece intersects with already placed piece
                        intersection = True
        return intersection

    def break_lines(self):
        '''Checks if there are any full lines. If there are, it deletes them and moves everything above down.'''
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
                        self.field[k][j] = self.field[k - 1][j] #Moves lines above the now empty line down one, starting from the bottom.
        self.score += lines ** 2    #Clearing multiple lines at once gives a better score
        self.lines_cleared += lines

    def go_space(self):
        '''Forces piece to go down instantly until it intersects, then it goes back up 1 and then freezes.'''
        while not self.intersects(self.figure):
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        '''Makes piece go down 1 square. If it then intersects, it goes back up and then freezes.'''
        self.figure.y += 1
        if self.intersects(self.figure):
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        '''Converts the currently falling piece into a static object on the game grid.'''
        global swapped
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():                                     #For each square with the figure in it:
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color #The field array gets set to the color of the piece
        self.break_lines()  #Checks if placed piece has caused a line to be filled.
        self.new_figure()
        self.next_piece()
        swapped = False     #Resets hold function to allow the next piece to be swapped.
        if self.intersects(self.figure):    #If immediately after the new piece is created, it intersects,
            self.state = "gameover"         #then the placed pieces have reached the top and the game is over.

    def go_side(self, dx):
        '''Moves shape dx squares to the right, stopping if it intersects with the boundries or another piece'''
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects(self.figure):
            self.figure.x = old_x

    def rotate(self):
        '''Rotates shape clockwise, stopping if it intersects with the boundries or another piece'''
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects(self.figure):
            self.figure.rotation = old_rotation

#---------------DEFINITIONS---------------#
def draw_figure(figure, width):
    '''Draws the figure onto the screen. Width of 0 means a square is completely filled, and larger values correspond to the size of the outline of the square.'''
    if figure is not None: #Draw figure if it exists
        for i in range(4):
            for j in range(4):
                p = i * 4 + j   #Go through each square in the figure's 4x4 grid
                if p in figure.image():
                    pygame.draw.rect(screen, colours[figure.color],
                                    [game.x + game.zoom * (j + figure.x) + 1,
                                    game.y + game.zoom * (i + figure.y) + 1,
                                    game.zoom - 2, game.zoom - 2], width)

def draw_text(text, font, color, x, y, anchor, outline):
    '''Draws text onto the screen with a rectangle corner anchored at a specific co-ordinate, with the ability to create outlines.'''
    text_temp = font.render(text, True, WHITE)
    rect_temp = text_temp.get_rect()
    rect_temp.__setattr__(anchor, (x,y))
    if outline == True:
        outline_temp = font.render(text, True, BLACK)
        x, y = rect_temp.topleft[0], rect_temp.topleft[1]
        for i in [(x-2,y-2),(x+2,y-2),(x+2,y+2),(x-2,y+2)]: #Outline works by rendering 4 black versions of the text slightly offset from the centre.
            screen.blit(outline_temp, i)
    screen.blit(text_temp, rect_temp)

def draw_instructions(instructions_list):
    '''Draws the list of instructions onto the screen, with each line being printed underneath the previous.'''
    start_y = 480
    j = 0
    for i in instructions_list:
        text = font_small.render(i, True, WHITE)
        rect = text.get_rect(midtop=(size_x/2,start_y + (j * font_small.get_linesize())))
        screen.blit(text, rect)
        j += 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size_x = 520
size_y = 600
size = (size_x, size_y)
pygame.init()   # Initialize the game engine
screen = pygame.display.set_mode(size) # Defines size of the screen
pygame.display.set_caption("Tetris - Yardley & Zeroni") # Renames window
clock = pygame.time.Clock()

done = False # Loop until the user clicks the close button.
paused = False
pressing_down = False
swapped = False

fps = 60
counter = 0     #Used for piece dropping speed
game = Tetris(20, 10)
levels_passed = [0]

current = [0,1,2,3,4,5,6]
count = 0
joined_list = random.sample(current, 7)+random.sample(current, 7)

instructions_list = [
    "Left and right arrows move the piece left and right.",
    "Up arrow rotates the piece.",
    "Down arrow moves the piece down faster.",
    "Space instantly places the piece.",
    "C holds the piece and/or swaps with the currently held piece.",
    "P pauses/unpauses the game."
    ]

font_small = pygame.font.SysFont('Calibri', 16, True, False)
font_med = pygame.font.SysFont('Calibri', 25, True, False)
font_large = pygame.font.SysFont('Calibri', 65, True, False)

while not done:
    for event in pygame.event.get():        #These allow the program to be unpaused and closed when paused.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
        if event.type == pygame.QUIT:
                done = True
                paused = True
                
    while not paused:
        if game.figure is None:
            game.new_figure()   #Generates initial piece

        game.prediction_piece() #Generates the prediction piece

        gravity = (0.8 - ((game.level - 1)*0.007)) ** (game.level - 1) #Official tetris formula - time per row in seconds
        counter += 1 #Counts frames elapsed

        if (game.lines_cleared % 10 == 0) and (game.level < 15):   #Every 10 lines cleared, the level increases until the level is 15.
            if game.lines_cleared not in levels_passed:
                game.level += 1
                levels_passed.append(game.lines_cleared)    #Needed to prevent the level continually increasing every loop.

        if (counter >= (60 * gravity)) or (pressing_down and counter % 3 == 0):
            if game.state == "start":
                counter = 0
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                paused = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True    #Allows holding the button down
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_c:
                    game.swap_held_piece()
                if event.key == pygame.K_ESCAPE:    #Reset all
                    game.__init__(20, 10)
                    game.figure = None
                    counter = 0
                    game.held_figure = None
                    game.level = 1
                    levels_passed = []

        if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False   #Allows holding the button down

        screen.fill(BLACK) # Sets background to black to assist with ease of playing for long term.

        for i in range(game.height):    #Draws grid pattern
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:    #If there is something in the current square:
                    pygame.draw.rect(screen, colours[game.field[i][j]], #Draw a rect with the associated color
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        pygame.draw.rect(screen, GRAY, [game.x - game.zoom * 6, game.y, game.zoom*4, game.zoom*4], 1) #Held Window
        pygame.draw.rect(screen, GRAY, [game.x + game.zoom * 12, game.y, game.zoom*4, game.zoom*4], 1) #Next Window
        
        draw_figure(game.figure, 0) #Draws the figures onto the screen
        draw_figure(game.next_figure, 0)
        draw_figure(game.held_figure, 0)
        draw_figure(game.prediction_figure, 2)

    #---------------TEXT---------------#
        draw_text("SCORE: " + str(game.score), font_med, WHITE, 10, 10, "topleft", False)
        draw_text("LINES: " + str(game.lines_cleared), font_med, WHITE, 510, 10, "topright", False)
        draw_text("LEVEL: " + str(game.level), font_med, WHITE, size_x/2, 10, "midtop", False)
        draw_text("HOLD", font_med, WHITE, 80, 150, "midtop", False)
        draw_text("NEXT", font_med, WHITE, 440, 150, "midtop", False)
        draw_instructions(instructions_list)

        if game.state == "gameover":
            draw_text("GAME OVER", font_large, font_large, size_x/2,(size_y/2)-10, "midbottom", True)
            draw_text("Press ESC", font_large, font_large, size_x/2,(size_y/2)+10, "midtop", True)

        if paused == True:
            draw_text("PAUSED", font_large, WHITE, size_x/2, size_y/2, "center", True)

        pygame.display.flip()   #Updates the screen
        clock.tick(fps)         #Waits until (1/fps) seconds passes

pygame.quit()