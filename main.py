import time
import sys
import glob
import random
import pygame
from pygame.locals import *

#print glob.glob('textures/*.png')
#sys.exit(0)

#constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
GREY  = (78, 66,    66)
RED   = (255, 0,     0)
WHITE = (255, 255, 255)

#constants representing the different resources
DIRT    = 0
GRASS   = 1
WATER   = 2
COAL    = 3
ROCK    = 4
LAVA    = 5
BEDROCK = 6
IRON    = 7
WOOD    = 8
HEARTS  = 9
FIRE    = 10
BRICK   = 11

#a dictionary linking resources to colours
textures =   {
                DIRT    : pygame.image.load('textures/dirt.png'),
                GRASS   : pygame.image.load('textures/grass.png'),
                WATER   : pygame.image.load('textures/water.png'),
                COAL    : pygame.image.load('textures/coal.png'),
                ROCK    : pygame.image.load('textures/rock.png'),
                LAVA    : pygame.image.load('textures/lava.png'),
                BEDROCK : pygame.image.load('textures/bedrock.png'),
                IRON    : pygame.image.load('textures/iron.png'),
                WOOD    : pygame.image.load('textures/wood.png'),
                HEARTS  : pygame.image.load('textures/heart.png'),
                FIRE    : pygame.image.load('textures/fire.png'),
                BRICK   : pygame.image.load('textures/brick.png')
             }

inventory =   {
                DIRT   : 0 ,
                GRASS  : 0 ,
                COAL   : 0 ,
                ROCK   : 0 ,
                IRON   : 0 ,
                WOOD   : 0 ,
                FIRE   : 0 ,
                BRICK  : 0 ,
                HEARTS : 20
            }

#maps each resource to the EVENT key used to place/craft it
controls = {
                DIRT    : 49,  #event 49 is the '1' key
                GRASS   : 50,  #event 50 is the '2' key, etc.
                #WATER   : 51,
                #COAL    : 52,
                WOOD    : 52, # 4
                FIRE    : 53, # 5
                #SAND    : 55,
                #GLASS   : 56,
                ROCK    : 51, # 3
                #STONE   : 48,
                BRICK   : 54, # 6
                #DIAMOND : 61
            }

craft =    {
                FIRE : { WOOD : 2, ROCK : 2 },
                BRICK: { ROCK : 3 }
            }
#useful game dimensions
TILESIZE  = 40
MAPWIDTH  = 30
MAPHEIGHT = 20


resources = [DIRT, GRASS, COAL, ROCK, IRON, WOOD, FIRE, BRICK, HEARTS]
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ] 
#set up the display
pygame.init()

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE+50))

PLAYER = pygame.image.load('player.png').convert_alpha()
playerPos = [0, 0]

INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)
pygame.display.set_caption('Minecraft a1.0')
pygame.display.set_icon(pygame.image.load('minecraft.jpeg'))

for rw in range(MAPHEIGHT):
    #loop through each column in that row
    for cl in range(MAPWIDTH):
        #pick a random number between 0 and 15
        randomNumber = random.randint(0,15)
        #if a zero, then the tile is coal
        if randomNumber == 0:
            tile = COAL
        #water if the random number is a 1 or a 2
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif randomNumber >= 3 and randomNumber <= 7:
            tile = GRASS
        elif randomNumber == 7 or randomNumber == 8:
            tile = ROCK
        elif randomNumber > 8 and randomNumber < 12:
            tile = DIRT
        else:
            tile = WOOD
        #set the position in the tilemap to the randomly chosen tile
        tilemap[rw][cl] = tile


while True:

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
                        

            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH - 1:
                playerPos[0] += 1 
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1
            if event.key == K_SPACE:
                #what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if currentTile == LAVA or currentTile == WATER or currentTile == BEDROCK:
                    continue
                if currentTile == IRON:
                    tilemap[playerPos[1]][playerPos[0]] = BEDROCK                
                #player now has 1 more of this resource
                inventory[currentTile] += 1
                #the player is now standing on dirt
                deep_chanche = random.randint(0, 10)
                if deep_chanche < 9:
                    tilemap[playerPos[1]][playerPos[0]] = BEDROCK
                elif deep_chanche == 9:
                    tilemap[playerPos[1]][playerPos[0]] = IRON
                else:
                    tilemap[playerPos[1]][playerPos[0]] = LAVA
                    inventory[HEARTS] -= 2

                    if inventory[HEARTS] <= 0:
                        #pygame.display.fill(BLACK, None, 0)                        
                        #msg = INVFONT.render('You Lose', True, BLACK)
                        time.sleep(3)
                        sys.exit(0)
            for key in controls:

                #if this key was pressed
                if (event.key == controls[key]):

                    #CRAFT if the mouse is also pressed
                    if pygame.mouse.get_pressed()[0]:

                        #if the item can be crafted
                        if key in craft:

                            #keeps track of whether we have the resources
                            #to craft this item
                            canBeMade = True
                            #for each item needed to craft...
                            for i in craft[key]:
                                #...if we don't have enough...
                                if craft[key][i] > inventory[i]:
                                    #...we can't craft it!
                                    canBeMade = False
                                    break
                            #if we can craft it (we have all needed resources)
                            if canBeMade == True:
                                #take each item from the inventory
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                #add the crafted item to the inventory
                                inventory[key] += 1
                        
                    else:
                        if (event.key == K_1):
                            #get the tile to swap with the dirt
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            #if we have dirt in our inventory
                            if inventory[DIRT] > 0:
                                #remove one dirt and place it
                                inventory[DIRT] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = DIRT

                        if (event.key == K_2):
                            #get the tile to swap with the dirt
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            #if we have dirt in our inventory
                            if inventory[GRASS] > 0:
                                #remove one dirt and place it
                                inventory[GRASS] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = GRASS
                        if (event.key == K_3):
                            #get the tile to swap with the dirt
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            #if we have dirt in our inventory
                            if inventory[ROCK] > 0:
                                #remove one dirt and place it
                                inventory[ROCK] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = ROCK
                        if (event.key == K_4):
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            if inventory[WOOD] > 0:
                                inventory[WOOD] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = WOOD
                        if (event.key == K_5):
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            if inventory[FIRE] > 0:
                                inventory[FIRE] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = FIRE
                        if (event.key == K_6):
                            currentTile = tilemap[playerPos[1]][playerPos[0]]
                            if inventory[BRICK] > 0:
                                inventory[BRICK] -= 1
                                tilemap[playerPos[1]][playerPos[0]] = BRICK

   #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))

    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    #display the inventory, starting 10 pixels in
    placePosition = 10
    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item],(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        #add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 50

    #update the display
    pygame.display.update()
