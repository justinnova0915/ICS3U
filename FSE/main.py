import pygame
import random
import math
import zipfile
import io
import os
import time

# --- Configuration & Constants ---
WIDTH, HEIGHT = 1920, 1080
FPS = 60
APPROACH_START_SCALE = 3.5
GLOBAL_CS_MULTIPLIER = 0.85 

PLAYFIELD_WIDTH = 512
PLAYFIELD_HEIGHT = 384
SCALE = min((WIDTH * 0.8) / PLAYFIELD_WIDTH, (HEIGHT * 0.8) / PLAYFIELD_HEIGHT)
OFFSET_X = (WIDTH - (PLAYFIELD_WIDTH * SCALE)) / 2
OFFSET_Y = (HEIGHT - (PLAYFIELD_HEIGHT * SCALE)) / 2

# --- BEATMAP CONFIGURATION ---
BEATMAP_PATH = "./FSE/Data/Beatmaps/AiScReam.osz" 
TEMP_AUDIO_PATH = "temp_audio_file"

# Colors
COLOR_BG = (10, 10, 15)
COLOR_CIRCLE = (255, 100, 150)
COLOR_SLIDER_TRACK = (40, 40, 60)
COLOR_SLIDER_BORDER = (200, 200, 220)
COLOR_APPROACH = (255, 255, 255)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (0, 200, 255)
COLOR_FOLLOW_CIRCLE = (255, 255, 255, 30)

# --- Helper Functions ---
def lerp(a, b, t):
    return a + (b - a) * t

def get_bezier_point(points, t):
    if len(points) == 1: return points[0]
    new_points = []
    for i in range(len(points) - 1):
        x = lerp(points[i][0], points[i+1][0], t)
        y = lerp(points[i][1], points[i+1][1], t)
        new_points.append((x, y))
    return get_bezier_point(new_points, t)

# --- Classes ---

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-5, 5), random.uniform(-5, 5)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay

    def draw(self, surface):
        if self.life <= 0: return
        alpha = int(self.life * 255)
        size = max(1, int(self.life * 6))
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (size, size), size)
        surface.blit(s, (self.x - size, self.y - size))

class HitObject:
    def __init__(self, x, y, hit_time, index, radius, stack_offset=0):
        nudge = stack_offset * (radius * 0.1)
        self.x = int(x * SCALE + OFFSET_X + nudge)
        self.y = int(y * SCALE + OFFSET_Y + nudge)
        self.hit_time = hit_time
        self.index = index
        self.radius = int(radius * SCALE * GLOBAL_CS_MULTIPLIER)
        self.is_hit = False
        self.is_missed = False
        self.type = "circle"

    def get_progress(self, current_time, preempt):
        return 1.0 - (self.hit_time - current_time) / preempt

class HitCircle(HitObject):
    def draw_body(self, surface, current_time, preempt):
        progress = self.get_progress(current_time, preempt)
        if progress < 0 or self.is_hit or self.is_missed: return

        alpha = min(255, int(progress * 2 * 255))
        temp_surface = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*COLOR_CIRCLE, alpha), (self.radius, self.radius), self.radius, 5)
        pygame.draw.circle(temp_surface, (255, 255, 255, alpha // 2), (self.radius, self.radius), self.radius - 5)
        
        font = pygame.font.SysFont("Arial", max(12, int(self.radius * 0.8)), bold=True)
        txt = font.render(str(self.index), True, (255, 255, 255))
        txt.set_alpha(alpha)
        temp_surface.blit(txt, (self.radius - txt.get_width()//2, self.radius - txt.get_height()//2))
        surface.blit(temp_surface, (self.x - self.radius, self.y - self.radius))

        if current_time < self.hit_time:
            scale = APPROACH_START_SCALE - (APPROACH_START_SCALE - 1.0) * progress
            pygame.draw.circle(surface, (255, 255, 255, alpha), (self.x, self.y), int(self.radius * scale), 2)

class Slider(HitObject):
    def __init__(self, x, y, hit_time, index, radius, curve_points, length, repeats, slider_multiplier, beat_duration, curve_type, stack_offset=0):
        super().__init__(x, y, hit_time, index, radius, stack_offset)
        self.type = "slider"
        nudge = stack_offset * (self.radius * 0.1)
        scaled_points = [(px * SCALE + OFFSET_X + nudge, py * SCALE + OFFSET_Y + nudge) for px, py in curve_points]
        
        self.smooth_path = []
        # Increase resolution to eliminate sharp angles
        res = max(int(length / 1.5), 20) 
        if curve_type in ['B', 'C', 'P']:
            for i in range(res + 1):
                self.smooth_path.append(get_bezier_point(scaled_points, i / res))
        else:
            for i in range(len(scaled_points) - 1):
                p1, p2 = scaled_points[i], scaled_points[i+1]
                seg_dist = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                steps = max(2, int(seg_dist))
                for s in range(steps):
                    self.smooth_path.append((lerp(p1[0], p2[0], s/steps), lerp(p1[1], p2[1], s/steps)))
            self.smooth_path.append(scaled_points[-1])

        self.repeats = repeats
        self.duration_per_slide = (length / (slider_multiplier * 100)) * beat_duration
        self.total_duration = self.duration_per_slide * repeats
        self.end_time = self.hit_time + self.total_duration
        self.is_active = False

    def get_ball_info(self, current_time):
        if not self.smooth_path: return self.smooth_path[0], 0, 0
        elapsed = current_time - self.hit_time
        slide_num = int(elapsed / self.duration_per_slide)
        progress = (elapsed % self.duration_per_slide) / self.duration_per_slide
        
        is_reversed = (slide_num % 2 == 1)
        actual_progress = 1.0 - progress if is_reversed else progress
        
        idx = actual_progress * (len(self.smooth_path) - 1)
        i = int(idx)
        rem = idx - i
        p1 = self.smooth_path[i]
        p2 = self.smooth_path[min(i + 1, len(self.smooth_path)-1)]
        pos = (lerp(p1[0], p2[0], rem), lerp(p1[1], p2[1], rem))
        
        return pos, slide_num, actual_progress

    def draw_track(self, surface, current_time, preempt):
        progress = self.get_progress(current_time, preempt)
        if progress < 0 or self.is_missed: return
        if current_time > self.end_time and not self.is_hit: return

        ball_pos, slide_num, ball_progress = self.get_ball_info(current_time)
        
        # Snake-out effect
        draw_path = self.smooth_path
        if self.hit_time <= current_time <= self.end_time and self.repeats == 1:
            start_idx = int(ball_progress * (len(self.smooth_path)-1))
            draw_path = self.smooth_path[start_idx:]

        if len(draw_path) > 1:
            for color, r_mod in [(COLOR_SLIDER_BORDER, 0), (COLOR_SLIDER_TRACK, -4)]:
                for i in range(0, len(draw_path), 2): # High density for smoothness
                    p = draw_path[i]
                    pygame.draw.circle(surface, color, (int(p[0]), int(p[1])), self.radius + r_mod)

        if self.repeats > 1:
            for r in range(1, self.repeats):
                arrow_pos = self.smooth_path[-1] if r % 2 == 1 else self.smooth_path[0]
                pygame.draw.circle(surface, (255, 255, 255), (int(arrow_pos[0]), int(arrow_pos[1])), int(self.radius * 0.6), 2)

    def draw_body(self, surface, current_time, preempt):
        progress = self.get_progress(current_time, preempt)
        if progress < 0 or self.is_missed: return
        if current_time > self.end_time and not self.is_hit: return

        alpha = min(255, int(progress * 2 * 255))
        ball_pos, slide_num, ball_progress = self.get_ball_info(current_time)

        if current_time <= self.hit_time:
            start_pos = self.smooth_path[0]
            pygame.draw.circle(surface, (*COLOR_CIRCLE, alpha), (int(start_pos[0]), int(start_pos[1])), self.radius, 5)
            font = pygame.font.SysFont("Arial", max(12, int(self.radius * 0.8)), bold=True)
            txt = font.render(str(self.index), True, (255, 255, 255))
            surface.blit(txt, (int(start_pos[0] - txt.get_width()//2), int(start_pos[1] - txt.get_height()//2)))
            
            scale = APPROACH_START_SCALE - (APPROACH_START_SCALE - 1.0) * progress
            pygame.draw.circle(surface, (255, 255, 255, alpha), (int(start_pos[0]), int(start_pos[1])), int(self.radius * scale), 2)

        if self.hit_time <= current_time <= self.end_time:
            bx, by = int(ball_pos[0]), int(ball_pos[1])
            s = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
            pygame.draw.circle(s, COLOR_FOLLOW_CIRCLE, (self.radius*3, self.radius*3), self.radius*2.5)
            surface.blit(s, (bx - self.radius*3, by - self.radius*3))
            pygame.draw.circle(surface, (255, 255, 255), (bx, by), self.radius - 5)
            pygame.draw.circle(surface, COLOR_ACCENT, (bx, by), self.radius, 4)

class BeatmapParser:
    @staticmethod
    def get_difficulties(path):
        if not os.path.exists(path): return []
        diffs = []
        try:
            with zipfile.ZipFile(path, 'r') as z:
                for f in [x for x in z.namelist() if x.endswith(".osu")]:
                    with z.open(f) as file:
                        content = file.read().decode('utf-8', errors='ignore')
                        v = next((l.split(":")[1].strip() for l in content.splitlines() if l.startswith("Version:")), "Unknown")
                        diffs.append((v, f))
        except: pass
        return diffs

    @staticmethod
    def parse_file_from_zip(path, target_filename):
        data = BeatmapData()
        try:
            with zipfile.ZipFile(path, 'r') as z:
                with z.open(target_filename) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                
                lines = content.splitlines()
                section = None
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    if line.startswith("["): section = line; continue
                    
                    if section == "[General]" and line.startswith("AudioFilename:"): data.audio_filename = line.split(":")[1].strip()
                    elif section == "[Metadata]":
                        if line.startswith("Title:"): data.title = line.split(":")[1].strip()
                        if line.startswith("Artist:"): data.artist = line.split(":")[1].strip()
                    elif section == "[Difficulty]":
                        if line.startswith("CircleSize:"): data.cs = float(line.split(":")[1])
                        if line.startswith("OverallDifficulty:"): data.od = float(line.split(":")[1])
                        if line.startswith("ApproachRate:"): data.ar = float(line.split(":")[1])
                        if line.startswith("SliderMultiplier:"): data.slider_multiplier = float(line.split(":")[1])
                    elif section == "[Events]":
                        if line.startswith("0,0,"): data.bg_filename = line.split(",")[2].strip('"')
                        elif line.startswith("2,"): 
                            p = line.split(",")
                            data.breaks.append((int(p[1]), int(p[2])))
                    elif section == "[TimingPoints]":
                        p = line.split(',')
                        if len(p) >= 2 and float(p[1]) > 0: data.beat_duration = float(p[1])
                    elif section == "[HitObjects]":
                        p = line.split(',')
                        x, y, t, obj_type = int(p[0]), int(p[1]), int(p[2]), int(p[3])
                        radius = (54.4 - 4.48 * data.cs)
                        idx = (len(data.hit_objects) % 9) + 1
                        
                        stack = 0
                        if data.hit_objects and abs(data.hit_objects[-1].hit_time - t) < 10:
                            stack = data.hit_objects[-1].stack_offset + 1 if hasattr(data.hit_objects[-1], 'stack_offset') else 1

                        if obj_type & 1: 
                            obj = HitCircle(x, y, t, idx, radius, stack)
                            obj.stack_offset = stack
                            data.hit_objects.append(obj)
                        elif obj_type & 2:
                            curve_parts = p[5].split('|')
                            pts = [(x, y)]
                            for pt in curve_parts[1:]:
                                try:
                                    c = pt.split(':')
                                    pts.append((int(c[0]), int(c[1])))
                                except: pass
                            obj = Slider(x, y, t, idx, radius, pts, float(p[7]), int(p[6]), data.slider_multiplier, data.beat_duration, curve_parts[0], stack)
                            obj.stack_offset = stack
                            data.hit_objects.append(obj)

                if data.audio_filename in z.namelist(): data.audio_data = z.read(data.audio_filename)
                if data.bg_filename and data.bg_filename in z.namelist():
                    try:
                        img_data = io.BytesIO(z.read(data.bg_filename))
                        data.bg_image = pygame.image.load(img_data).convert()
                        br = data.bg_image.get_rect()
                        bs = min(WIDTH/br.width, HEIGHT/br.height)
                        data.bg_image = pygame.transform.smoothscale(data.bg_image, (int(br.width*bs), int(br.height*bs)))
                        data.bg_image.set_alpha(100)
                    except: pass
            return data
        except Exception as e: print(f"Error: {e}"); return None

class BeatmapData:
    def __init__(self):
        self.audio_filename = self.bg_filename = self.bg_image = self.audio_data = None
        self.hit_objects = []; self.breaks = []
        self.title = self.artist = "Unknown"
        self.cs = self.od = self.ar = 5.0; self.slider_multiplier = 1.0; self.beat_duration = 500.0

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.difficulties = BeatmapParser.get_difficulties(BEATMAP_PATH)
        self.active_objects = []; self.particles = []; self.score = self.combo = 0; self.accuracy_hits = []
        self.shake = 0; self.running = True; self.state = "selector"

        # Timing sync variables
        self.last_mixer_pos = 0
        self.last_perf_time = 0
        self.interpolated_time = 0

    def start(self, filename):
        self.beatmap = BeatmapParser.parse_file_from_zip(BEATMAP_PATH, filename)
        if self.beatmap and self.beatmap.audio_data:
            ext = ".ogg" if self.beatmap.audio_data.startswith(b'OggS') else ".mp3"
            f_path = TEMP_AUDIO_PATH + ext
            with open(f_path, "wb") as f: f.write(self.beatmap.audio_data)
            pygame.mixer.music.load(f_path)
            pygame.mixer.music.play()
        
        self.preempt = 1200 + 600 * (5 - self.beatmap.ar) / 5 if self.beatmap.ar < 5 else 1200 - 750 * (self.beatmap.ar - 5) / 5
        self.w300, self.w100, self.w50 = 80 - 6*self.beatmap.od, 140 - 8*self.beatmap.od, 200 - 10*self.beatmap.od
        self.state = "playing"
        self.last_perf_time = time.perf_counter()

    def get_current_time(self):
        """High precision hybrid master clock."""
        if self.state != "playing": return 0
        
        current_mixer_pos = pygame.mixer.music.get_pos()
        current_perf = time.perf_counter()

        # If mixer position changed, update our base time
        if current_mixer_pos != self.last_mixer_pos:
            self.last_mixer_pos = current_mixer_pos
            self.last_perf_time = current_perf
            self.interpolated_time = current_mixer_pos
        else:
            # Otherwise, use high-precision timer to fill in the gaps between mixer updates
            delta = (current_perf - self.last_perf_time) * 1000 # to ms
            self.interpolated_time = self.last_mixer_pos + delta
            
        return self.interpolated_time

    def update(self):
        if self.state == "selector": return
        now = self.get_current_time()
        
        if self.beatmap:
            while self.beatmap.hit_objects and self.beatmap.hit_objects[0].hit_time - self.preempt <= now:
                self.active_objects.append(self.beatmap.hit_objects.pop(0))
        
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)
            
        for obj in self.active_objects[:]:
            if not obj.is_hit and not obj.is_missed:
                if obj.type == "circle" and now > obj.hit_time + self.w50:
                    obj.is_missed = True; self.combo = 0; self.shake = 12
                elif obj.type == "slider":
                    if now > obj.hit_time + self.w50 and not obj.is_active:
                        obj.is_missed = True; self.combo = 0; self.shake = 12
                    elif now > obj.end_time: obj.is_hit = True 
            if obj.is_hit or obj.is_missed: self.active_objects.remove(obj)
        if self.shake > 0: self.shake -= 1

    def draw(self):
        self.screen.fill(COLOR_BG)
        if self.state == "selector":
            f = pygame.font.SysFont("Verdana", 50)
            for i, (n, _) in enumerate(self.difficulties):
                r = pygame.Rect(WIDTH//2 - 400, 300 + i*150, 800, 100)
                pygame.draw.rect(self.screen, (40, 40, 60), r, border_radius=20)
                pygame.draw.rect(self.screen, COLOR_ACCENT, r, 3, border_radius=20)
                txt = f.render(n, True, COLOR_TEXT)
                self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 300 + i*150 + 25))
        else:
            if self.beatmap.bg_image:
                self.screen.blit(self.beatmap.bg_image, (WIDTH//2 - self.beatmap.bg_image.get_width()//2, HEIGHT//2 - self.beatmap.bg_image.get_height()//2))
            now = self.get_current_time()
            
            for obj in self.active_objects:
                if obj.type == "slider": obj.draw_track(self.screen, now, self.preempt)
            for obj in self.active_objects:
                obj.draw_body(self.screen, now, self.preempt)
                
            for p in self.particles: p.draw(self.screen)
            ui = pygame.font.SysFont("Verdana", 80, bold=True)
            self.screen.blit(ui.render(f"{self.score:08}", True, COLOR_TEXT), (WIDTH - 500, 50))
            self.screen.blit(ui.render(f"{self.combo}x", True, COLOR_ACCENT), (50, HEIGHT - 150))
        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: self.running = False
                if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or \
                   (e.type == pygame.KEYDOWN and (e.key == pygame.K_z or e.key == pygame.K_x)):
                    if self.state == "selector":
                        if hasattr(e, 'pos'):
                            for i in range(len(self.difficulties)):
                                if pygame.Rect(WIDTH//2 - 400, 300 + i*150, 800, 100).collidepoint(e.pos):
                                    self.start(self.difficulties[i][1])
                    else:
                        click_pos = pygame.mouse.get_pos()
                        now = self.get_current_time()
                        self.active_objects.sort(key=lambda o: o.hit_time)
                        for o in self.active_objects:
                            if o.is_hit or o.is_missed: continue
                            if math.hypot(click_pos[0] - o.x, click_pos[1] - o.y) <= o.radius:
                                if o.type == "circle":
                                    err = abs(now - o.hit_time)
                                    if err <= self.w50:
                                        o.is_hit = True; self.combo += 1
                                        p = 300 if err <= self.w300 else (100 if err <= self.w100 else 50)
                                        self.score += p * self.combo; self.accuracy_hits.append(p)
                                        for _ in range(12): self.particles.append(Particle(o.x, o.y, COLOR_CIRCLE))
                                        break
                                elif o.type == "slider":
                                    if abs(now - o.hit_time) <= self.w50:
                                        o.is_active = True; self.combo += 1; self.score += 30 * self.combo; break
            self.update(); self.draw(); self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    Game().run()