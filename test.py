"""
Program: Miku Paint Pro (Pygame Edition)
Author: Gemini (for ICS 3U)
Description: A Hatsune Miku themed paint program featuring freehand drawing, 
             shapes (rect, circle, line), stamps, and load/save functionality.
Theme: Hatsune Miku (Teal #39C5BB, Pink #E639AF)
"""

import pygame
import random
import os

# --- TKINTER HANDLING ---
# Arch Linux users: Ensure 'tk' is installed (sudo pacman -S tk)
try:
    from tkinter import filedialog, Tk
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False

# --- INITIALIZATION ---
pygame.init()

# Robust Font Initialization (Fix for Python 3.14 / Arch issues)
FONT_AVAILABLE = True
try:
    if not pygame.font.get_init():
        pygame.font.init()
except (ImportError, NotImplementedError, pygame.error):
    FONT_AVAILABLE = False

if TK_AVAILABLE:
    try:
        root = Tk()
        root.withdraw()
    except Exception:
        TK_AVAILABLE = False

# Screen Dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MIKU PAINT PRO - Vocaloid Edition")

# --- COLORS ---
TEAL = (57, 197, 187)      
PINK = (230, 57, 175)      
DARK_GREY = (30, 30, 30)   
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- CANVAS SETUP ---
canvas_rect = pygame.Rect(200, 100, 950, 650)
canvas_surf = pygame.Surface((canvas_rect.width, canvas_rect.height))
canvas_surf.fill(WHITE)

# --- GLOBAL VARIABLES ---
draw_color = TEAL
brush_size = 5
tool = "pencil"
filled = False
undo_list = []

# --- ASSET GENERATION ---
def create_stamps():
    stamps = []
    themes = [TEAL, PINK, (255, 255, 0), (0, 255, 0), (200, 200, 255)]
    for i in range(5):
        s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(s, themes[i], (20, 20), 18)
        pygame.draw.circle(s, WHITE, (20, 20), 18, 2)
        stamps.append(s)
    return stamps

stamps = create_stamps()

# --- HELPER FUNCTIONS ---
def safe_render(text, size, color, bold=False):
    if FONT_AVAILABLE:
        try:
            font = pygame.font.SysFont("Arial", size, bold=bold)
            return font.render(text, True, color)
        except: pass
    surf = pygame.Surface((len(text)*size//2, size))
    surf.fill((40, 40, 40))
    pygame.draw.rect(surf, color, surf.get_rect(), 1)
    return surf

def draw_ui():
    """Renders the static UI elements around the canvas"""
    screen.fill(DARK_GREY)
    
    # Title
    title_surf = safe_render("MIKU PAINT ", 36, TEAL, True)
    pro_surf = safe_render("PRO", 36, PINK, True)
    screen.blit(title_surf, (20, 20))
    screen.blit(pro_surf, (20 + title_surf.get_width(), 20))

    # Sidebar
    pygame.draw.rect(screen, (45, 45, 45), (10, 100, 170, 680), border_radius=15)
    
    # Tool Buttons
    tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]
    for i, t in enumerate(tools_list):
        t_rect = pygame.Rect(25, 120 + (i * 45), 140, 35)
        color = TEAL if tool == t else (60, 60, 60)
        pygame.draw.rect(screen, color, t_rect, border_radius=5)
        txt = safe_render(t.upper(), 14, BLACK if tool == t else WHITE, True)
        screen.blit(txt, (t_rect.centerx - txt.get_width()//2, t_rect.centery - txt.get_height()//2))

    # Stamps
    stamp_header = safe_render("STAMPS", 16, PINK, True)
    screen.blit(stamp_header, (25, 440))
    for i in range(5):
        s_rect = pygame.Rect(25 + (i%2 * 75), 470 + (i//2 * 50), 60, 40)
        pygame.draw.rect(screen, (60, 60, 60), s_rect, border_radius=5)
        screen.blit(stamps[i], (s_rect.centerx - 20, s_rect.centery - 20))
        if tool == f"stamp_{i}":
            pygame.draw.rect(screen, WHITE, s_rect, 2, border_radius=5)

    # Save/Load Buttons
    save_rect = pygame.Rect(25, 610, 140, 35)
    load_rect = pygame.Rect(25, 655, 140, 35)
    pygame.draw.rect(screen, PINK, save_rect, border_radius=5)
    pygame.draw.rect(screen, PINK, load_rect, border_radius=5)
    
    save_txt = safe_render("SAVE (S)", 14, BLACK, True)
    load_txt = safe_render("LOAD (L)", 14, BLACK, True)
    screen.blit(save_txt, (save_rect.centerx - save_txt.get_width()//2, save_rect.centery - save_txt.get_height()//2))
    screen.blit(load_txt, (load_rect.centerx - load_txt.get_width()//2, load_rect.centery - load_txt.get_height()//2))

    # Color Palette
    colors = [BLACK, WHITE, (255,0,0), (0,255,0), (0,0,255), (255,255,0), TEAL, PINK]
    for i, c in enumerate(colors):
        c_rect = pygame.Rect(200 + (i * 45), 760, 40, 30)
        pygame.draw.rect(screen, c, c_rect, border_radius=3)
        if draw_color == c:
            pygame.draw.rect(screen, WHITE, c_rect, 3, border_radius=3)

    # Preview Box
    pygame.draw.rect(screen, draw_color, (1000, 760, 150, 30), border_radius=5)
    
    # Border around the canvas area
    pygame.draw.rect(screen, TEAL, canvas_rect.inflate(10, 10), 5, border_radius=10)

def save_file():
    path = None
    if TK_AVAILABLE:
        try: 
            path = filedialog.asksaveasfilename(
                title="Save your Miku Art",
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
            )
        except: pass
    if not path: 
        path = "miku_art.png"
    
    try:
        pygame.image.save(canvas_surf, path)
        print(f"Successfully saved to: {path}")
    except pygame.error as e:
        print(f"Save failed: {e}")

def load_file():
    path = None
    if TK_AVAILABLE:
        try: 
            path = filedialog.askopenfilename(
                title="Load a Bitmap",
                filetypes=[("Image files", "*.png *.jpg *.bmp"), ("All Files", "*.*")]
            )
        except: pass
    
    if path:
        try:
            img = pygame.image.load(path)
            # Rubric Requirement: Resize to fit canvas area
            img = pygame.transform.scale(img, (canvas_rect.width, canvas_rect.height))
            canvas_surf.blit(img, (0, 0))
            print(f"Loaded: {path}")
        except pygame.error as e:
            print(f"Load failed: {e}")

# --- MAIN LOOP ---
running = True
mx, my = 0, 0
omx, omy = 0, 0
start_x, start_y = 0, 0

while running:
    omx, omy = mx, my
    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()
    
    rel_mx, rel_my = mx - canvas_rect.x, my - canvas_rect.y
    rel_omx, rel_omy = omx - canvas_rect.x, omy - canvas_rect.y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                undo_list.append(canvas_surf.copy())
                if len(undo_list) > 30: undo_list.pop(0)
                
                if not canvas_rect.collidepoint(mx, my):
                    # Tool Selection
                    tools_list = ["pencil", "brush", "eraser", "spray", "line", "rect", "oval"]
                    for i, t in enumerate(tools_list):
                        if pygame.Rect(25, 120 + (i * 45), 140, 35).collidepoint(mx, my):
                            tool = t
                    # Stamp Selection
                    for i in range(5):
                        if pygame.Rect(25 + (i%2 * 75), 470 + (i//2 * 50), 60, 40).collidepoint(mx, my):
                            tool = f"stamp_{i}"
                    # Color Selection
                    colors = [BLACK, WHITE, (255,0,0), (0,255,0), (0,0,255), (255,255,0), TEAL, PINK]
                    for i, c in enumerate(colors):
                        if pygame.Rect(200 + (i * 45), 760, 40, 30).collidepoint(mx, my):
                            draw_color = c
                    # Save/Load Buttons
                    if pygame.Rect(25, 610, 140, 35).collidepoint(mx, my): save_file()
                    if pygame.Rect(25, 655, 140, 35).collidepoint(mx, my): load_file()
                else:
                    start_x, start_y = rel_mx, rel_my

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: save_file()
            if event.key == pygame.K_l: load_file()
            if event.key == pygame.K_f: filled = not filled
            if event.key == pygame.K_u and undo_list:
                canvas_surf = undo_list.pop()

    draw_ui()
    screen.blit(canvas_surf, (canvas_rect.x, canvas_rect.y))

    if mb[0] and canvas_rect.collidepoint(mx, my):
        if tool == "pencil":
            pygame.draw.line(canvas_surf, draw_color, (rel_omx, rel_omy), (rel_mx, rel_my), 1)
        elif tool == "brush":
            pygame.draw.line(canvas_surf, draw_color, (rel_omx, rel_omy), (rel_mx, rel_my), brush_size)
            pygame.draw.circle(canvas_surf, draw_color, (rel_mx, rel_my), brush_size // 2)
        elif tool == "eraser":
            pygame.draw.line(canvas_surf, WHITE, (rel_omx, rel_omy), (rel_mx, rel_my), 30)
            pygame.draw.circle(canvas_surf, WHITE, (rel_mx, rel_my), 15)
        elif tool == "spray":
            for _ in range(25):
                rx, ry = random.randint(-15, 15), random.randint(-15, 15)
                if rx**2 + ry**2 <= 15**2:
                    if 0 <= rel_mx + rx < canvas_rect.width and 0 <= rel_my + ry < canvas_rect.height:
                        canvas_surf.set_at((rel_mx + rx, rel_my + ry), draw_color)
        elif tool.startswith("stamp_"):
            idx = int(tool.split("_")[1])
            canvas_surf.blit(stamps[idx], (rel_mx - 20, rel_my - 20))

        # Preview shapes on SCREEN
        elif tool in ["line", "rect", "oval"]:
            if tool == "line":
                pygame.draw.line(screen, draw_color, (start_x + canvas_rect.x, start_y + canvas_rect.y), (mx, my), 2)
            elif tool == "rect":
                r = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mx - (start_x + canvas_rect.x), my - (start_y + canvas_rect.y))
                r.normalize()
                if filled: pygame.draw.rect(screen, draw_color, r)
                else: pygame.draw.rect(screen, draw_color, r, 2)
            elif tool == "oval":
                r = pygame.Rect(start_x + canvas_rect.x, start_y + canvas_rect.y, mx - (start_x + canvas_rect.x), my - (start_y + canvas_rect.y))
                r.normalize()
                if r.width > 2 and r.height > 2:
                    if filled: pygame.draw.ellipse(screen, draw_color, r)
                    else: pygame.draw.ellipse(screen, draw_color, r, 2)

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if tool in ["line", "rect", "oval"] and canvas_rect.collidepoint(mx, my):
            if tool == "line":
                pygame.draw.line(canvas_surf, draw_color, (start_x, start_y), (rel_mx, rel_my), 2)
            elif tool == "rect":
                r = pygame.Rect(start_x, start_y, rel_mx - start_x, rel_my - start_y)
                r.normalize()
                if filled: pygame.draw.rect(canvas_surf, draw_color, r)
                else: pygame.draw.rect(canvas_surf, draw_color, r, 2)
            elif tool == "oval":
                r = pygame.Rect(start_x, start_y, rel_mx - start_x, rel_my - start_y)
                r.normalize()
                if r.width > 2 and r.height > 2:
                    if filled: pygame.draw.ellipse(canvas_surf, draw_color, r)
                    else: pygame.draw.ellipse(canvas_surf, draw_color, r, 2)

    coord_txt = safe_render(f"Pos: {rel_mx}, {rel_my} | Tool: {tool} | Filled: {filled} (F)", 14, WHITE)
    screen.blit(coord_txt, (200, 740))

    pygame.display.flip()

pygame.quit()