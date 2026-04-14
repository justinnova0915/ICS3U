"""
Program: Miku Paint Pro (Pygame Edition)
Author: Justin Li
"""

import pygame
import random
import os
import colorsys
import math
from tkinter import filedialog, Tk

# --- SETTINGS & PATHS ---
STAMP_PATHS = [
    r"./Assets/stamp0001.png",
    r"./Assets/stamp0011.png",
    r"./Assets/stamp0032.png",
    r"./Assets/stamp0088.png",
    r"./Assets/stamp0091.png"
]

# Assets for visual overhaul
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURSOR_BASE = os.path.join(BASE_DIR, "Assets", "Cursors")
WALLPAPER_PATH = os.path.join(BASE_DIR, "Assets", "wallpaper.png")
LOGO_PATH = os.path.join(BASE_DIR, "Assets", "logo.png")
MUSIC_PATH = os.path.join(BASE_DIR, "Assets", "music.mp3")

# --- INITIALIZATION ---
pygame.init()
pygame.font.init()


root = Tk()
root.withdraw()

# Screen Dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MIKU PAINT")

# --- COLORS ---
TEAL = (57, 197, 187)      
PINK = (230, 57, 175)      
DARK_GREY = (30, 30, 30)   
HOVER_GREY = (80, 80, 80) # New color for Hover state
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PRESETS = [BLACK, WHITE, (255,0,0), (0,255,0), (0,0,255), (255,255,0), TEAL, PINK]

# --- CANVAS SETUP ---
canvas_rect = pygame.Rect(200, 100, 950, 650)
canvas_surf = pygame.Surface((canvas_rect.width, canvas_rect.height))
canvas_surf.fill(WHITE)

# --- GLOBAL VARIABLES ---
draw_color = TEAL
thickness = 5  
tool = "pencil"
filled = False
undo_list = []
redo_list = []

# Picker States
picking_color = False
dragging_slider = False
color_wheel_radius = 100
picker_rect = pygame.Rect(WIDTH - 300, 390, 280, 350)
value_slider = 1.0 
current_hue = 0.48  # Default for Teal
current_sat = 0.71  # Default for Teal

# Cursor Animation State
cursor_dict = {"Normal": [], "Handwriting": [], "Link": []}
cur_frame = 0
cur_timer = 0
cur_speed = 100 # ms per frame

# Fonts
font_title = pygame.font.SysFont("Arial Black", 36)
font_ui = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Arial", 14)
font_mono = pygame.font.SysFont("Courier", 14)

# Music init
pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Load assets
def create_stamps():
    stamps = []
    for path in STAMP_PATHS:
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                stamps.append(img)
            except pygame.error:
                s = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(s, PINK, (0, 0, 100, 100), 5)
                stamps.append(s)
        else:
            s = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.rect(s, PINK, (0, 0, 100, 100), 2)
            txt = font_title.render("?", True, PINK)
            s.blit(txt, (35, 25))
            stamps.append(s)
    return stamps

def load_visuals():
    wp, lg = None, None
    if os.path.exists(WALLPAPER_PATH):
        try:
            temp = pygame.image.load(WALLPAPER_PATH).convert()
            w, h = temp.get_size()
            ratio = w/h
            if ratio > 1200/800:
                nh = 800; nw = int(nh * ratio)
            else:
                nw = 1200; nh = int(nw / ratio)
            temp = pygame.transform.smoothscale(temp, (nw, nh))
            wp = temp.subsurface(((nw-1200)//2, (nh-800)//2, 1200, 800))
        except: pass
    if os.path.exists(LOGO_PATH):
        try:
            temp = pygame.image.load(LOGO_PATH).convert_alpha()
            aspect = temp.get_width() / temp.get_height()
            lg = pygame.transform.smoothscale(temp, (int(50 * aspect), 50))
        except: pass
    
    for mode in cursor_dict.keys():
        path = os.path.join(CURSOR_BASE, mode)
        if os.path.exists(path):
            files = sorted([f for f in os.listdir(path) if f.endswith(".png")])
            for f in files:
                img = pygame.image.load(os.path.join(path, f)).convert_alpha()
                cursor_dict[mode].append(pygame.transform.scale(img, (44, 44)))
    return wp, lg

master_stamps = create_stamps()
wallpaper, logo_img = load_visuals()

def generate_color_wheel(radius):
    wheel = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for x in range(radius * 2):
        for y in range(radius * 2):
            dx, dy = x - radius, y - radius
            dist = (dx**2 + dy**2)**0.5
            if dist <= radius:
                angle = (pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0)) + 360) % 360
                hue = angle / 360
                sat = dist / radius
                r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
                wheel.set_at((x, y), (int(r*255), int(g*255), int(b*255), 255))
    return wheel

wheel_surf = generate_color_wheel(color_wheel_radius)

# --- UI FUNCTIONS ---
def draw_ui(mx, my):
    if wallpaper: screen.blit(wallpaper, (0, 0))
    else: screen.fill(DARK_GREY)
    
    # Frosted glass overlay
    glass = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(glass, (20, 20, 20, 200), (10, 100, 170, 685), border_radius=15) # Sidebar
    pygame.draw.rect(glass, (20, 20, 20, 160), (10, 10, 480, 80), border_radius=15) # Header
    pygame.draw.rect(glass, (20, 20, 20, 160), (190, 755, 970, 40), border_radius=10) # Palette
    screen.blit(glass, (0, 0))
    
    # Logo and Title
    x_off = 25
    if logo_img:
        screen.blit(logo_img, (25, 25))
        x_off += logo_img.get_width() + 15
    
    paint_txt = font_title.render("PAINT", True, TEAL)
    pro_txt = font_title.render(" PRO", True, PINK)
    screen.blit(paint_txt, (x_off, 25))
    screen.blit(pro_txt, (x_off + paint_txt.get_width(), 25))

    # Save/Load with Hover Highlighting
    save_btn_rect = pygame.Rect(WIDTH - 160, 25, 140, 40)
    load_btn_rect = pygame.Rect(WIDTH - 320, 25, 140, 40)
    
    for r, txt in [(save_btn_rect, "SAVE (S)"), (load_btn_rect, "LOAD (L)")]:
        color = (255, 150, 220) if r.collidepoint(mx, my) else PINK
        pygame.draw.rect(screen, color, r, border_radius=12)
        pygame.draw.rect(screen, WHITE, r, 2, border_radius=12)
        btn_txt = font_ui.render(txt, True, BLACK)
        screen.blit(btn_txt, (r.centerx - btn_txt.get_width()//2, r.centery - btn_txt.get_height()//2))

    # Tool Buttons with 3-State Highlighting
    tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]
    for i, t in enumerate(tools_list):
        t_rect = pygame.Rect(25, 110 + (i * 35), 140, 30)
        if tool == t: color, txt_color = TEAL, BLACK
        elif t_rect.collidepoint(mx, my): color, txt_color = HOVER_GREY, WHITE
        else: color, txt_color = (60, 60, 60), WHITE

        pygame.draw.rect(screen, color, t_rect, border_radius=8)
        if tool == t: pygame.draw.rect(screen, WHITE, t_rect, 2, border_radius=8)
        txt = font_ui.render(t.upper(), True, txt_color)
        screen.blit(txt, (t_rect.centerx - txt.get_width()//2, t_rect.centery - txt.get_height()//2))

    # Thickness Control
    thick_label = font_ui.render(f"SIZE: {thickness}", True, TEAL)
    screen.blit(thick_label, (25, 360))
    plus_rect = pygame.Rect(115, 355, 25, 25)
    minus_rect = pygame.Rect(145, 355, 25, 25)
    for r, char in [(plus_rect, "+"), (minus_rect, "-")]:
        color = HOVER_GREY if r.collidepoint(mx, my) else (70, 70, 70)
        pygame.draw.rect(screen, color, r, border_radius=5)
        screen.blit(font_ui.render(char, True, WHITE), (r.x + 6, r.y + 2))

    # Sidebar Preview Box
    preview_box = pygame.Rect(25, 390, 140, 70)
    pygame.draw.rect(screen, (10, 10, 10), preview_box, border_radius=10)
    pygame.draw.rect(screen, TEAL if tool != "eraser" else PINK, preview_box, 2, border_radius=10)
    
    if tool.startswith("stamp_"):
        idx = int(tool.split("_")[1])
        p_size = 40
        p_img = pygame.transform.scale(master_stamps[idx], (int(p_size), int(p_size)))
        screen.blit(p_img, (preview_box.centerx - 20, preview_box.centery - 20))
    else:
        p_radius = max(2, min(30, thickness // 2))
        if tool == "eraser":
            p_color = WHITE 
        else:
            p_color = draw_color
        if tool == "pencil": 
            p_radius = 2
        pygame.draw.circle(screen, p_color, preview_box.center, p_radius)

    # Stamps with 3-State Highlighting
    stamp_header = font_ui.render("STAMPS", True, PINK)
    screen.blit(stamp_header, (25, 470))
    for i in range(5):
        s_rect = pygame.Rect(25 + (i%2 * 75), 495 + (i//2 * 45), 60, 40)
        if tool == f"stamp_{i}": 
            color = WHITE
        elif s_rect.collidepoint(mx, my): 
            color = HOVER_GREY
        else: 
            color = (60, 60, 60)
        pygame.draw.rect(screen, color, s_rect, border_radius=8)
        icon = pygame.transform.scale(master_stamps[i], (32, 32))
        screen.blit(icon, (s_rect.centerx - 16, s_rect.centery - 16))

    # Color Palette (Presets)
    for i, c in enumerate(PRESETS):
        c_rect = pygame.Rect(200 + (i * 45), 760, 40, 30)
        pygame.draw.rect(screen, c, c_rect, border_radius=5)
        if draw_color == c: pygame.draw.rect(screen, WHITE, c_rect, 3, border_radius=5)

    # Current Color Preview Trigger
    color_trigger_rect = pygame.Rect(1000, 760, 150, 30)
    pygame.draw.rect(screen, draw_color, color_trigger_rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, color_trigger_rect, 2, border_radius=8)
    
    # Canvas Border
    pygame.draw.rect(screen, (0, 0, 0, 100), canvas_rect.inflate(14, 14), border_radius=12)
    pygame.draw.rect(screen, TEAL, canvas_rect.inflate(10, 10), 4, border_radius=10)

def draw_color_picker():
    """Renders the HSV color wheel popup directly above the trigger"""
    pygame.draw.rect(screen, (40, 40, 40), picker_rect, border_radius=15)
    pygame.draw.rect(screen, TEAL, picker_rect, 3, border_radius=15)
    
    # Wheel
    wheel_pos = (picker_rect.x + 20, picker_rect.y + 20)
    screen.blit(wheel_surf, wheel_pos)
    
    # Slider
    slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
    pygame.draw.rect(screen, (20, 20, 20), slider_rect)
    for i in range(slider_rect.height):
        v = 1.0 - (i / slider_rect.height)
        pygame.draw.line(screen, (int(255*v), int(255*v), int(255*v)), (slider_rect.left, slider_rect.top + i), (slider_rect.right, slider_rect.top + i))
    
    indicator_y = slider_rect.top + int((1.0 - value_slider) * slider_rect.height)
    pygame.draw.rect(screen, PINK, (slider_rect.left - 5, indicator_y - 2, slider_rect.width + 10, 4))
    
    close_txt = font_small.render("CLICK OUTSIDE TO CLOSE", True, (150, 150, 150))
    screen.blit(close_txt, (picker_rect.centerx - close_txt.get_width()//2, picker_rect.bottom - 25))

# --- FILE OPERATIONS ---
def save_file():
    path = filedialog.asksaveasfilename(title="Save your Miku Art", defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if path: pygame.image.save(canvas_surf, path)

def load_file():
    path = filedialog.askopenfilename(title="Load a Bitmap", filetypes=[("Image files", "*.png *.jpg *.bmp")])
    if path:
        img = pygame.image.load(path)
        canvas_surf.fill(WHITE) # Rubric: Ensure only one picture is visible at a time
        img = pygame.transform.scale(img, (canvas_rect.width, canvas_rect.height))
        canvas_surf.blit(img, (0, 0))

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

def update_draw_color():
    """Updates global draw_color based on stored HSV values"""
    global draw_color
    r, g, b = colorsys.hsv_to_rgb(current_hue, current_sat, value_slider)
    draw_color = (int(r*255), int(g*255), int(b*255))

# --- MAIN LOOP ---
clock = pygame.time.Clock()
running = True
mx, my = 0, 0
omx, omy = 0, 0
start_x, start_y = 0, 0

while running:
    dt = clock.tick(60)
    omx, omy = mx, my
    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()
    
    rel_mx, rel_my = mx - canvas_rect.x, my - canvas_rect.y
    rel_omx, rel_omy = omx - canvas_rect.x, omy - canvas_rect.y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if picking_color:
                    # Wheel coordinates relative to top-left of picker window
                    wheel_center = (picker_rect.x + 20 + color_wheel_radius, picker_rect.y + 20 + color_wheel_radius)
                    dx, dy = mx - wheel_center[0], my - wheel_center[1]
                    dist = (dx**2 + dy**2)**0.5
                    
                    if dist <= color_wheel_radius:
                        # Grab base color from wheel and update global H/S
                        raw_color = wheel_surf.get_at((int(mx - (picker_rect.x + 20)), int(my - (picker_rect.y + 20))))
                        h, s, _ = colorsys.rgb_to_hsv(raw_color.r/255, raw_color.g/255, raw_color.b/255)
                        current_hue, current_sat = h, s
                        update_draw_color()
                    
                    slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
                    if slider_rect.collidepoint(mx, my):
                        dragging_slider = True
                    
                    if not picker_rect.collidepoint(mx, my):
                        picking_color = False
                else:
                    # Trigger Color Wheel
                    if pygame.Rect(1000, 760, 150, 30).collidepoint(mx, my):
                        picking_color = True
                    
                    # Top Buttons
                    if pygame.Rect(WIDTH - 160, 25, 140, 40).collidepoint(mx, my): save_file()
                    if pygame.Rect(WIDTH - 320, 25, 140, 40).collidepoint(mx, my): load_file()

                    if not canvas_rect.collidepoint(mx, my):
                        # Sidebar and Presets
                        tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]
                        for i, t in enumerate(tools_list):
                            if pygame.Rect(25, 110 + (i * 35), 140, 30).collidepoint(mx, my):
                                tool = t
                        if pygame.Rect(115, 355, 25, 25).collidepoint(mx, my): thickness = min(100, thickness + 1)
                        if pygame.Rect(145, 355, 25, 25).collidepoint(mx, my): thickness = max(1, thickness - 1)
                        for i in range(5):
                            if pygame.Rect(25 + (i%2 * 75), 495 + (i//2 * 45), 60, 40).collidepoint(mx, my):
                                tool = f"stamp_{i}"
                        # Presets
                        for i, c in enumerate(PRESETS):
                            if pygame.Rect(200 + (i * 45), 760, 40, 30).collidepoint(mx, my):
                                draw_color = c
                                h, s, v = colorsys.rgb_to_hsv(c[0]/255, c[1]/255, c[2]/255)
                                current_hue, current_sat, value_slider = h, s, v
                    else:
                        undo_list.append(canvas_surf.copy())
                        if len(undo_list) > 30: undo_list.pop(0)
                        redo_list.clear()
                        start_x, start_y = rel_mx, rel_my

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = False
                # Handle Shape Finalization
                if tool in ["line", "rect", "oval"] and canvas_rect.collidepoint(mx, my) and not picking_color:
                    if tool == "line":
                        # MATH: Draw rotated polygon to keep thickness constant regardless of angle
                        dx, dy = rel_mx - start_x, rel_my - start_y
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            px, py = -dy * (thickness / 2) / dist, dx * (thickness / 2) / dist
                            pts = [(start_x+px, start_y+py), (start_x-px, start_y-py), (rel_mx-px, rel_my-py), (rel_mx+px, rel_my+py)]
                            pygame.draw.polygon(canvas_surf, draw_color, pts)
                        pygame.draw.circle(canvas_surf, draw_color, (start_x, start_y), thickness // 2)
                        pygame.draw.circle(canvas_surf, draw_color, (rel_mx, rel_my), thickness // 2)
                    elif tool == "rect":
                        r = pygame.Rect(start_x, start_y, rel_mx - start_x, rel_my - start_y)
                        r.normalize()
                        if filled: 
                            pygame.draw.rect(canvas_surf, draw_color, r)
                        else: 
                            pygame.draw.rect(canvas_surf, draw_color, r, thickness)
                    elif tool == "oval":
                        r = pygame.Rect(start_x, start_y, rel_mx - start_x, rel_my - start_y)
                        r.normalize()
                        if r.width > thickness and r.height > thickness:
                            if filled: 
                                pygame.draw.ellipse(canvas_surf, draw_color, r)
                            else: 
                                pygame.draw.ellipse(canvas_surf, draw_color, r, thickness)

        # --- UNIFIED KEYBOARD HANDLING (MOVED INSIDE EVENT LOOP) ---
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if (mods & pygame.KMOD_CTRL):
                if event.key == pygame.K_z:
                    if (mods & pygame.KMOD_SHIFT): 
                        perform_redo()
                    else: 
                        perform_undo()
                if event.key == pygame.K_s: save_file()
                if event.key == pygame.K_l: load_file()
                if event.key == pygame.K_f: filled = not filled
            
            if event.key == pygame.K_UP: thickness = min(100, thickness + 1)
            if event.key == pygame.K_DOWN: thickness = max(1, thickness - 1)

    # Handle Draggable Slider
    if picking_color and dragging_slider:
        slider_rect = pygame.Rect(picker_rect.right - 40, picker_rect.y + 20, 20, 200)
        value_slider = 1.0 - ((my - slider_rect.top) / slider_rect.height)
        value_slider = max(0, min(1, value_slider))
        update_draw_color()

    # Rendering
    draw_ui(mx, my) # Passing mouse pos for hover effects
    screen.blit(canvas_surf, (canvas_rect.x, canvas_rect.y))

    if picking_color:
        draw_color_picker()
    elif canvas_rect.collidepoint(mx, my):
        if tool.startswith("stamp_"):
            idx = int(tool.split("_")[1])
            s_size = thickness * 5
            ghost = pygame.transform.scale(master_stamps[idx], (int(s_size), int(s_size)))
            ghost.set_alpha(150)
            screen.blit(ghost, (mx - s_size//2, my - s_size//2))
        elif tool == "brush":
            pygame.draw.circle(screen, draw_color, (mx, my), thickness // 2, 1)
        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, (mx, my), (thickness * 4) // 2, 1)
        elif tool == "pencil":
            pygame.draw.circle(screen, draw_color, (mx, my), 2, 1)
        elif tool in ["line", "rect", "oval", "spray"]:
            pygame.draw.line(screen, BLACK, (mx-10, my), (mx+10, my), 1)
            pygame.draw.line(screen, BLACK, (mx, my-10), (mx, my+10), 1)
    
    # Active Drawing logic (Canvas persistence)
    if mb[0] and canvas_rect.collidepoint(mx, my) and not picking_color:
        if tool == "pencil":
            pygame.draw.line(canvas_surf, draw_color, (rel_omx, rel_omy), (rel_mx, rel_my), 1)
        elif tool in ["brush", "eraser"]:
            col = draw_color if tool == "brush" else WHITE
            thick = thickness if tool == "brush" else thickness * 4
            dx, dy = rel_mx - rel_omx, rel_my - rel_omy
            dist = math.hypot(dx, dy)
            if dist > 0:
                px, py = -dy * (thick / 2) / dist, dx * (thick / 2) / dist
                pts = [(rel_omx+px, rel_omy+py), (rel_omx-px, rel_omy-py), (rel_mx-px, rel_my-py), (rel_mx+px, rel_my+py)]
                pygame.draw.polygon(canvas_surf, col, pts)
            pygame.draw.circle(canvas_surf, col, (rel_mx, rel_my), thick // 2)
        elif tool == "spray":
            for _ in range(thickness // 2 + 5):
                rx, ry = random.randint(-thickness, thickness), random.randint(-thickness, thickness)
                if rx**2 + ry**2 <= thickness**2:
                    if 0 <= rel_mx + rx < canvas_rect.width and 0 <= rel_my + ry < canvas_rect.height:
                        canvas_surf.set_at((rel_mx + rx, rel_my + ry), draw_color)
        elif tool.startswith("stamp_"):
            idx = int(tool.split("_")[1])
            s_size = thickness * 5
            s_img = pygame.transform.scale(master_stamps[idx], (int(s_size), int(s_size)))
            canvas_surf.blit(s_img, (rel_mx - s_size//2, rel_my - s_size//2))
        elif tool in ["line", "rect", "oval"]:
            # Screen Preview (Same logic as provided)
            if tool == "line":
                sx, sy = start_x + canvas_rect.x, start_y + canvas_rect.y
                dx, dy = mx - sx, my - sy
                dist = math.hypot(dx, dy)
                if dist > 0:
                    px, py = -dy * (thickness / 2) / dist, dx * (thickness / 2) / dist
                    pts = [(sx+px, sy+py), (sx-px, sy-py), (mx-px, my-py), (mx+px, my+py)]
                    pygame.draw.polygon(screen, draw_color, pts)
                pygame.draw.circle(screen, draw_color, (sx, sy), thickness // 2); pygame.draw.circle(screen, draw_color, (mx, my), thickness // 2)
            elif tool == "rect":
                r = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mx - (start_x + canvas_rect.x), my - (start_y + canvas_rect.y))
                r.normalize()
                if filled: pygame.draw.rect(screen, draw_color, r)
                else: pygame.draw.rect(screen, draw_color, r, thickness)
            elif tool == "oval":
                r = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mx - (start_x + canvas_rect.x), my - (start_y + canvas_rect.y))
                r.normalize()
                if r.width > thickness and r.height > thickness:
                    if filled: pygame.draw.ellipse(screen, draw_color, r)
                    else: pygame.draw.ellipse(screen, draw_color, r, thickness)

    # --- ANIMATED CURSOR LOGIC (INJECTED AT END) ---
    pygame.mouse.set_visible(False)
    mode = "Normal"
    if canvas_rect.collidepoint(mx, my): 
        mode = "Handwriting"
    elif (mx < 200 or my < 100 or my > 750 or mx > 1150): 
        mode = "Link"
    
    cur_timer += dt
    if cur_timer > cur_speed:
        cur_timer = 0
        if cursor_dict[mode]: 
            cur_frame = (cur_frame + 1) % len(cursor_dict[mode])
    
    if cursor_dict[mode]:
        screen.blit(cursor_dict[mode][cur_frame % len(cursor_dict[mode])], (mx, my))
    else: 
        pygame.draw.circle(screen, BLACK, (mx, my), 2)

    coord_txt = font_mono.render(f"Pos: {rel_mx}, {rel_my} | Tool: {tool} | Size: {thickness} | Ctrl+Z: Undo", True, WHITE)
    screen.blit(coord_txt, (200, 740))
    pygame.display.flip()

pygame.quit()