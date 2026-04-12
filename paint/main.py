import pygame

# Surface init
screen = pygame.display.set_mode((1920, 1080))
canvas = pygame.Surface((980, 980))
preview = pygame.Surface((980, 980), pygame.SRCALPHA)
canvas.fill("white")
screen.fill("azure")
preview.fill((0, 0, 0, 0))

# Clock init
clock = pygame.time.Clock()

# Flags
running = True
LeftMouseButtonDown = False
RightMouseButtonDown = False
InCanvas = False

tools = ["pencil", "shape", "eraser", "stamp", "load", "eyedropper"]
tool_thickness = {
    "pencil" : 5,
    "eraser" : 5,
    "stamp"  : 5
}

tool = tools[0]

# Prev mouse pos init
PREV_MOUSE_X, PREV_MOUSE_Y = pygame.mouse.get_pos()

# Game loop
while running:

    # State checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LeftMouseButtonDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            LeftMouseButtonDown = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                tool = tools[0]
            elif event.key == pygame.K_s:
                tool = tools[1]
            elif event.key == pygame.K_e:
                tool = tools[2]
            elif event.key == pygame.K_t:
                tool = tools[3]
            elif event.key == pygame.K_d:
                tool = tools[5]
            elif event.key == pygame.K_LEFTBRACKET and tool in tool_thickness:
                tool_thickness[tool] = max(1, tool_thickness[tool] - 1)
            elif event.key == pygame.K_RIGHTBRACKET and tool in tool_thickness:
                tool_thickness[tool] = min(50, tool_thickness[tool] + 1)
            
    preview.fill((0, 0, 0, 0))

    # Get Mouse Pos
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
    CANVAS_POS = (MOUSE_X - 890, MOUSE_Y - 50)

    InCanvas = pygame.Rect(890, 50, 980, 980).collidepoint(MOUSE_X, MOUSE_Y)
    


    # Drawing
    if InCanvas:
        if tool == "pencil":
            if LeftMouseButtonDown:
                pygame.draw.circle(canvas, "red", CANVAS_POS, tool_thickness["pencil"]/2)
                pygame.draw.line(canvas, "red", CANVAS_POS, PREV_CANVAS_POS, tool_thickness["pencil"])
            else:
                pygame.draw.circle(preview, "black", CANVAS_POS, tool_thickness["pencil"]/2, 1)
        elif tool == "shape":
            if LeftMouseButtonDown:
                pygame.draw
        elif tool == "eraser":
            if LeftMouseButtonDown:
                pygame.draw.circle(canvas, "white", CANVAS_POS, tool_thickness["eraser"]/2)
                pygame.draw.line(canvas, "white", CANVAS_POS, PREV_CANVAS_POS, tool_thickness["eraser"])
            else:
                pygame.draw.circle(preview, "black", CANVAS_POS, tool_thickness["eraser"]/2, 1)
        elif tool == "shape":
            pass
        

    # Update prev pos
    PREV_MOUSE_X, PREV_MOUSE_Y = MOUSE_X, MOUSE_Y
    PREV_CANVAS_POS = (PREV_MOUSE_X - 890, PREV_MOUSE_Y - 50)
    
    # Blits
    screen.blit(canvas, (890, 50))
    screen.blit(preview, (890, 50))


    pygame.display.flip()
    clock.tick(120)

pygame.quit()
