# Feb 6, 2026
# More Function excersizes
# pdfs/Exercises-functions 2026.pdf

# 6.

import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("calibri", 64)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 1000))
screen.fill("white")
running = True

def Text(font, col, txt, x, y):
    text_surface = font.render(txt, True, col)
    screen.blit(text_surface, (x, y))

def DrawFace(x, y, size, color):
    pygame.draw.circle(screen, color, (x, y), size, 1)
    pygame.draw.circle(screen, color, (x-size/2, y-size/2), size/5, 1)
    pygame.draw.circle(screen, color, (x+size/2, y-size/2), size/5, 1)
    pygame.draw.arc(screen, color, (x-size/2, y+size/2, size/2, size/4), 3, 0, 2)

DrawFace(500, 500, 50, "black")
Text(font, "green", "hello", 500, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()