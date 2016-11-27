# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:14:08 2016

@author: Askanio
"""

import pygame
import time
import random

pygame.init()
#Defining colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
#Defining resolution
display_width = 800
display_height = 600
#Defining blocks size
block_size = 20
AppleThickness = 30
#Game display size
gameDisplay = pygame.display.set_mode((display_width,display_height))
#Game name & game icon (will be displayed on game window)
pygame.display.set_caption('Slither')
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
#loading snakeheadsprite
img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple.png')
#defining clock as pygame in-built function
clock = pygame.time.Clock()
FPS = 15
#setting snakehead spawndirection
direction = "right"

#Rounding function to the next 10s so stuff will be perfectly alligned
def roundToNextTen(n):
    """This function will round int to nearest 10 usefull when"""
    return round(n/10.0)*10.0
#Drawing snake
def snake(block_size, snakelist):
    
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        
    gameDisplay.blit(head,(snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])
 
#Defining a functions to print message to the sreen
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
    
smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          size = "large")
        message_to_screen("Press C to continie or Q to quit.",
                          black,
                          25)
        pygame.display.update()
        clock.tick(5)
        
def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = roundToNextTen(random.randrange(0,display_width-AppleThickness))
    randAppleY = roundToNextTen(random.randrange(0,display_height-AppleThickness))
    return randAppleX,randAppleY

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        message_to_screen("If you run into yourself, or edges, you die!",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          black,
                          180)
        pygame.display.update()
        clock.tick(15)

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg ,color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)
    #screen_text = font.render(msg,True,color)
    #gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    
#Main Loop
def gameLoop():
    global direction
    direction = "right"
    running = True
    gameOver = False
    snakelist = []
    snakeLength = 1
    #Head of the snake
    lead_x = display_width/2
    lead_y = display_height/2
    #The change in coordinates
    lead_x_change = 10
    lead_y_change = 0
    #Apple coordinates 
    randAppleX, randAppleY = randAppleGen()
    while running:
        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over", 
                              red, 
                              -50, 
                              size = "large")
            message_to_screen("Press C to play again or Q to quit", 
                              black, 
                              50, 
                              size = "medium")
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        #detecting collision and quiting the game
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
             gameOver = True
             
        #Checking for events
        for event in pygame.event.get():
            #Moving the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_p:
                    pause()
            #Stop movement when key is not pressed down (too easy for a snake game)
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    #lead_x_change = 0
        
            #Quiting the game
            if event.type == pygame.QUIT:
                running = False
                
        #Each itteration the X coordinate is changed
        lead_x += lead_x_change
        lead_y += lead_y_change
        #Changing color of display
        gameDisplay.fill(white)
        
        #Rendering graphics
        #pygame.draw.rect(gameDisplay, red, [randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(appleimg, (randAppleX,randAppleY))
        #Snake
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakelist.append(snakeHead)
        
        if len(snakelist) > snakeLength:
            del snakelist[0]
        
        #Detecting Head collisions with other parts of snake
        for eachSegment in snakelist[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
                
        snake(block_size, snakelist)
        
        #gameDisplay.fill(red, rect = [200,200,50,50]) - alternitive way to draw rects       
        score(snakeLength-1)
        pygame.display.update()
        #Updating clock No. of ticks = FPS
        
#        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness:
#            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
#                snakeLength += 1
#                randAppleX = random.randrange(0,display_width-AppleThickness)
#                randAppleY = random.randrange(0,display_height-AppleThickness)
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:  
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
               snakeLength += 1
               randAppleX, randAppleY = randAppleGen()
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                snakeLength += 1
                randAppleX, randAppleY = randAppleGen()
            
        clock.tick(FPS)
    pygame.quit()
    quit()
    
game_intro()         
gameLoop()            
          

