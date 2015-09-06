import pygame
from math import sin, cos, radians
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLUE_GREEN = (0, 100, 255)
PADDLE_SPEED = 3
BALL_SPEED = 4*PADDLE_SPEED/3
PADDLE_HEIGHT = 4

def cosd(deg):
    return cos(radians(deg))

def sind(deg):
    return sin(radians(deg))

def createPaddle():
    # width, height, xPos, color
    return (50, PADDLE_HEIGHT, SCREEN_WIDTH/2, BLUE_GREEN)

def createBall(paddle):
    (pw, ph, px, pc) = paddle
    radius = 6
    initial_angle = 30
    xDir = BALL_SPEED * cosd(initial_angle)
    yDir = BALL_SPEED * sind(initial_angle)
    # width, xPos, yPos, color, xDir, yDir
    return (radius, px, SCREEN_HEIGHT - (ph + radius), BLUE_GREEN, xDir, yDir)

def createBrick(paddle, xPos, yPos):
    (pw, ph, px, pc) = paddle
    # width, height, xPos, yPos, color
    return (pw, 2*ph, xPos, yPos, BLUE_GREEN)

def createWorld():
    # paddle, ball, bricks, kpm
    paddle = createPaddle()
    ball = createBall(paddle)
    bricks = []
    keyPressMap = {}
    return (paddle, ball, bricks, keyPressMap)

def isKeyPressed(kpm, key):
    return key in kpm and kpm[key]

def when(cond, cns, alt):
    if cond:
        return cns
    else:
        return alt

def rand_color(color):
    (r, g, b) = color
    magnitude_big_enough = False
    while not magnitude_big_enough:
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        magnitude_big_enough = r + g + b >= 80
    return (r, g, b)

def checkBounds(paddle, ball, bricks, kpm):
    (pw, ph, px, pc) = paddle
    new_px = min(SCREEN_WIDTH - pw/2, max(pw/2, px))
    paddle = (pw, ph, new_px, pc)

    (brad, bx, by, bc, bvx, bvy) = ball
    x_wall_hit = bx <= brad or bx >= SCREEN_WIDTH-brad
    y_wall_hit = by <= brad or by >= SCREEN_HEIGHT-brad
    new_bvx = when(x_wall_hit, -bvx, bvx)
    new_bvy = when(y_wall_hit, -bvy, bvy)
    new_bx = min(SCREEN_WIDTH - brad, max(brad, bx))
    new_by = min(SCREEN_HEIGHT - brad, max(brad, by))
    new_bc = when(x_wall_hit or y_wall_hit, rand_color(bc), bc)
    ball = (brad, new_bx, new_by, new_bc, new_bvx, new_bvy)

    return (paddle, ball, bricks, kpm)

def updateWorld(world):
    done = False
    (paddle, ball, bricks, kpm) = world
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            kpm[event.key] = True
        elif event.type == pygame.KEYUP:
            kpm[event.key] = False

    if isKeyPressed(kpm, pygame.K_ESCAPE):
        done = True

    # Update paddle
    (pw, ph, px, pc) = paddle
    if isKeyPressed(kpm, pygame.K_LEFT):
        paddle = (pw, ph, px-PADDLE_SPEED, pc)
    elif isKeyPressed(kpm, pygame.K_RIGHT):
        paddle = (pw, ph, px+PADDLE_SPEED, pc)

    # Update ball
    (brad, bx, by, bc, bvx, bvy) = ball
    (bxn, byn) = (bx + bvx, by - bvy)
    ball = (brad, bxn, byn, bc, bvx, bvy)

    new_world = checkBounds(paddle, ball, bricks, kpm)

    return (new_world, done)

def drawWorld(world, s):
    s.fill((0,0,0))

    (paddle, ball, bricks, kpm) = world

    # Draw paddle
    (pw, ph, px, pc) = paddle
    pygame.draw.rect(s, pc, ((px - (pw/2)), SCREEN_HEIGHT-ph, pw, ph))

    # Draw ball
    (brad, bx, by, bc, bvx, bvy) = ball
    (bx, by) = (int(round(bx)), int(round(by)))
    pygame.draw.circle(s, bc, (bx, by), brad)

    # Draw bricks
    for brick in bricks:
        (brw, brh, brx, bry, brc) = brick
        pygame.draw.rect(s, brc, ((brx - (brw/2)), (bry - (brh/2)), brw, brh))

    pygame.display.flip()
    return

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Serendipitous Puzzles & Monsters")

    done = False
    clock = pygame.time.Clock()
    world = createWorld()

    while not done:
        drawWorld(world, screen)
        (world, done) = updateWorld(world)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

