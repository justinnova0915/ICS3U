from pygame import *

width,height=800,600
screen=display.set_mode((width,height))
green=(0,255,0)
myClock=time.Clock()



running=True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
               
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    if mb[0]:
        draw.polygon(screen, green, [(mx, my), (mx+30, my+30), (mx-30, my+30)], 3)
    elif mb[2]:
        draw.polygon(screen, green, [(mx, my), (mx+30, my-30), (mx-30, my-30)], 3)
      
    myClock.tick(60)
    display.flip()
            
quit()