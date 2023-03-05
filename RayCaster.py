import pygame
import math
import random
import time

screen = pygame.display.set_mode((550, 500))

running = True
# player attributes
px ,py = 75, 125
p_angle = 3*math.pi/2
speed = 200
offset2 = 0
darkness = 15000

GameMap = []

def refresh_map():
    global GameMap
    GameMap = [
        [4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4]
    ]

def generate_map():
    global GameMap
    refresh_map()
    x = 0
    y = 0
    for i in range(25):
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        while GameMap[x][y] > 0 or (x == math.floor(px/50) and y == math.floor(py/50)):
            x = random.randint(1, 10)
            y = random.randint(1, 10)
        GameMap[x][y] = random.choice([3])

generate_map()
def showMap():
    x = 0
    y = 0
    for i in GameMap:
        for j in i:
            if j == 1:
                pygame.draw.rect(screen, (255, 255 ,255), (x, y, 39, 39), 2)
            if j == 2:
                pygame.draw.rect(screen, (255, 0 ,0), (x, y, 39, 39), 2)
            if j == 3:
                pygame.draw.rect(screen, (0, 255 ,0), (x, y, 39, 39), 2)
            if j == 4:
                pygame.draw.rect(screen, (0, 0 ,255), (x, y, 39, 39), 2)
            x += 40
        x = 0
        y += 40

def show_player():
    pygame.draw.rect(screen, (255, 255, 0), ((px-5)*4/5, (py-5)*4/5, 10, 10))
    pygame.draw.line(screen, (255, 255, 0), (px*4/5, py*4/5), (px*4/5+math.cos(p_angle)*50, py*4/5+math.sin(p_angle)*50))

def move_player():
    global px, py, p_angle, offset2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        px += math.cos(p_angle)*speed*dt
        py += math.sin(p_angle)*speed*dt
        # offset2 += 0.01

    if keys[pygame.K_s]:
        px -= math.cos(p_angle)*speed*dt
        py -= math.sin(p_angle)*speed*dt
        # offset2 -= 0.01
    
    if keys[pygame.K_a]:
        p_angle -= 2*dt
    
    if keys[pygame.K_d]:
        p_angle += 2*dt

    if keys[pygame.K_UP]:
        offset2 += 0.5
    if keys[pygame.K_DOWN]:
        offset2 -= 0.5
    if offset2 < 1:
        offset2 = 1
    if offset2 > 200:
        offset2 = 200

def caste_rays():
    # ray1
    angle = p_angle - math.pi/6
    for j in range(120):
        angle += math.pi/360
        if angle < 0:
            angle += 2*math.pi
        if angle > 2*math.pi:
            angle = 0
        ray1_found = False
        left = angle > math.pi/2 and angle < 3*math.pi/2
        if left:
            a = -50
            currx1 = math.floor(px//50)*50 - 0.0001
        else:
            a = 50
            currx1 = math.ceil(px//50)*50+50
        curry1 = (px-currx1)*math.tan(-angle)+py
        if currx1//50 >= 0 and currx1//50 < 12 and curry1//50 >= 0 and curry1//50 < 12:
            if left:
                if GameMap[math.floor(curry1//50)][int(currx1//50)] > 0:
                    ray1_found = True
            else:
                if GameMap[math.floor(curry1//50)][int(currx1//50)] > 0:
                    ray1_found = True
        if not ray1_found: 
            for i in range(12):
                currx1 += a
                curry1 = (px-currx1)*math.tan(-angle)+py
                if currx1//50 >= 0 and currx1//50 < 12 and curry1//50 >= 0 and curry1//50 < 12:
                    if left:
                        if GameMap[math.floor(curry1//50)][int(currx1//50)] > 0:
                            break
                    else:
                        if GameMap[math.floor(curry1//50)][int(currx1//50)] > 0:
                            break
        ray1_length = math.sqrt((currx1 - px)**2 + (curry1 - py)**2)
        # ray 1

        # ray 2
        ray2_found = False
        up = angle > math.pi
        if up:
            a = -50
            curry2 = math.floor(py//50)*50 - 0.0001
        else:
            a = 50
            curry2 = math.ceil(py//50)*50 + 50
        currx2 = (py-curry2)/(math.tan(-angle)+0.0001)+px
        if currx2//50 >= 0 and currx2//50 < 12 and curry2//50 >= 0 and curry2//50 < 12:
                if up:
                    if GameMap[int(curry2//50)][math.floor(currx2//50)] > 0:
                        ray2_found = True
                else:
                    if GameMap[int(curry2//50)][math.ceil(currx2//50)] > 0:
                        ray2_found = True
        if not ray2_found:
            for i in range(12):
                curry2 += a
                currx2 = (py-curry2)/(math.tan(-angle)+0.0001)+px
                if currx2//50 >= 0 and currx2//50 < 12 and curry2//50 >= 0 and curry2//50 < 12:
                    if up:
                        if GameMap[int(curry2//50)][math.floor(currx2//50)] > 0:
                            break
                    else:
                        if GameMap[int(curry2//50)][math.ceil(currx2//50)] > 0:
                            break
        ray2_length = math.sqrt((currx2 - px)**2 + (curry2 - py)**2)

        ca = abs(p_angle - angle)
        if ca < 0:
            ca += 2*math.pi
        if ca > math.pi*2:
            ca -= math.pi*2

        if ray1_length > ray2_length:
            ray2_length = ray2_length*math.cos(ca)
            lineH = 520*50/ray2_length
            offset = 200-lineH/2
            value = GameMap[int(curry2//50)][int(currx2//50)]
            cc = 200 - darkness/lineH
            if cc < 0:
                cc = 0
            if cc > 255:
                cc = 255
            colour = [cc, cc, cc]
            if value == 2:
                colour = [cc, 0, 0]
            if value == 3:
                colour = [0, cc, 0]
            if value == 4:
                colour = [0, 0, cc]
            pygame.draw.rect(screen, colour, (j*5-50, offset+offset2, 5, lineH))
            # pygame.draw.line(screen, (255, 255, 255), (px, py), (currx2, curry2))
        else:
            ray1_length = ray1_length*math.cos(ca)
            lineH = 520*50/ray1_length
            offset = 200-lineH/2
            value = GameMap[int(curry1//50)][int(currx1//50)]
            cc = 200 - darkness/lineH
            if cc < 0:
                cc = 0
            if cc > 255:
                cc = 255
            colour = [cc, cc, cc]
            if value == 2:
                colour = [cc, 0, 0]
            if value == 3:
                colour = [0, cc, 0]
            if value == 4:
                colour = [0, 0, cc]
            pygame.draw.rect(screen, colour, (j*5-50, offset+offset2, 5, lineH))
            # pygame.draw.line(screen, (255, 255, 255), (px, py), (currx1, curry1))
        # ray2

prevX = px
prevY = py

show_map = False

def draw_ground():
    cc = 500000/darkness
    for i in range(40):
        cc += 50000/darkness
        if cc > 255:
            cc = 255
        pygame.draw.rect(screen, [0, cc, cc/3], (0, 220+i*7+offset2, 550, 7))

stars = []
for i in range(500):
    stars.append([random.randint(0, 10000), random.randint(0, 500)])

def show_stars():
    a = 0
    for i in stars:
        a = i[0]-p_angle*550
        if a > 2*math.pi:
            a -= 2*math.pi*550
        if a < 0:
            a += 2*math.pi*550
        pygame.draw.rect(screen, (255, 255, 255), (a, 275-i[1]+offset2, 1, 1))

def set_bounds():
    global px, py, prevX, prevY, offset2
    if GameMap[int(py//50)][int(px//50)] and not GameMap[int(prevY//50)][int(prevX//50)]:
        px, py = prevX, prevY
    prevX = px
    prevY = py
    # if offset2 > 50:
    #     offset2 = 50
    # if offset2 < -50:
    #     offset2 = -50

last_time = time.time()

while running:

    screen.fill((0, 0, 30))

    show_stars()

    dt = time.time() - last_time
    last_time = time.time()

    a = -500-p_angle*550
    if a > 2*math.pi:
        a -= 2*math.pi*550
    if a < 0:
        a += 2*math.pi*550
    pygame.draw.ellipse(screen, (225, 225, 225), (a, offset2-50, 60, 60))

    draw_ground()

    caste_rays()

    if show_map:
        showMap()

    if show_map:
        show_player()

    move_player()

    set_bounds()

    if p_angle < 0:
        p_angle += 2*math.pi
    if p_angle > 2*math.pi:
        p_angle -= 2*math.pi

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if show_map:
                    show_map = False
                else:
                    show_map = True
            if event.key == pygame.K_c:
                generate_map()

    pygame.display.update()