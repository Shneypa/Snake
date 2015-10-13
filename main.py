import pygame
import time
import random

pygame.init()                                           # initialize pygame



# Display variables and display init

white = (255,255,255)                                         # defining Colors
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

gameDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))        # create window

pygame.display.set_caption("Slither")



block_size = 20                                          # snake moves 20 pixels per frame
appleThickness = 30

img = pygame.image.load('snake_head.png')                # load snake head spirte
apple_img = pygame.image.load('strawberry.png')          # load apple sprite

clock = pygame.time.Clock()                              # variable to control FPS
FPS = 30

starting_direction = "right"
direction = starting_direction

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


# Intro Loop

def game_intro():

    intro = True

    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither", green, -100, font_size= "large")

        message_to_screen("The objective of the game is to read red apples", black, -30, "small")
        message_to_screen("The more apples you eat the longer you get.", black, 0, "small")
        message_to_screen("If you run into yourself, you die!", black, 30, "small")
        message_to_screen("Press C to play or Q to quit.", black, 180, "small")

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(15)


# DRAWING THE SNAKE

def draw_snake(block_size, snakelist):

    # rotation of snake head sprite

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "up":
        head = img
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)


    # drawing snake head

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))            # draw snake head using sprite

    # drawing snake segments

    for XnY in snakelist[:-1]:                                           # draw all other snake segments
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])         # (x,y,width,height)




def text_objects(text, color, font_size):
    if font_size == "small":
        textSurface = smallfont.render(text, True, color)
    elif font_size == "medium":
        textSurface = medfont.render(text, True, color)
    elif font_size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color = black, y_displacement = 0, font_size = "small"):                  # discplacement from the center on Y axis

    textSurf, textRect = text_objects(msg, color, font_size)
    textRect.center = (WINDOW_WIDTH /2), (WINDOW_HEIGHT /2 + y_displacement)
    gameDisplay.blit(textSurf, textRect)


def randX():
       return (random.randrange((WINDOW_WIDTH - appleThickness) // block_size)) * block_size
def randY():
       return (random.randrange((WINDOW_HEIGHT - appleThickness) // block_size)) * block_size

# apple's coords can't start at (800, __ ) or(__ , 600) cuz will be out of bounds
# apples' coords have to be in steps of 10 pixels (in steps of our block_size, e.g. (0,50) (0,60) (0,70)
# and can't be in between ( e.g. apple can't be in (13, 38) coordinate, it has to be in (10, 40)


# GAME LOOP
def gameLoop():

    global direction        # now we can modify the direction variable which is initialized outside game loop
    direction = starting_direction

    # Game variables

    gameExit = False
    gameOver = False

    lead_x = WINDOW_WIDTH / 2
    lead_y = WINDOW_HEIGHT / 2
    lead_x_change = block_size
    lead_y_change = 0

    apple_x = randX()
    apple_y = randY()

    snakelist = []
    snakelength = 1


    # GAME LOOP:

    while not gameExit:


    # Play again or quit?

        while gameOver == True:

            gameDisplay.fill(white)
            message_to_screen("Game over",  y_displacement = -50, color = red, font_size = "large")
            message_to_screen("Press C to play again or Q to quit",black, 50, font_size = "small")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

                    if event.key == pygame.K_c:
                        gameLoop()


        # EVENT HANDLING

        for event in pygame.event.get():

            if event.type is pygame.QUIT:
                gameExit = True

            if event.type is pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                      if lead_x_change <= 0:        # if we were going right, disallow instant reverse of direction (so not to crash in itself)
                          lead_x_change = -block_size     # move 10 pixels left at every update
                          lead_y_change = 0         # reset vertical movement
                          direction = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                      if lead_x_change >= 0:
                          lead_x_change = block_size
                          lead_y_change = 0
                          direction = "right"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                      if lead_y_change <= 0:
                          lead_y_change = -block_size
                          lead_x_change = 0
                          direction = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                      if lead_y_change >= 0:
                          lead_y_change = block_size
                          lead_x_change = 0
                          direction = "down"


        # UPDATE AND RENDER

        lead_x += lead_x_change                     # updated coordinates for this frame
        lead_y += lead_y_change

        # check if snake crashed into itself (any segment except head is equal to head)
        for eachSegment in snakelist[:-1]:
            if eachSegment in snakehead:
                print("crashed into self!")
                gameOver


        # check if snake ran out of bounds
        if lead_x >= WINDOW_WIDTH or lead_x < 0 or lead_y < 0 or lead_y >= WINDOW_HEIGHT:
            gameOver = True


        gameDisplay.fill(white)                                                 # draws 'in the background'. we clean the screen.

        # drawing apple
        gameDisplay.blit(apple_img, (apple_x,apple_y))

        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        if len(snakelist) > snakelength:
            del snakelist[0]

        # drawing snake
        draw_snake(block_size, snakelist)

        # snake hit the apple
        if lead_x + block_size > apple_x and lead_x < apple_x + appleThickness :
           if lead_y + block_size > apple_y and lead_y < apple_y + appleThickness:
              apple_x = randX()
              apple_y = randY()
              snakelength += 1


        pygame.display.update()                                                 # draws everything to the screen

        clock.tick(FPS)                                                         # 30 FPS


    # END OF GAME LOOP

    gameDisplay.fill(white)

    pygame.display.update()

    pygame.quit()

    quit()


game_intro()

gameLoop()







'''
        CODING SEQUENCE - HYPOTHESIS

1. Screen and canvas initialization (white screen)
2. Run and update game loop
3. Draw  grid on a canvas                                                               // just use white fill for now

4. Create a snake object. (Properties: Length, Position of head, Direction, Image)      // just use rectangle for now
5. Snake moves on each update
6. KeyListener. (Snake changes direction if we press WASD or ARROWS)

7. Apple object (Properties: position (Randomly generated), Image )
8. Collision detection. (Snake is about to land on a square with an apple?  Snake lenght +1 )
9. Collision detection. (Snake is about to go out of bounds?) Lose
10. Collision detection. (Snake is about to hit itself?) Lose
11. Handling Quit game.
12. Score counter.
13. Lose game screen.
14. New game screen
15. Pause screen




        CODING SEQUENCE - ACTUAL

1. Create window
2. Simple game LOOP  (while loop)
3. Handle QUIT event

4. Draw a rectangle onto a screen (add update() method)
5. Listen to events (Key pressed? Change coordinates of the rectangle)
6. Set a variable that tracks change in coordinate (now rectangle is flying around at 2000 updates/second)
7. Limit updates/second to a reasonable FPS rate (60 FPS fo example)

8. setting movement rules (can't reverse direction, can't move diagonally)

9. Game over message to the screen

10. randomly draw an apple, adjust the coordinates to be a factor of block_size (fit the 'grid')


'''