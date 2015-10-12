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



block_size = WINDOW_WIDTH / 80 * 4                                                 # snake moves 10 pixels per frame
appleThickness = 30

clock = pygame.time.Clock()                                             # variable to control FPS
FPS = 15



# Putting messages to screen (will put in the middle of the scrren by default)

font_size = 25
font = pygame.font.SysFont(None, font_size)

def snake(block_size, snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])         # (x,y,width,height)

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (WINDOW_WIDTH /2), (WINDOW_HEIGHT /2 )
    gameDisplay.blit(textSurf, textRect)
    #screen_text = font.render(msg, True, color)
    #gameDisplay.blit(screen_text, [(WINDOW_WIDTH / 2, WINDOW_HEIGHT/2])

def randX():
       return (random.randrange((WINDOW_WIDTH - appleThickness) // block_size)) * block_size
def randY():
       return (random.randrange((WINDOW_HEIGHT - appleThickness) // block_size)) * block_size

# apple's coords can't start at (800, __ ) or(__ , 600) cuz will be out of bounds
# apples' coords have to be in steps of 10 pixels (in steps of our block_size, e.g. (0,50) (0,60) (0,70)
# and can't be in between ( e.g. apple can't be in (13, 38) coordinate, it has to be in (10, 40)


# GAME LOOP
def gameLoop():

    # Game variables

    gameExit = False
    gameOver = False

    lead_x = WINDOW_WIDTH / 2
    lead_y = WINDOW_HEIGHT / 2
    lead_x_change = 0
    lead_y_change = 0

    apple_x = randX()
    apple_y = randY()

    snakelist = []
    snakelength = 1

    snake_out_of_bounds = False
    snake_on_apple = False


    # GAME LOOP:

    while not gameExit:

    # Play again or quit?

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
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

                if event.key == pygame.K_LEFT:
                      if lead_x_change <= 0:        # if we were going right, disallow instant reverse of direction (so not to crash in itself)
                          lead_x_change = -block_size     # move 10 pixels left at every update
                          lead_y_change = 0         # reset vertical movement
                elif event.key == pygame.K_RIGHT:
                      if lead_x_change >= 0:
                          lead_x_change = block_size
                          lead_y_change = 0
                elif event.key == pygame.K_UP:
                      if lead_y_change <= 0:
                          lead_y_change = -block_size
                          lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                      if lead_y_change >= 0:
                          lead_y_change = block_size
                          lead_x_change = 0


        # UPDATE AND RENDER

        lead_x += lead_x_change                     # updated coordinates for this frame
        lead_y += lead_y_change

        # check if snake crashed into itself (any segment except head is equal to head)
        for eachSegment in snakelist[:-1]:
            if eachSegment in snakehead:
                gameOver

        # check if snake ran out of bounds
        if lead_x >= WINDOW_WIDTH or lead_x < 0 or lead_y < 0 or lead_y >= WINDOW_HEIGHT:
            snake_out_of_bounds = True
            gameOver = True

        gameDisplay.fill(white)                                                 # draws 'in the background'. we clean the screen.


        pygame.draw.rect(gameDisplay, red, [apple_x, apple_y, appleThickness, appleThickness])


        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        if len(snakelist) > snakelength:
            del snakelist[0]

        snake(block_size, snakelist)

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