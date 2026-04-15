"""
Program: Miku Paint Pro
Author: Justin Li
"""

# Imports
import pygame
import random
import os
import colorsys
import math
from tkinter import filedialog, Tk


# Stamps Paths
STAMP_PATHS = [
    r"./Assets/stamp0001.png",
    r"./Assets/stamp0011.png",
    r"./Assets/stamp0032.png",
    r"./Assets/stamp0088.png",
    r"./Assets/stamp0091.png"
]

# Assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURSOR_BASE = os.path.join(BASE_DIR, "Assets", "Cursors")
WALLPAPER_PATH = os.path.join(BASE_DIR, "Assets", "wallpaper.png")
LOGO_PATH = os.path.join(BASE_DIR, "Assets", "logo.png")
MUSIC_PATH = os.path.join(BASE_DIR, "Assets", "music.mp3")

# Inits
pygame.init()
pygame.font.init()

root = Tk()
root.withdraw()

# Screen Dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MIKU PAINT")


# Stock colors
TEAL = (57, 197, 187)      
PINK = (230, 57, 175)      
DARK_GREY = (30, 30, 30)   
HOVER_GREY = (80, 80, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PRESETS = [
    BLACK, WHITE, (255, 0, 0), (0, 255, 0), 
    (0, 0, 255), (255, 255, 0), TEAL, PINK
]


# Canvas inits
canvas_rect = pygame.Rect(200, 100, 950, 650)
canvas_surf = pygame.Surface((canvas_rect.width, canvas_rect.height))
canvas_surf.fill(WHITE)


# State variables
draw_color = TEAL
thickness = 5  
tool = "pencil"
filled = False
playing = True

undo_list = []
redo_list = []


# Picker States
picking_color = False
dragging_slider = False
color_wheel_radius = 100
picker_rect = pygame.Rect(WIDTH - 300, 390, 280, 350)
value_slider = 1.0 

# The default is teal
current_hue = 0.48
current_sat = 0.71


# Animated cursor init
# Cursor has three states:
# 1. Normal
# 2. Handwriting for when on the canvas
# 3. Link which is for hovering above buttons
cursor_dict = {"Normal": [], "Handwriting": [], "Link": []}
cursor_frame = 0
cursor_timer = 0
cursor_speed = 100 # ms per frame

# Fonts
font_title = pygame.font.SysFont("Arial Black", 36)
font_ui = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Arial", 14)
font_mono = pygame.font.SysFont("Courier", 14)


print(f"""
{'='*40}
    Welcome to MIKU PAINT PRO!!!
{'='*40}

[ CONTROLS ]
  - Left Click    : Draw / Use Tool / UI Interaction
  - Ctrl + Z      : Undo
  - Ctrl + Shift+Z: Redo
  - Ctrl + S      : Save Canvas
  - Ctrl + L      : Load Image to Canvas
  - Ctrl + F      : Toggle Shape Fill (Rect/Oval)
  - Up / Down     : Increase / Decrease Brush Size
  - P             : Toggle Music Play/Pause

[ TOOLS ]
  - Pencil, Brush, Eraser, Spray
  - Line, Rectangle, Oval
  - Custom Stamps (Sidebar)

{'='*40}
Ready to create with Miku! What will you make this time?
""")

# Play music
pygame.mixer.init()
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


# Helper functions ↓↓↓

# Create stamps
def create_stamps():
    # Init a list to store the stamps
    stamps = []
    for path in STAMP_PATHS:
        # Convert surface to alpha so it can be transparent
        img = pygame.image.load(path).convert_alpha()
        stamps.append(img)
    
    return stamps

# process and create wallpaper and logo surfaces
def load_visuals():

    # inits
    wallpaper = None
    logo = None

    # load into surface
    temp_wp = pygame.image.load(WALLPAPER_PATH).convert()
    wp_w, wp_h = temp_wp.get_size()

    # get aspect ratio
    wp_ratio = wp_w / wp_h
    
    # if it is longer than the screen
    if wp_ratio > 1200 / 800:
        new_h = 800
        # clamp
        new_w = int(new_h * wp_ratio)
    # if its wider than the screen
    else:
        new_w = 1200
        # clamp
        new_h = int(new_w / wp_ratio)
    
    # resizes the wallpaper to the window size
    temp_wp = pygame.transform.smoothscale(temp_wp, (new_w, new_h))
      
    # we set the starting point so that we put the center of the image in the center of the window
    # height and width subtracted by window divided by two essentially divided the extra space by 2, so half of the extra part gets left out on either side
    wallpaper = temp_wp.subsurface(((new_w - 1200) // 2, (new_h - 800) // 2, 1200, 800))

    # load logos
    temp_logo = pygame.image.load(LOGO_PATH).convert_alpha()
    logo_aspect = temp_logo.get_width() / temp_logo.get_height()
    # clamps the logo height to 50, multiplies the aspect ratio with 50 to get the shrinked width
    logo = pygame.transform.smoothscale(temp_logo, (int(50 * logo_aspect), 50))
    
    # load the cursor animation
    # the cursor animation is made up of a series of png images
    # first layer of for loop iterated through the subfolders under CURSOR_BASE, which is ./Assets/Cursors
    for mode in cursor_dict.keys():
        mode_path = os.path.join(CURSOR_BASE, mode)
        
        # iterate through the subfolder
        for filename in os.listdir(mode_path):
            if filename.endswith(".png"):
                # get the image from the file
                cursor_img = pygame.image.load(os.path.join(mode_path, filename)).convert_alpha()
                # shrink down to 44x44, and put into dict
                cursor_dict[mode].append(pygame.transform.scale(cursor_img, (44, 44)))
                
    return wallpaper, logo

# call the functions
master_stamps = create_stamps()
wallpaper, logo_img = load_visuals()

# Generate the color picking color wheel
def generate_color_wheel(radius):
    wheel = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    # iterate through all the possible points in the sequare containing the circle 
    for x in range(radius * 2):
        for y in range(radius * 2):

            # calculate the distance of the point to the center
            diff_x, diff_y = x - radius, y - radius
            dist = (diff_x**2 + diff_y**2)**0.5
            
            # check if the point is in the circle
            if dist <= radius:

                # calculate the angle of the point relative to a reference vector pointing to the right
                # python's angle_to generates angles in the range of -180 to 180
                # so we add 360 to make everything positive, then mod 360 to keep it in range
                angle = (pygame.math.Vector2(diff_x, diff_y).angle_to(pygame.math.Vector2(1, 0)) + 360) % 360
                # normalize angle into hue
                hue = angle / 360
                # same to saturation
                sat = dist / radius
                r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
                wheel.set_at((x, y), (int(r * 255), int(g * 255), int(b * 255), 255))
    return wheel


wheel_surf = generate_color_wheel(color_wheel_radius)


# time for UI
# this is where we draw all the UI
def draw_ui(mouse_x, mouse_y):
    # clear the entire screen
    if wallpaper:
        screen.blit(wallpaper, (0, 0))
    else:
        screen.fill(DARK_GREY)
    
    # draw the under rectangles of the UI stuff
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (20, 20, 20, 200), (10, 100, 170, 685), border_radius=15) 
    pygame.draw.rect(overlay, (20, 20, 20, 160), (10, 10, 480, 80), border_radius=15) 
    pygame.draw.rect(overlay, (20, 20, 20, 160), (190, 755, 970, 40), border_radius=10) 
    screen.blit(overlay, (0, 0))
    
    # Logo and Title
    title_x_offset = 25
    screen.blit(logo_img, (25, 25))
    title_x_offset += logo_img.get_width() + 15
    
    paint_txt = font_title.render("PAINT", True, TEAL)
    pro_txt = font_title.render(" PRO", True, PINK)
    screen.blit(paint_txt, (title_x_offset, 25))
    screen.blit(pro_txt, (title_x_offset + paint_txt.get_width(), 25))

    # Save and load buttons
    save_btn_rect = pygame.Rect(WIDTH - 160, 25, 140, 40)
    load_btn_rect = pygame.Rect(WIDTH - 320, 25, 140, 40)
    
    for button_rect, label_text in [(save_btn_rect, "SAVE (S)"), (load_btn_rect, "LOAD (L)")]:
        button_color = PINK
        if button_rect.collidepoint(mouse_x, mouse_y):
            button_color = (255, 150, 220)
            
        pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=12)
        
        btn_txt_surf = font_ui.render(label_text, True, BLACK)
        screen.blit(btn_txt_surf, (button_rect.centerx - btn_txt_surf.get_width() // 2, button_rect.centery - btn_txt_surf.get_height() // 2))

    # Tool Buttons, iterate over each
    tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]
    for i, tool_name in enumerate(tools_list):
        tool_rect = pygame.Rect(25, 110 + (i * 35), 140, 30)
        
        btn_color = (60, 60, 60)
        text_color = WHITE
        
        # If the current tool is this one
        if tool == tool_name: 
            btn_color = TEAL
            text_color = BLACK
        # If the mouse is hovering over this one
        elif tool_rect.collidepoint(mouse_x, mouse_y): 
            btn_color = HOVER_GREY
            text_color = WHITE


        pygame.draw.rect(screen, btn_color, tool_rect, border_radius=8)
        if tool == tool_name: 
            pygame.draw.rect(screen, WHITE, tool_rect, 2, border_radius=8)
            
        tool_label = font_ui.render(tool_name.upper(), True, text_color)
        screen.blit(tool_label, (tool_rect.centerx - tool_label.get_width() // 2, tool_rect.centery - tool_label.get_height() // 2))

    # Thickness
    thick_label_surf = font_ui.render(f"SIZE: {thickness}", True, TEAL)
    screen.blit(thick_label_surf, (25, 360))
    
    plus_rect = pygame.Rect(115, 355, 25, 25)
    minus_rect = pygame.Rect(145, 355, 25, 25)
    
    for control_rect, char in [(plus_rect, "+"), (minus_rect, "-")]:
        control_color = (70, 70, 70)
        if control_rect.collidepoint(mouse_x, mouse_y):
            control_color = HOVER_GREY
            
        pygame.draw.rect(screen, control_color, control_rect, border_radius=5)
        screen.blit(font_ui.render(char, True, WHITE), (control_rect.x + 6, control_rect.y + 2))

    # Sidebar Preview Box
    preview_box = pygame.Rect(25, 390, 140, 70)
    # Preview box background
    pygame.draw.rect(screen, (10, 10, 10), preview_box, border_radius=10)
    
    border_col = TEAL
    if tool == "eraser":
        border_col = PINK

    # Border
    pygame.draw.rect(screen, border_col, preview_box, 2, border_radius=10)
    
    # the preview
    if tool.startswith("stamp_"):
        stamp_idx = int(tool.split("_")[1])
        preview_stamp_img = pygame.transform.scale(master_stamps[stamp_idx], (40, 40))
        screen.blit(preview_stamp_img, (preview_box.centerx - 20, preview_box.centery - 20))
    else:
        prev_radius = max(2, min(30, thickness // 2))
        prev_color = draw_color
        if tool == "eraser":
            prev_color = WHITE 
        if tool == "pencil": 
            prev_radius = 2
        pygame.draw.circle(screen, prev_color, preview_box.center, prev_radius)

    # Stamps (same logic as buttons)
    stamp_header = font_ui.render("STAMPS", True, PINK)
    screen.blit(stamp_header, (25, 470))
    
    for i in range(5):
        stamp_btn_rect = pygame.Rect(25 + (i%2 * 75), 495 + (i//2 * 45), 60, 40)
        
        stamp_bg_color = (60, 60, 60)
        if tool == f"stamp_{i}": 
            stamp_bg_color = WHITE
        elif stamp_btn_rect.collidepoint(mouse_x, mouse_y): 
            stamp_bg_color = HOVER_GREY
            
        pygame.draw.rect(screen, stamp_bg_color, stamp_btn_rect, border_radius=8)
        stamp_icon = pygame.transform.scale(master_stamps[i], (32, 32))
        screen.blit(stamp_icon, (stamp_btn_rect.centerx - 16, stamp_btn_rect.centery - 16))

    # Color presets
    for i, preset_color in enumerate(PRESETS):
        preset_rect = pygame.Rect(200 + (i * 45), 760, 40, 30)
        pygame.draw.rect(screen, preset_color, preset_rect, border_radius=5)
        if draw_color == preset_color: 
            pygame.draw.rect(screen, WHITE, preset_rect, 3, border_radius=5)

    # Color pallete button
    color_trigger_rect = pygame.Rect(1000, 760, 150, 30)
    pygame.draw.rect(screen, draw_color, color_trigger_rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, color_trigger_rect, 2, border_radius=8)
    
    # Canvas Border
    pygame.draw.rect(screen, (0, 0, 0, 100), canvas_rect.inflate(14, 14), border_radius=12)
    pygame.draw.rect(screen, TEAL, canvas_rect.inflate(10, 10), 4, border_radius=10)


def draw_color_picker():
    # Requires a bit of math
    pygame.draw.rect(screen, (40, 40, 40), picker_rect, border_radius=15)
    pygame.draw.rect(screen, TEAL, picker_rect, 3, border_radius=15)
    
    # Init the wheel
    wheel_pos = (picker_rect.x + 20, picker_rect.y + 20)
    screen.blit(wheel_surf, wheel_pos)
    
    # The value slider
    slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
    pygame.draw.rect(screen, (20, 20, 20), slider_rect)

    # Draws the gradient white to black, iterates through each height, bottom to top
    for i in range(slider_rect.height):
        # The value is the ratio of the current height to the total, inverted
        # since i/slider_rect.height is from 1 to 0, but we want 0 to 1
        val = 1.0 - (i / slider_rect.height)
        pygame.draw.line(screen, (int(255 * val), int(255 * val), int(255 * val)), (slider_rect.left, slider_rect.top + i), (slider_rect.right, slider_rect.top + i))
    
    # the handle
    indicator_y = slider_rect.top + int((1.0 - value_slider) * slider_rect.height)
    pygame.draw.rect(screen, PINK, (slider_rect.left - 5, indicator_y - 2, slider_rect.width + 10, 4))
    
    close_txt_surf = font_small.render("CLICK OUTSIDE TO CLOSE", True, (150, 150, 150))
    screen.blit(close_txt_surf, (picker_rect.centerx - close_txt_surf.get_width() // 2, picker_rect.bottom - 25))


# saving and loading

def save_file():
    save_path = filedialog.asksaveasfilename(title="Save your Miku Art", defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if save_path: 
        pygame.image.save(canvas_surf, save_path)


def load_file():
    load_path = filedialog.askopenfilename(title="Load a Bitmap", filetypes=[("Image files", "*.png *.jpg *.bmp")])
    if load_path:
        loaded_img = pygame.image.load(load_path)
        canvas_surf.fill(WHITE) 
        scaled_img = pygame.transform.scale(loaded_img, (canvas_rect.width, canvas_rect.height))
        canvas_surf.blit(scaled_img, (0, 0))

# undo and redo
# we have two lists, undo and redo list
# when we draw, we take the current canvas layer and pushes it onto the undo list
# when we undo, we pop the last surface, draws it, and puts that surface onto the redo list
# when we redo, we pop the last surface on the redo list, draws it, and puts that onto the undo list
def perform_undo():
    global canvas_surf
    if undo_list:
        redo_list.append(canvas_surf.copy())
        canvas_surf = undo_list.pop()


def perform_redo():
    global canvas_surf
    if redo_list:
        undo_list.append(canvas_surf.copy())
        canvas_surf = redo_list.pop()

# this function just checks every frame to change the draw color based on hsv into rgb
def update_draw_color():
    global draw_color
    r, g, b = colorsys.hsv_to_rgb(current_hue, current_sat, value_slider)
    draw_color = (int(r * 255), int(g * 255), int(b * 255))


# RUNNING LOOP (YAY)

# Clock to sync frame rate
clock = pygame.time.Clock()
running = True

# mouse pos variable inits
mouse_x, mouse_y = 0, 0
last_mouse_x, last_mouse_y = 0, 0
start_x, start_y = 0, 0

while running:

    # Gets the time since last frame
    # this is used for cursor animation, since we need to run it at a constant rate
    delta_time = clock.tick(60)
    
    # update mouse pos
    last_mouse_x, last_mouse_y = mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    
    # Canvas pos
    rel_mouse_x, rel_mouse_y = mouse_x - canvas_rect.x, mouse_y - canvas_rect.y
    rel_old_mouse_x, rel_old_mouse_y = last_mouse_x - canvas_rect.x, last_mouse_y - canvas_rect.y

    # Event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:

            # collision detection
            if event.button == 1:
                # color picking (this if statement stops you from accedentally clicking on other ui when you try to exit)
                if picking_color:
                    # wheel coordinates relative to top-left of picker window
                    wheel_center = (picker_rect.x + 20 + color_wheel_radius, picker_rect.y + 20 + color_wheel_radius)
                    # Convert global mouse pos to start from the center of the wheel
                    diff_x, diff_y = mouse_x - wheel_center[0], mouse_y - wheel_center[1]
                    # pythag
                    dist_to_center = (diff_x**2 + diff_y**2)**0.5
                    
                    # check if mouse is in bound of the wheel
                    if dist_to_center <= color_wheel_radius:

                        # grab base color from wheel and update global H/S
                        raw_picked_color = wheel_surf.get_at((int(mouse_x - (picker_rect.x + 20)), int(mouse_y - (picker_rect.y + 20))))
                        # note: we drop the v because that is going to get fed from the slider
                        h, s, _ = colorsys.rgb_to_hsv(raw_picked_color.r / 255, raw_picked_color.g / 255, raw_picked_color.b / 255)
                        current_hue, current_sat = h, s
                        update_draw_color()
                    
                    # value slider "collider rect"
                    slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
                    if slider_rect.collidepoint(mouse_x, mouse_y):
                        dragging_slider = True
                    
                    if not picker_rect.collidepoint(mouse_x, mouse_y):
                        picking_color = False
                else:
                    # if clicking on the trigger, then open the menu
                    if pygame.Rect(1000, 760, 150, 30).collidepoint(mouse_x, mouse_y):
                        picking_color = True
                    
                    # save and load buttons 
                    if pygame.Rect(WIDTH - 160, 25, 140, 40).collidepoint(mouse_x, mouse_y): 
                        save_file()
                    if pygame.Rect(WIDTH - 320, 25, 140, 40).collidepoint(mouse_x, mouse_y): 
                        load_file()
                    
                    # if we are not drawing on the canvas
                    if not canvas_rect.collidepoint(mouse_x, mouse_y):
                        # sidebar
                        tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]

                        for i, tool_name in enumerate(tools_list):
                            if pygame.Rect(25, 110 + (i * 35), 140, 30).collidepoint(mouse_x, mouse_y):
                                tool = tool_name
                                
                        if pygame.Rect(115, 355, 25, 25).collidepoint(mouse_x, mouse_y): 
                            thickness = min(100, thickness + 1)
                        if pygame.Rect(145, 355, 25, 25).collidepoint(mouse_x, mouse_y): 
                            thickness = max(1, thickness - 1)
                            
                        for i in range(5):
                            if pygame.Rect(25 + (i%2 * 75), 495 + (i//2 * 45), 60, 40).collidepoint(mouse_x, mouse_y):
                                tool = f"stamp_{i}"
                                
                        #pPresets
                        for i, preset_color in enumerate(PRESETS):
                            if pygame.Rect(200 + (i * 45), 760, 40, 30).collidepoint(mouse_x, mouse_y):
                                draw_color = preset_color
                                h, s, v = colorsys.rgb_to_hsv(preset_color[0] / 255, preset_color[1] / 255, preset_color[2] / 255)
                                current_hue, current_sat, value_slider = h, s, v
                    else:
                        # if we are drawing, then save the surface onto undo so we can go back to this state
                        undo_list.append(canvas_surf.copy())
                        # clamp undo to save resources
                        if len(undo_list) > 30: 
                            undo_list.pop(0)
                        # clear redo because that branch is now stale (like git)
                        redo_list.clear()
                        # record the start position relative to the canvas
                        start_x, start_y = rel_mouse_x, rel_mouse_y

        # when the mouse button is lifted
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = False
                
                # Handle Shape Finalization
                if tool in ["line", "rect", "oval"] and canvas_rect.collidepoint(mouse_x, mouse_y) and not picking_color:
                    if tool == "line":
                        # get deltas
                        diff_x, diff_y = rel_mouse_x - start_x, rel_mouse_y - start_y
                        # pythag
                        dist = (diff_x**2 + diff_y**2)**0.5
                        
                        # Math to make sure we are making a line that is always consistenly in thickness no matter the angle
                        if dist > 0:
                            # calculate the distance the 4 points are from the actual start and end positions
                            # we achive this by first taking the perpendicuar coords (x, y) → (-y, x)
                            # then, we scale this using the ratio of the thickness/2 and our current sitance
                            # mathmatically, our original distance cnacelles out, leaving us with thickness/2, which is what we want
                            perp_x, perp_y = -diff_y * (thickness / 2) / dist, diff_x * (thickness / 2) / dist
                            
                            # define the 4 points of the polygon
                            poly_points = [
                                (start_x + perp_x, start_y + perp_y), 
                                (start_x - perp_x, start_y - perp_y), 
                                (rel_mouse_x - perp_x, rel_mouse_y - perp_y), 
                                (rel_mouse_x + perp_x, rel_mouse_y + perp_y)
                            ]
                            # draws it
                            pygame.draw.polygon(canvas_surf, draw_color, poly_points)
                        
                        # Draws circle caps, looks nicer
                        pygame.draw.circle(canvas_surf, draw_color, (start_x, start_y), thickness // 2)
                        pygame.draw.circle(canvas_surf, draw_color, (rel_mouse_x, rel_mouse_y), thickness // 2)
                    
                    elif tool == "rect":
                        shape_rect = pygame.Rect(start_x, start_y, rel_mouse_x - start_x, rel_mouse_y - start_y)
                        # normalize to make sure we don;t have negative deltas
                        shape_rect.normalize()

                        if filled: 
                            pygame.draw.rect(canvas_surf, draw_color, shape_rect)
                        else: 
                            pygame.draw.rect(canvas_surf, draw_color, shape_rect, thickness)
                            
                    elif tool == "oval":
                        shape_rect = pygame.Rect(start_x, start_y, rel_mouse_x - start_x, rel_mouse_y - start_y)
                        shape_rect.normalize()
                        if shape_rect.width > thickness and shape_rect.height > thickness:
                            if filled: 
                                pygame.draw.ellipse(canvas_surf, draw_color, shape_rect)
                            else: 
                                pygame.draw.ellipse(canvas_surf, draw_color, shape_rect, thickness)

        # Shortcuts
        if event.type == pygame.KEYDOWN:
            # Music short cut
            if event.key == pygame.K_p:
                playing = not playing
                if playing:
                    print("play")
                    pygame.mixer.music.unpause()
                else:
                    print("pause")
                    pygame.mixer.music.pause()
            # The get_mods() function returns a bitmask of the modifer keys (shift, ctl, alt, etc)
            key_mods = pygame.key.get_mods()
            # we then AND this with the ctrl key to get whether its pressed down
            if (key_mods & pygame.KMOD_CTRL):
                # undo and redo
                if event.key == pygame.K_z:
                    if (key_mods & pygame.KMOD_SHIFT): 
                        perform_redo()
                    else: 
                        perform_undo()
                
                # save
                if event.key == pygame.K_s: 
                    save_file()
                # load
                if event.key == pygame.K_l: 
                    load_file()
                # filled shapes
                if event.key == pygame.K_f: 
                    filled = not filled
            
            # change brush size
            if event.key == pygame.K_UP: 
                thickness = min(100, thickness + 1)
            if event.key == pygame.K_DOWN: 
                thickness = max(1, thickness - 1)

    # update the color picker slider
    if picking_color and dragging_slider:
        slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
        # we only update the value slider y if we are dragging it
        value_slider = 1.0 - ((mouse_y - slider_rect.top) / slider_rect.height)
        value_slider = max(0, min(1, value_slider))
        update_draw_color()

    # rendering
    draw_ui(mouse_x, mouse_y) 
    screen.blit(canvas_surf, (canvas_rect.x, canvas_rect.y))


    if picking_color:
        draw_color_picker()
    elif canvas_rect.collidepoint(mouse_x, mouse_y):

        if tool.startswith("stamp_"):
            stamp_idx = int(tool.split("_")[1])
            stamp_size = thickness * 5
            # blits ghost preview onto the screen
            ghost_stamp = pygame.transform.scale(master_stamps[stamp_idx], (int(stamp_size), int(stamp_size)))
            ghost_stamp.set_alpha(150)
            screen.blit(ghost_stamp, (mouse_x - stamp_size // 2, mouse_y - stamp_size // 2))
            
        elif tool == "brush":
            pygame.draw.circle(screen, draw_color, (mouse_x, mouse_y), thickness // 2, 1)
        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), (thickness * 4) // 2, 1)
        elif tool == "pencil":
            pygame.draw.circle(screen, draw_color, (mouse_x, mouse_y), 2, 1)
        elif tool in ["line", "rect", "oval", "spray"]:
            pygame.draw.line(screen, BLACK, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 1)
            pygame.draw.line(screen, BLACK, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 1)
    
    # drawing
    if mouse_buttons[0] and canvas_rect.collidepoint(mouse_x, mouse_y) and not picking_color:
        if tool == "pencil":
            pygame.draw.line(canvas_surf, draw_color, (rel_old_mouse_x, rel_old_mouse_y), (rel_mouse_x, rel_mouse_y), 1)
            
        elif tool in ["brush", "eraser"]:
            draw_col = draw_color
            if tool == "eraser":
                draw_col = WHITE
                
            draw_thick = thickness
            if tool == "eraser":
                draw_thick = thickness * 1.5
                
            diff_x, diff_y = rel_mouse_x - rel_old_mouse_x, rel_mouse_y - rel_old_mouse_y
            dist = (diff_x**2 + diff_y**2)**0.5
            
            if dist > 0:
                perp_x, perp_y = -diff_y * (draw_thick / 2) / dist, diff_x * (draw_thick / 2) / dist
                bridge_points = [
                    (rel_old_mouse_x + perp_x, rel_old_mouse_y + perp_y), 
                    (rel_old_mouse_x - perp_x, rel_old_mouse_y - perp_y), 
                    (rel_mouse_x - perp_x, rel_mouse_y - perp_y), 
                    (rel_mouse_x + perp_x, rel_mouse_y + perp_y)
                ]
                pygame.draw.polygon(canvas_surf, draw_col, bridge_points)
            pygame.draw.circle(canvas_surf, draw_col, (rel_mouse_x, rel_mouse_y), draw_thick // 2)
            
        elif tool == "spray":
            for _ in range(thickness // 2 + 5):
                # choose random point
                rand_x, rand_y = random.randint(-thickness, thickness), random.randint(-thickness, thickness)
                # check if its in bounds
                if rand_x**2 + rand_y**2 <= thickness**2:
                    # if the random position is inside the canvas
                    if 0 <= rel_mouse_x + rand_x < canvas_rect.width and 0 <= rel_mouse_y + rand_y < canvas_rect.height:
                        canvas_surf.set_at((rel_mouse_x + rand_x, rel_mouse_y + rand_y), draw_color)
        
        elif tool.startswith("stamp_"):
            stamp_idx = int(tool.split("_")[1])
            stamp_size = thickness * 5
            stamp_img = pygame.transform.scale(master_stamps[stamp_idx], (int(stamp_size), int(stamp_size)))
            canvas_surf.blit(stamp_img, (rel_mouse_x - stamp_size // 2, rel_mouse_y - stamp_size // 2))
            
        elif tool in ["line", "rect", "oval"]:
            # these are screen previews, because how these tools work, they can only be finalized when you lift the mouse
            if tool == "line":
                start_scr_x, start_scr_y = start_x + canvas_rect.x, start_y + canvas_rect.y
                diff_x, diff_y = mouse_x - start_scr_x, mouse_y - start_scr_y
                dist = (diff_x**2 + diff_y**2)**0.5
                
                if dist > 0:
                    perp_x, perp_y = -diff_y * (thickness / 2) / dist, diff_x * (thickness / 2) / dist
                    poly_points = [
                        (start_scr_x + perp_x, start_scr_y + perp_y), 
                        (start_scr_x - perp_x, start_scr_y - perp_y), 
                        (mouse_x - perp_x, mouse_y - perp_y), 
                        (mouse_x + perp_x, mouse_y + perp_y)
                    ]
                    pygame.draw.polygon(screen, draw_color, poly_points)
                pygame.draw.circle(screen, draw_color, (start_scr_x, start_scr_y), thickness // 2)
                pygame.draw.circle(screen, draw_color, (mouse_x, mouse_y), thickness // 2)
                
            elif tool == "rect":
                preview_rect = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mouse_x - (start_x + canvas_rect.x), mouse_y - (start_y + canvas_rect.y))
                preview_rect.normalize()
                if filled: 
                    pygame.draw.rect(screen, draw_color, preview_rect)
                else: 
                    pygame.draw.rect(screen, draw_color, preview_rect, thickness)
                    
            elif tool == "oval":
                preview_rect = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mouse_x - (start_x + canvas_rect.x), mouse_y - (start_y + canvas_rect.y))
                preview_rect.normalize()
                if preview_rect.width > thickness and preview_rect.height > thickness:
                    if filled: 
                        pygame.draw.ellipse(screen, draw_color, preview_rect)
                    else: 
                        pygame.draw.ellipse(screen, draw_color, preview_rect, thickness)


    pygame.mouse.set_visible(False)
    current_mode = "Normal"
    
    if canvas_rect.collidepoint(mouse_x, mouse_y): 
        current_mode = "Handwriting"
    elif (mouse_x < 200 or mouse_y < 100 or mouse_y > 750 or mouse_x > 1150): 
        current_mode = "Link"
    
    cursor_timer += delta_time
    if cursor_timer > cursor_speed:
        cursor_timer = 0
        if cursor_dict[current_mode]: 
            cursor_frame = (cursor_frame + 1) % len(cursor_dict[current_mode])
    
    if cursor_dict[current_mode]:
        screen.blit(cursor_dict[current_mode][cursor_frame % len(cursor_dict[current_mode])], (mouse_x, mouse_y))
    else: 
        pygame.draw.circle(screen, BLACK, (mouse_x, mouse_y), 2)

    coord_info_surf = font_mono.render(f"Pos: {rel_mouse_x}, {rel_mouse_y} | Tool: {tool} | Size: {thickness} | Ctrl+Z: Undo", True, WHITE)
    screen.blit(coord_info_surf, (200, 740))
    pygame.display.flip()

pygame.quit()