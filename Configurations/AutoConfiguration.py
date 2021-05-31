import pygame
import time
import math
pygame.init()
window = pygame.display.set_mode((1200, 600))
points = []
lines = []
begin = False
anim = False
n = 9

# Used to extend line segments out to infinity (or reasonably close to it)
def extend(start,end):
    m = (end[1] - start[1]) / (end[0] - start[0])
    left_y = (m * (-100000 - start[0])) + start[1]
    right_y = (m * (120000 - start[0])) + start[1]
    return [-100000, left_y], [120000, right_y]

# distance formula
def distance(start, end):
    return math.sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)

# determines the next point for auto generation of the configuration.
# Only used from j = 3 to n-3
def getNextPoint(p1, p2, p3, s):
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    y = m * ((p3[0] + s) - p1[0]) + p1[1]
    return [p3[0] + s, y]

# Scales distance between point and center of window
def scale(point,s):
    newX = point[0] - (600 - point[0]) * s
    newY = point[1] - (300 - point[1]) * s
    return [newX,newY]

# Scales all points and lines based on desired percentage
def scaler(p,l,s):
    if len(p) != len(l):
        print("ERROR")
    newPoints = []
    newLines = []
    for j in range(len(p)):
        newPoints.append([scale(p[j][0],s),scale(p[j][1],s)])
        newLines.append([scale(l[j][0],s),scale(l[j][1],s)])
    return newPoints,newLines


# Auto generates a configuration of n points, based on the algorithm from section 2.1
def generate(num):
    print(num)
    genPoints = []
    genLines = []

    p2 = [200, 300]
    p4 = [400, 300]
    p3 = [325, 275]
    genPoints.append([p2,p4])
    genPoints.append([p2, p3])
    genPoints.append([p3, p4])
    genLines.append(list(extend(p2,p4)))
    genLines.append(list(extend(p2,p3)))
    genLines.append(list(extend(p3,p4)))

    for j in range(3, num-3):
        genPoints.append(
            [genPoints[j - 1][1], getNextPoint(genPoints[j - 2][0], genPoints[j - 2][1], genPoints[j - 1][1], 150)])
        genLines.append(
            list(extend(genPoints[j - 1][1], getNextPoint(genPoints[j - 2][0], genPoints[j - 2][1], genPoints[j - 1][1], 150)))
        )
    return genPoints,genLines

# pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                points = []
                lines = []
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_DOWN:
                for i in range(len(points)):
                    points[i][0][1] += 10
                    points[i][1][1] += 10
                for i in range(len(lines)):
                    lines[i][0][1] += 10
                    lines[i][1][1] += 10
            if event.key == pygame.K_UP:
                for i in range(len(points)):
                    points[i][0][1] -= 10
                    points[i][1][1] -= 10
                for i in range(len(lines)):
                    lines[i][0][1] -= 10
                    lines[i][1][1] -= 10
            if event.key == pygame.K_LEFT:
                for i in range(len(points)):
                    points[i][0][0] -= 10
                    points[i][1][0] -= 10
                for i in range(len(lines)):
                    lines[i][0][0] -= 10
                    lines[i][1][0] -= 10
            if event.key == pygame.K_RIGHT:
                for i in range(len(points)):
                    points[i][0][0] += 10
                    points[i][1][0] += 10
                for i in range(len(lines)):
                    lines[i][0][0] += 10
                    lines[i][1][0] += 10
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                temp = generate(n)
                points = temp[0]
                lines.extend(temp[1])
                anim = True
            if event.key == pygame.K_k:
                temp = scaler(points,lines,.1)
                points = temp[0]
                lines = temp[1]
            if event.key == pygame.K_l:
                temp = scaler(points,lines,-.1)
                points = temp[0]
                lines = temp[1]
            if event.key == pygame.K_LEFTBRACKET:
                if n - 1 > 8:
                    n -= 1
            if event.key == pygame.K_RIGHTBRACKET:
                n += 1
    window.fill((255, 255, 255))
    # Remaining code is used to manually draw points and lines
    # as well as blit everything to the screen
    if any(pygame.mouse.get_pressed()) and not begin:
        posStart = pygame.mouse.get_pos()
        begin = True

    if begin:
        posNow = pygame.mouse.get_pos()
        pygame.draw.line(window, (255, 0, 0), (posStart[0], posStart[1]), (posNow[0], posNow[1]))

    if not any(pygame.mouse.get_pressed()) and begin:
        for i in range(len(points)):
            if distance(posStart, points[i][0]) < 20:
                posStart = points[i][0]
            if distance(posStart, points[i][1]) < 20:
                posStart = points[i][1]
            if distance(posNow, points[i][0]) < 20:
                posEnd = points[i][0]
            if distance(posNow, points[i][1]) < 20:
                posEnd = points[i][1]
        points.append([list(posStart), list(posNow)])
        lines.append([extend(posStart,posNow)[0],
                      extend(posStart,posNow)[1]])
        begin = False
    if anim:
        for i in range(len(points)):
            pygame.draw.circle(window, (255, 0, 0), points[i][0], radius=5)
            pygame.draw.circle(window, (255, 0, 0), points[i][1], radius=5)
            pygame.draw.line(window, (255, 0, 0), lines[i][0], lines[i][1])

            pygame.display.flip()
            time.sleep(.5)
        anim = False
    for i in range(len(points)):
        pygame.draw.circle(window, (0, 0, 0), points[i][0], radius=5)
        pygame.draw.circle(window, (0, 0, 0), points[i][1], radius=5)
        pygame.draw.line(window, (0, 0, 0), lines[i][0], lines[i][1])
    font2 = pygame.font.SysFont('didot.ttc', 72)
    img = font2.render(str(n), True, (255,0,0))
    window.blit(img, (20, 20))
    pygame.display.flip()
