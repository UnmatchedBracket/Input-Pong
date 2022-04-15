import pygame
import sys
from pygame._sdl2.video import Window, Renderer, Texture
import time
import math

pygame.init()

sound_paddle_hit = pygame.mixer.Sound("paddle_hit.wav")
sound_wall_hit = pygame.mixer.Sound("wall_hit.wav")
sound_score = pygame.mixer.Sound("score.wav")

X = 0

W, H = pygame.display.get_desktop_sizes()[0]

ball = Window("ball", (50, 50), (X, 0), borderless=True)

ball_renderer = Renderer(ball)

ball_renderer.draw_color = (255, 255, 255, 255)
ball_renderer.clear()
ball_renderer.present()

paddle = Window("paddle", (500, 50), (X, 1000), borderless=True)

paddle_renderer = Renderer(paddle)
paddle_surf = pygame.Surface(paddle.size)
paddle_surf.fill((255, 255, 255))

def arrow(x, dir):
    pygame.draw.polygon(paddle_surf, (0, 0, 255), [(x+(15*dir), 10), (x+(15*dir), 40), (x, 25)])

arrow(10,  1)
arrow(25,  1)
arrow(135, 1)

arrow(490, -1)
arrow(475, -1)
arrow(365, -1)


pygame.draw.rect(paddle_surf, (0, 0, 255), (247, 0, 6, 50))
pygame.draw.rect(paddle_surf, (0, 0, 255), (124, 0, 2, 50))
pygame.draw.rect(paddle_surf, (0, 0, 255), (374, 0, 2, 50))

paddle_renderer.blit(Texture.from_surface(paddle_renderer, paddle_surf))
paddle_renderer.present()

FONT = pygame.font.SysFont("quicksand", 60)
BAKFONT = pygame.font.SysFont("symbola", 60)

ui = Window("ui", (W, 160), (X, H-160), borderless=True)

ui_renderer = Renderer(ui)
ui_surf = pygame.Surface(ui.size)

paddle_x = 0
paddle_y = 800
paddle_velocity = 0
paddle_accel = 0

ball_pos = [0, 40]

ball_vel = [10, -10]

SPECIAL = "⌫↤⇬↵⏎⇧⟵⌦⎚"
BACKSPACE = "⌫"
SHIFT = "⇬"
ENTER = "⏎"
CLEAR = "⎚"

typed = ""

alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[]{}-=_+`~'\":;,.<>/? "
alphabet += BACKSPACE + SHIFT*3 + ENTER*5 + CLEAR*10
alphabet = list(alphabet)
random.shuffle(alphabet)
alphabet = "".join(alphabet)

current = 0
anim_offset = 0

def centered(win, render, xy):
    rect = render.get_rect()
    rect.midtop = xy
    win.blit(render, rect.topleft)

def render_ui(nocursor=False):
    global anim_offset
    ui_surf.fill((255, 255, 255))
    x = W/2 + 1000
    i = 10
    current_ofsetted = current - math.floor(anim_offset)
    partial_offset = (anim_offset % 1) * 100
    anim_offset *= 0.82
    while x > -50:
        color = min(abs(i*20), 200)
        char = alphabet[(current_ofsetted+i)%len(alphabet)]
        f = (BAKFONT if char in SPECIAL else FONT)
        centered(ui_surf, f.render(char, True, (color, color, color)), (x+partial_offset, 0))
        x -= 100
        i -= 1

    pygame.draw.rect(ui_surf, (0, 0, 255), (W/2-32, 0, 4, 80))
    pygame.draw.rect(ui_surf, (0, 0, 255), (W/2+28, 0, 4, 80))

    cursor = "|" if (time.time() % 1 < 0.5 and not nocursor) else ""
    
    ui_surf.blit(FONT.render(typed + cursor, True, (0, 0, 0)), (0, 80))

    ui_renderer.blit(Texture.from_surface(ui_renderer, ui_surf))
    ui_renderer.present()

render_ui()
paddle.position = (paddle_x+X, paddle_y)
ball.position = (ball_pos[0]+X, ball_pos[1])

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_accel -= 1
            if event.key == pygame.K_RIGHT:
                paddle_accel += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle_accel += 1
            if event.key == pygame.K_RIGHT:
                paddle_accel -= 1
##        if event.type == pygame.WINDOWMOVED:
##            if event.window == ball:
##                ball_pos = [event.x, event.y]
##            if event.window == paddle:
##                paddle_x = event.x

    paddle_velocity += paddle_accel * 5
    paddle_x += paddle_velocity
    paddle_velocity *= 0.8

    if not 0 <= paddle_x < W-500:
        paddle_x = max(0, min(W-500, paddle_x))
        if abs(paddle_velocity) > 5:
            paddle_velocity *= -1
        else:
            paddle_velocity = 0

    ball_pos[0] += ball_vel[0]

    if not 0 < ball_pos[0] < W-50:
        ball_vel[0] *= -1
        sound_wall_hit.play()

    ball_pos[1] += ball_vel[1]

    if ball_pos[1] <= 0:
        ball_vel[1] *= -1
        sound_wall_hit.play()

    if ball_pos[1] >= paddle_y-50:
        if (paddle_x - 50) < ball_pos[0] < (paddle_x + 500):
            ball_vel[1] *= -1
            hitpoint = ball_pos[0] + 25 - (paddle_x + 250)
            if hitpoint <= -125:
                current -= 5
                anim_offset -= 5
            elif hitpoint <= 0:
                current -= 1
                anim_offset -= 1
            elif hitpoint < 125:
                current += 1
                anim_offset += 1
            else:
                current += 5
                anim_offset += 5
            current %= len(alphabet)
            sound_paddle_hit.play()
        else:
            ball_vel = [abs(ball_vel[0]), -abs(ball_vel[1])]
            ball_pos = [paddle_x, paddle_y-50]
            sound_score.play()
            typed += alphabet[current]
            if typed[-1] == ENTER:
                typed = typed[:-1]
                break
            elif typed[-1] == CLEAR:
                typed = ""
                current = 0
                anim_offset = 1000
            elif typed[-1] == BACKSPACE:
                typed = typed[:-2]
            elif typed[-1] == SHIFT:
                typed = typed[:-1]
                alphabet = alphabet.upper()
            else:
                alphabet = alphabet.lower()

    if int(paddle_x) != paddle.position[0]:
        paddle.position = (paddle_x+X, paddle_y)
    ball.position = (ball_pos[0]+X, ball_pos[1])
    render_ui()
    clock.tick(60)

ball.destroy()
paddle.destroy()

render_ui(nocursor=True)

for i in range(80):
    pygame.draw.rect(ui_surf, (0, 0, 0), (0, 0, W, i+1))
    ui_renderer.blit(Texture.from_surface(ui_renderer, ui_surf))
    ui_renderer.present()
    clock.tick(60)

for i in range(100):
    ui.position = (ui.position[0], ui.position[1]-5)
    clock.tick(60)
