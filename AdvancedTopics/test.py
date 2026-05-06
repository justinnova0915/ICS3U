import pygame
import math
import random

# --- Settings ---
WIDTH, HEIGHT = 640, 480  # Moderate resolution
BALL_SIZE_3D = 0.5        # Physical radius in the 3D world
COLLISION_DIST = BALL_SIZE_3D * 2.0 
SUBSTEPS = 6              # Higher precision to stop "tunneling"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Linked Physics: No Clipping")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.vel = [random.uniform(-0.01, 0.01) for _ in range(3)]
        self.color = pygame.Color(0)
        self.color.hsva = (random.randint(0, 360), 80, 90, 100)

    def update(self, g, f):
        d_sq = sum(p**2 for p in self.pos)
        dist = math.sqrt(d_sq)
        if dist > 0.1:
            accel = g / (d_sq + 1.0)
            for i in range(3):
                self.vel[i] -= (self.pos[i] / dist) * accel
        
        for i in range(3):
            self.pos[i] += self.vel[i]
            self.vel[i] *= f

def handle_collisions(balls):
    for _ in range(SUBSTEPS): # Precision loop
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                b1, b2 = balls[i], balls[j]
                diff = [b2.pos[k] - b1.pos[k] for k in range(3)]
                dist_sq = sum(d**2 for d in diff)
                
                # Check against the physical diameter
                if dist_sq < COLLISION_DIST**2:
                    dist = math.sqrt(dist_sq) or 0.0001
                    normal = [d/dist for d in diff]
                    
                    # Force separation immediately
                    overlap = (COLLISION_DIST - dist)
                    for k in range(3):
                        b1.pos[k] -= normal[k] * overlap * 0.5
                        b2.pos[k] += normal[k] * overlap * 0.5
                    
                    # Dampen velocity on impact to stop jitter
                    rel_vel = [b2.vel[k] - b1.vel[k] for k in range(3)]
                    vel_n = sum(rel_vel[k] * normal[k] for k in range(3))
                    if vel_n < 0:
                        impulse = -1.1 * vel_n / 2
                        for k in range(3):
                            b1.vel[k] -= impulse * normal[k]
                            b2.vel[k] += impulse * normal[k]

def rotate_3d(pos, ax, ay):
    x, y, z = pos
    cy, sy = math.cos(ay), math.sin(ay)
    nx, nz = x * cy + z * sy, -x * sy + z * cy
    cx, sx = math.cos(ax), math.sin(ax)
    ny, nz = y * cx - nz * sx, y * sx + nz * cx
    return [nx, ny, nz]

# --- Setup ---
balls = [Ball((random.random()-0.5)*5, (random.random()-0.5)*5, (random.random()-0.5)*5) for _ in range(10)]
cam_x = cam_y = cam_vx = cam_vy = 0

while True:
    screen.fill((10, 10, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  cam_vy -= 0.008
    if keys[pygame.K_RIGHT]: cam_vy += 0.008
    if keys[pygame.K_UP]:    cam_vx -= 0.008
    if keys[pygame.K_DOWN]:  cam_vx += 0.008
    cam_x += cam_vx; cam_y += cam_vy; cam_vx *= 0.9; cam_vy *= 0.9

    # Physics
    handle_collisions(balls)
    for b in balls: b.update(0.08, 0.96)

    # Rendering
    z_buffer = [float('inf')] * (WIDTH * HEIGHT)
    px_array = pygame.PixelArray(screen)

    for b in balls:
        rot = rotate_3d(b.pos, cam_x, cam_y)
        view_dist = 10
        # Calculate visual radius based on the SAME BALL_SIZE_3D used in physics
        zoom = 300 / (rot[2] + view_dist)
        r = int(BALL_SIZE_3D * zoom) 
        
        cx, cy = int(rot[0] * zoom + WIDTH//2), int(rot[1] * zoom + HEIGHT//2)
        
        if r < 1: continue

        for dy in range(-r, r):
            scr_y = cy + dy
            if 0 <= scr_y < HEIGHT:
                for dx in range(-r, r):
                    scr_x = cx + dx
                    if 0 <= scr_x < WIDTH:
                        d_sq = dx*dx + dy*dy
                        if d_sq <= r*r:
                            local_z = math.sqrt(r*r - d_sq)
                            pixel_z = rot[2] - (local_z / zoom)
                            
                            idx = scr_y * WIDTH + scr_x
                            if pixel_z < z_buffer[idx]:
                                z_buffer[idx] = pixel_z
                                lum = (local_z / r)
                                px_array[scr_x, scr_y] = (
                                    int(b.color.r * lum),
                                    int(b.color.g * lum),
                                    int(b.color.b * lum)
                                )

    px_array.close()
    pygame.display.flip()
    clock.tick(60)