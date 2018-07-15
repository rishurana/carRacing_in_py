import pygame as pg
import time
import random

pg.init()

crashAudio = pg.mixer.Sound("crashAudios.wav")
pg.mixer.music.load("carCrash.mp3")

dWidth = 800
dHeight = 600

cWidth = 70

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0,0,255)
green = (0,200,0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

gameDisplay = pg.display.set_mode((dWidth,dHeight))
pg.display.set_caption("racing game")
clock = pg.time.Clock()

carImg = pg.image.load('car.png')
pause = False

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def styleObject(text, font):
    textSurface = font.render(text, True, black)
    return textSurface ,textSurface.get_rect()



def showMessage(text):
    beauty_text = pg.font.Font('freesansbold.ttf',115)
    TextSurf, TextRact = styleObject(text , beauty_text)
    TextRact.center = ((dWidth/2),(dHeight/2))
    gameDisplay.blit(TextSurf, TextRact)
    pg.display.update()
    time.sleep(2)
    gameloop()

def crash():

    pg.mixer.music.stop()
    pg.mixer.Sound.play(crashAudio)

    beauty_text = pg.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRact = styleObject("You Crashed", beauty_text)
    TextRact.center = ((dWidth / 2), (dHeight / 2))
    gameDisplay.blit(TextSurf, TextRact)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit()

        # button(msg, x, y, w, h, ac, ic):
        button("Replay", 150, 450, 100, 50, bright_green, green, gameloop)
        button("Quit", 550, 450, 100, 50, bright_red, red, gameExit)

        pg.display.update()
        clock.tick(15)

def gameExit():
    pg.quit()
    quit()

def obstacle_dodged(count):
    font = pg.font.SysFont(None, 25)
    text = font.render("Dodged : "+str(count), True, black)
    gameDisplay.blit(text, (5,5))

def obstacle(obstacle_x ,obstacle_y, obstacle_w, obstacle_h, color):
    pg.draw.rect(gameDisplay, color, [obstacle_x, obstacle_y, obstacle_w, obstacle_h])

def button(msg, x, y, w, h, ac, ic, action = None):
    mouse = pg.mouse.get_pos()

    click = pg.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pg.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pg.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = styleObject(msg, smallText)
    textRect.center = (x + (w / 2), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def resume():
    global pause

    pg.mixer.music.resume()

    pause = False

def paused():

    pg.mixer.music.pause()


    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit()
        gameDisplay.fill(white)
        beauty_text = pg.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRact = styleObject("Paused", beauty_text)
        TextRact.center = ((dWidth / 2), (dHeight / 2))
        gameDisplay.blit(TextSurf, TextRact)

        #button(msg, x, y, w, h, ac, ic):
        button("continue", 150, 450, 100, 50, bright_green, green, resume)
        button("Quit", 550, 450, 100, 50, bright_red, red, gameExit)

        pg.display.update()
        clock.tick(15)

def introduction():

    intro = True

    while intro:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit()
        gameDisplay.fill(white)
        beauty_text = pg.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRact = styleObject("Race Game", beauty_text)
        TextRact.center = ((dWidth / 2), (dHeight / 2))
        gameDisplay.blit(TextSurf, TextRact)

        #button(msg, x, y, w, h, ac, ic):
        button("GO!", 150, 450, 100, 50, bright_green, green, gameloop)
        button("Quit", 550, 450, 100, 50, bright_red, red, gameExit)

        pg.display.update()
        clock.tick(15)

def gameloop():

    pg.mixer.music.play(-1)

    x = (dWidth * 0.45)
    y = (dHeight * 0.75)

    x_change=0

    obstacle_startx = random.randrange(0,dWidth-100)
    obstacle_starty = -600
    obstacle_speed = 8
    obstacle_width = 100
    obstacle_hight = 100

    dodged_object = 0
    increment = 0
    counter = 0
    global pause

    gameExit = False

    while not gameExit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit()
            #print(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_change = -(10+increment)
                if event.key == pg.K_RIGHT:
                    x_change = (10+increment)
                if event.key == pg.K_p:
                    pause = True
                    paused()
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    x_change = 0


        x += x_change
        gameDisplay.fill(white)

        #def obstacle(obstacle_x, obstacle_y, obstacle_w, obstacle_h, color):
        obstacle(obstacle_startx, obstacle_starty, obstacle_width, obstacle_hight, black)
        obstacle_starty += obstacle_speed

        car(x,y)
        obstacle_dodged(dodged_object)

        if x>dWidth-cWidth or x<0:
            crash()

        if obstacle_starty > dHeight:
            obstacle_starty = 0 - obstacle_hight
            obstacle_startx = random.randrange(0,dWidth-obstacle_width)
            dodged_object += 1
            counter += 1
            if counter == 5:
                if obstacle_speed < 12:
                    obstacle_speed += 1
                    increment += .5
                if obstacle_width < 250:
                    obstacle_width += 3
                counter = 0


        if y < obstacle_starty + obstacle_hight:
            if x+cWidth > obstacle_startx and x < obstacle_startx + obstacle_width:
                crash()


        pg.display.update()
        clock.tick(60)
introduction()
gameloop()
gameExit()
