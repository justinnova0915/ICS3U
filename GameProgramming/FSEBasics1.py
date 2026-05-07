'''
Main GAme LOOP will always look similar to this:

While running:
    get input from the user
    move good guy (only moving!!! not drawing!!!)
    move bad guys (only moving!!! not drawing!!!)
    move other stuff (only moving!!! not drawing!!!)
    check interactions
    draw scene (the ENTIRE drawing cdeo goes here)
    delay (60 fps)
'''



from pygame import *
import math

width,height=800,600
screen=display.set_mode((width,height))
red=(255,0,0)
grey=(127,127,127)
black=(0,0,0)
blue=(0,0,255)
green=(0,255,0)
yellow=(255,255,0)
white=(255,255,255)
myClock=time.Clock()

def drawScene(badGuys, gx, gy):
    screen.fill(black)
    draw.circle(screen, green, (mx, my), 35)

    for en in enemies:
        draw.circle(screen, red, (en[0], en[1]), 25)

def moveEnemies(badGuys, gx, gy):
    for guy in badGuys:
        if guy[0] < gx:
            guy[0] += SPEED
        if guy[0] > gx:
            guy[0] -= SPEED
        if guy[1] < gy:
            guy[1] += SPEED
        if guy[1] > gy:
            guy[1] -= SPEED

def checkHits(badGuys, gx, gy):
    for i in range(len(badGuys)):
        d = math.sqrt((gx-badGuys[i][0])**2+(gy-badGuys[i][1])**2)
        if d < 50:
            badGuys[i][0] = 150+i*100
            badGuys[i][1] = 20

running=True

SPEED = 2

ex, ey = 0, 0

enemies = [[150+i*100,20] for i in range(6)]

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    
    drawScene(enemies, mx, my)
    moveEnemies(enemies, mx, my)

    myClock.tick(60)
    display.flip()
            
quit()