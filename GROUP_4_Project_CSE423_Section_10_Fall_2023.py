import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


Window_Width, Window_Height= 500, 780
previous_score = 0
with open("score.txt") as file:
    previous_score = int(file.read())


exhaust = []
num_exhaust = 4

enemyExhaust = []
num_enemyExhaust = 8

stars = []
num_stars = 200

enemyCenterInitalization = random.randrange(-230, 230), 200
enemyCenter = enemyCenterInitalization
enemyColorList = [(0.5, 0.2, 0), (0.5, 0.5, 0), (0.5, 0.2, 0.5), (0, 0.7, 0.5), (0, 0.6, 0.8)]

userSpaceShipInitialPosition = 0, -190
userCurrentSpaceShipCenter = userSpaceShipInitialPosition
speed = 1


left_bullet_center = userCurrentSpaceShipCenter
right_bullet_center = userCurrentSpaceShipCenter
enemy_bullet_center = enemyCenter

score = 0
health_count = 3

background_color = 0.0, 0.0, 0.0
pointSize = 2

circleSize = 2
circleColor = (0, 0.8, 1)

crossColor = 1.0, 0.0, 0.0
backArrowColor = 0.0, 0.7, 0.8
playPauseColor = 0.0, 0.5, 0.0
userCurrentSpaceShipColor = 1.0, 1.0, 1.0
enemyColor = random.choice(enemyColorList)



# center of buttons on the top part:
button_center = 0, 232.5

paused = False
gameOver = False
x2 = 0


def init():
    r, g, b = background_color
    glClearColor(r, g, b, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)




def draw_exhaust(x, y):
    drawLine_8_waySymmetry(x-70, y, x-70, y + 10, (1.0, 1.0, 1.0))
    drawLine_8_waySymmetry(x+70, y, x+70, y + 10, (1.0, 1.0, 1.0))

def draw_enemyExhaust(x, y):
    drawLine_8_waySymmetry(x, y, x, y + 10, (1.0, 1.0, 1.0))
    
def reset():
    global speed, enemyCenter, score, gameOver, paused, userCurrentSpaceShipColor, enemyColor, health_count, enemyExhaust
    speed = 1
    health_count = 3
    score = 0
    paused = False
    gameOver = False
    enemyColor = random.choice(enemyColorList)
    x, y = enemyCenterInitalization
    enemyCenter = random.randrange(-230, 230), y
    userCurrentSpaceShipColor = 1.0, 1.0, 1.0

    enemyX, enemyY = enemyCenter
    # UPDATE ENEMY EXHAUST COORDINATES
    for i in range(num_enemyExhaust):
        enemyExhaustX = (enemyX - 12) + i*3 
        enemyExhaustY = random.randint(enemyY+14, enemyY+18)
        enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)
    
    print(f'Starting Over!')


def convert_coordinate(oldX, oldY):
    newX = oldX - (Window_Width/2) + 6
    newY = (Window_Height/2 - oldY)*((500)/Window_Height) + 6
    return newX, newY


def draw_point(x, y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)
    glVertex2f(x, y)
    glEnd()


def draw_circle(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(y + c_x, -x + c_y)
    glVertex2f(x + c_x, -y + c_y)
    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-y + c_x, -x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)

    glEnd()

def draw_semi_circle(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if(abs(dx) >= abs(dy)):
        if(dx > 0):
            if(dy > 0):
                zone = 0
            else:
                zone = 7
        else:
            if(dy > 0):
                zone = 3
            else:
                zone = 4
    else:
        if(dy > 0):
            if(dx > 0):
                zone = 1
            else:
                zone = 2
        else:
            if(dx > 0):
                zone = 6
            else:
                zone = 5
    
    return zone

def anyZoenToZoneZero(x0, y0, x1, y1, color):
    zone = findZone(x0, y0, x1, y1)
    if(zone == 0):
        drawLine_0(x0, y0, x1, y1, zone, color)
    if(zone == 1):
        drawLine_0(y0, x0, y1, x1, zone, color)
    if(zone == 2):
        drawLine_0(y0, -x0, y1, -x1, zone, color)
    if(zone == 3):
        drawLine_0(-x0, y0, -x1, y1, zone, color)
    if(zone == 4):
        drawLine_0(-x0, -y0, -x1, -y1, zone, color)
    if(zone == 5):
        drawLine_0(-y0, -x0, -y1, -x1, zone, color)
    if(zone == 6):
        drawLine_0(-y0, x0, -y1, x1, zone, color)
    if(zone == 7):
        drawLine_0(x0, -y0, x1, -y1, zone, color)


def zoneZeroToOriginalZone(x, y, zone):
    if(zone == 0):
        return (x, y)
    if(zone == 1):
        return (y, x)
    if(zone == 2):
        return (-y, x)
    if(zone == 3):
        return (-x, y)
    if(zone == 4):
        return (-x, -y)
    if(zone == 5):
        return (-y, -x)
    if(zone == 6):
        return (y, -x)
    if(zone == 7):
        return (x, -y)


def drawLine_8_waySymmetry(x0, y0, x1, y1, color):
    anyZoenToZoneZero(x0, y0, x1, y1, color)


def drawLine_0(x0, y0, x1, y1, zone, color):
    # MID-POINT LINE DRAWING ALGORITHM (FOR ZONE 0): 
    dx = x1 - x0
    dy = y1 - y0
    delE = 2*dy
    delNE = 2*(dy-dx)
    d = 2*dy -dx
    x = x0
    y = y0

    while( x <= x1):
        originalX, originalY = zoneZeroToOriginalZone(x, y, zone)
        draw_point(originalX, originalY, pointSize, color)
        if(d < 0):
            d += delE
            x += 1
        else : 
            d += delNE
            x += 1
            y += 1

    


def draw_enemyShip(color):
    x, y = enemyCenter
    drawLine_8_waySymmetry(x-15, y, x-15, y+12, color)
    drawLine_8_waySymmetry(x+15, y+12, x+15, y, color)
    drawLine_8_waySymmetry(x-15, y+12, x, y, color)
    drawLine_8_waySymmetry(x, y, x+15, y+12, color)
    drawLine_8_waySymmetry(x+15, y, x, y-12, color)
    drawLine_8_waySymmetry(x, y-12, x-15, y, color)


def draw_cross(color):
    x, y = button_center
    drawLine_8_waySymmetry(x+200, y-12.5, x+240, y+12.5, color)
    drawLine_8_waySymmetry(x+200, y+12.5, x+240, y-12.5, color)

def draw_backArrow(color):
    x, y = button_center
    draw_circle_midpoint(x-220, y, 18)
    drawLine_8_waySymmetry(x-238, y+5, x-250, y-10, color)
    drawLine_8_waySymmetry(x-238, y+5, x-225, y-10, color)


def draw_pause(color):
    x, y = button_center
    drawLine_8_waySymmetry(x-10, y+12.5, x-10, y-12.5, (color))
    drawLine_8_waySymmetry(x+10, y+12.5, x+10, y-12.5, color)

def draw_play(color):
    x, y = button_center
    drawLine_8_waySymmetry(x-20, y+12.5, x+20, y, color)
    drawLine_8_waySymmetry(x+20, y, x-20, y-12.5, color)
    drawLine_8_waySymmetry(x-20, y-12.5, x-20, y+12.5, color)

def draw_pause_play(color):
    if(paused):
        draw_play(color)
    else:
        draw_pause(color)

def draw_userShip_triangle(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x-80, y-50, x+80, y-50, color)

    drawLine_8_waySymmetry(x-65, y+20, x, y+60, color)
    drawLine_8_waySymmetry(x+65, y+20, x, y+60, color)

    drawLine_8_waySymmetry(x-65, y+10, x, y+50, color)
    drawLine_8_waySymmetry(x+65, y+10, x, y+50, color)

    drawLine_8_waySymmetry(x-15, y-50, x, y-60, color)
    drawLine_8_waySymmetry(x+15, y-50, x, y-60, color)

def draw_left_misile(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x-75, y-50, x-75, y+50, color)
    drawLine_8_waySymmetry(x-65, y-50, x-65, y+50, color)
    drawLine_8_waySymmetry(x-75, y+50, x-70, y+55, color)
    drawLine_8_waySymmetry(x-70, y+55, x-65, y+50, color)
    drawLine_8_waySymmetry(x-75, y-50, x-70, y-55, color)
    drawLine_8_waySymmetry(x-70, y-55, x-65, y-50, color)

def draw_right_misile(color):
    x, y = userCurrentSpaceShipCenter
    drawLine_8_waySymmetry(x+75, y-50, x+75, y+50, color)
    drawLine_8_waySymmetry(x+65, y-50, x+65, y+50, color)
    drawLine_8_waySymmetry(x+75, y+50, x+70, y+55, color)
    drawLine_8_waySymmetry(x+70, y+55, x+65, y+50, color)
    drawLine_8_waySymmetry(x+75, y-50, x+70, y-55, color)
    drawLine_8_waySymmetry(x+70, y-55, x+65, y-50, color)


def draw_right_bullet(color):
    x, y  = right_bullet_center
    drawLine_8_waySymmetry(x+70, y+55, x+70, y+60, color)

def draw_left_bullet(color):
    x, y  = left_bullet_center
    drawLine_8_waySymmetry(x-70, y+55, x-70, y+60, color)

def draw_enemy_bullet(color):
    x, y = enemy_bullet_center
    drawLine_8_waySymmetry(x, y-15, x, y-20, color)

def draw_health(dx, dy, color):
    x, y = button_center
    drawLine_8_waySymmetry(x+dx, y-dy, x+dx+15, y+dy, color)
    drawLine_8_waySymmetry(x+dx-15, y+dy, x+dx, y-dy, color)
    draw_semi_circle_midpoint(x+dx+7.5, y+dy, 7.5, color)
    draw_semi_circle_midpoint(x+dx-7.5, y+dy, 7.5, color)



def draw_semi_circle_right(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(y + c_x, -x + c_y)
    glVertex2f(x + c_x, -y + c_y)
    glEnd()

def draw_semi_circle_midpoint_right(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_right(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_right(x, y, c_x, c_y, circleSize, color)



def draw_semi_circle_for_5(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(x + c_x, y + c_y)
    glVertex2f(y + c_x, x + c_y)
    glVertex2f(y + c_x, -x + c_y)
    glVertex2f(x + c_x, -y + c_y)
    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()

def draw_semi_circle_midpoint_for_5(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_for_5(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_for_5(x, y, c_x, c_y, circleSize, color)


def draw_semi_circle_left(x, y, c_x, c_y, s, color):
    glPointSize(s)
    glBegin(GL_POINTS)
    r, g, b = color
    glColor3f(r, g, b)

    glVertex2f(-x + c_x, -y + c_y)
    glVertex2f(-y + c_x, -x + c_y)
    glVertex2f(-y + c_x, x + c_y)
    glVertex2f(-x + c_x, y + c_y)
    glEnd()

def draw_semi_circle_midpoint_left(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle_left(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle_left(x, y, c_x, c_y, circleSize, color)



def draw_0(x, y, color):
    draw_circle_midpoint(x, y, 10)

def draw_1(x, y, color):
    drawLine_8_waySymmetry(x-10, y+5, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x, y-10, color)

def draw_2(x, y, color):
    draw_semi_circle_midpoint(x, y+5, 5, color)
    drawLine_8_waySymmetry(x+6, y+6, x-5, y-10, color)
    drawLine_8_waySymmetry(x-5, y-10, x+10, y-10, color)

def draw_3(x, y, color):
    draw_semi_circle_midpoint_right(x, y+5, 5, color)
    draw_semi_circle_midpoint_right(x, y-5, 5, color)

def draw_4(x, y, color):
    drawLine_8_waySymmetry(x-10, y, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x, y-10, color)
    drawLine_8_waySymmetry(x-10, y, x+5, y, color)

def draw_5(x, y, color):
    drawLine_8_waySymmetry(x-10, y+10, x+5, y+10, color)
    drawLine_8_waySymmetry(x-10, y+10, x-10, y, color)
    draw_semi_circle_midpoint_for_5(x-3, y-3, 7, color)

def draw_6(x, y, color):
    draw_semi_circle_midpoint_left(x, y, 10, color)
    draw_circle_midpoint(x-2, y-3.5, 6)

def draw_7(x, y, color):
    drawLine_8_waySymmetry(x-10, y+10, x, y+10, color)
    drawLine_8_waySymmetry(x, y+10, x-10, y-10, color)

def draw_8(x, y, color):
    draw_circle_midpoint(x, y+5, 5)
    draw_circle_midpoint(x, y-5, 5)

def draw_9(x, y, color):
    draw_semi_circle_midpoint_right(x, y, 10, color)
    draw_circle_midpoint(x+2, y+3.5, 6)

def draw_score(actualScore, distance):
    x, y = button_center
    tempScore = actualScore
    remainder = tempScore%10

    while(tempScore != None):

        if(remainder == 0):
            draw_0(x-140 + distance, y, circleColor)
        elif(remainder == 1):
            draw_1(x-140 + distance, y, circleColor)
        elif(remainder == 2):
            draw_2(x-140 + distance, y, circleColor)
        elif(remainder == 3):
            draw_3(x-140 + distance, y, circleColor)
        elif(remainder == 4):
            draw_4(x-140 + distance, y, circleColor)
        elif(remainder == 5):
            draw_5(x-140 + distance, y, circleColor)
        elif(remainder == 6):
            draw_6(x-140 + distance, y, circleColor)
        elif(remainder == 7):
            draw_7(x-140 + distance, y, circleColor)
        elif(remainder == 8):
            draw_8(x-140 + distance, y, circleColor)
        else:
            draw_9(x-140 + distance, y, circleColor) 
        
        tempScore = tempScore // 10  
        remainder = tempScore % 10
        
        distance -= 30
        if(tempScore == 0):
            tempScore = None         
    


def draw_score_partition(color, x, y):
    drawLine_8_waySymmetry(x, y+20, x, y-20, color)
    drawLine_8_waySymmetry(x-90, y+20, x+70, y+20, color)
    drawLine_8_waySymmetry(x-90, y-20, x+70, y-20, color)
    drawLine_8_waySymmetry(x-90, y+20, x-90, y-20, color)
    drawLine_8_waySymmetry(x+70, y+20, x+70, y-20, color)

def draw_circle_midpoint(c_x, c_y, r):
    x = 0
    y = r
    d = 5 - 4*r
    draw_circle(x, y, c_x, c_y, circleSize, circleColor)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_circle(x, y, c_x, c_y, circleSize, circleColor)


def draw_semi_circle_midpoint(c_x, c_y, r, color):
    x = 0
    y = r
    d = 5 - 4*r
    draw_semi_circle(x, y, c_x, c_y, circleSize, color)
    while(y > x):
        if(d < 0):
            d += 4*(2*x + 3)
        else:
            d += 4*(-2*y + 2*x +5)
            y-=1
        x+=1
        draw_semi_circle(x, y, c_x, c_y, circleSize, color)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    r, g, b = background_color
    glClearColor(r, g, b, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    draw_enemyShip(enemyColor)
    draw_cross(crossColor)
    draw_backArrow(backArrowColor)
    draw_pause_play(playPauseColor)
    draw_userShip_triangle(userCurrentSpaceShipColor)
    c_x, c_y = userCurrentSpaceShipCenter
    draw_circle_midpoint(c_x, c_y, 50)
    draw_left_misile(userCurrentSpaceShipColor)
    draw_right_misile(userCurrentSpaceShipColor)

    draw_right_bullet(userCurrentSpaceShipColor)
    draw_left_bullet(userCurrentSpaceShipColor)
    draw_enemy_bullet(userCurrentSpaceShipColor)

    for i in range(health_count):
        draw_health(60 + (i*40), 8, (1.0, 0, 0))



    for particles in exhaust:
        x, y = particles
        draw_exhaust(x, y)


    # DRAW ENEMY EXHAUST
    for coordinates in enemyExhaust:
        x, y = coordinates
        draw_enemyExhaust(x, y)


    for star_coordinates in stars:
        x, y = star_coordinates
        draw_point(x, y, 1, (1.0, 1.0, 1.0))



    draw_score(score, 90)
    bx, by = button_center
    draw_score_partition(circleColor, bx - 100, by)
    draw_score(previous_score, 0)

    glutSwapBuffers()




def printGameState():
    global previous_score
    if(not gameOver):
        print(f'Score: {score}')
    else:
        print(f'Game Over!', end=" ")
        if(score > previous_score):
            print(f'[You made new high score', end=" ")
            previous_score = score
        else:
            print(f'[Previous High Score : {previous_score}', end=" | ")
        print(f'Your Score : {score}]')
    



def animate():
    global enemyCenter, speed, score, gameOver, enemyColor, userCurrentSpaceShipColor, left_bullet_center, right_bullet_center, health_count, userCurrentSpaceShipCenter, enemy_bullet_center, exhaust, enemyExhaust, stars
    enemyX, enemyY = enemyCenter

    
    
    userCurrentSpaceShipX, userCurrentSpaceShipY = userCurrentSpaceShipCenter
    bulletX1, bulletY1 = left_bullet_center
    bulletX2, bulletY2 = right_bullet_center
    enemy_bullet_X, enemy_bullet_Y = enemy_bullet_center

    # ENEMY BULLET MOVEMENT
    if((enemy_bullet_X >= userCurrentSpaceShipX-75) and (enemy_bullet_X <= userCurrentSpaceShipX+75) and (enemy_bullet_Y-20 <= userCurrentSpaceShipY+55) and (enemy_bullet_Y-15 >= userCurrentSpaceShipY-55)):
        health_count-=1

        
        print("bullet hit")

        if(health_count==0):
            gameOver = True
            printGameState()
            userCurrentSpaceShipColor = 1.0, 0.0, 0.0

            
           
        if(health_count>0):
            userCurrentSpaceShipCenter = userSpaceShipInitialPosition
            enemy_bullet_center = enemyCenter

            # RESETTING THE EXHAUST POSITION
            ox, oy = userCurrentSpaceShipCenter
            for i in range(num_exhaust):
                exhaustX = ox + i*2.5 - (5)
                exhaustY = random.randint(oy-70, oy-60)
                exhaust[i] = (exhaustX, exhaustY)

    elif(enemy_bullet_Y >= (-Window_Height/2)):
        enemy_bullet_Y -= 3*speed
        enemy_bullet_center = enemy_bullet_X, enemy_bullet_Y
    else:
        enemy_bullet_center = enemyCenter

    # USER SPACESHIP BULLET MOVEMENT
    if( bulletX1-70 >= enemyX-16 and bulletX1-70 <= enemyX+16 and bulletY1+60 >= enemyY-12 and bulletY1+55 <= enemyY+12):
        left_bullet_center = userCurrentSpaceShipCenter
        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY

        # UPDATE ENEMY EXHAUST COORDINATES
        for i in range(num_enemyExhaust):
            enemyExhaustX = enemyX + i*3 - 12
            enemyExhaustY = random.randint(enemyY+14, enemyY+18)
            enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)

        score+=1
        printGameState()
    elif(bulletY1 < (Window_Height/2)-200):
        bulletY1+=10
        left_bullet_center = bulletX1, bulletY1
    else:
        left_bullet_center = userCurrentSpaceShipCenter

    if( bulletX2+70 >= enemyX-16 and bulletX2+70 <= enemyX+16 and bulletY2+60 >= enemyY-12 and bulletY2+55 <= enemyY+12):
        
        right_bullet_center = userCurrentSpaceShipCenter
        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY

        # UPDATE ENEMY EXHAUST COORDINATES
        for i in range(num_enemyExhaust):
            enemyExhaustX = enemyX + i*3 - 12
            enemyExhaustY = random.randint(enemyY+14, enemyY+18)
            enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)

        score+=1
        printGameState()
    elif(bulletY2 < (Window_Height/2)-200):
        bulletY2+=10
        right_bullet_center = bulletX2, bulletY2
    else:
        right_bullet_center = userCurrentSpaceShipCenter


    
    if(enemyX+10 >= userCurrentSpaceShipX-75 and enemyX-13 <= userCurrentSpaceShipX+75 and enemyY-10 <= userCurrentSpaceShipY+55 and enemyY+10 >= userCurrentSpaceShipY-55):

            health_count-=1

            if(health_count==0):
                gameOver = True
                printGameState()
                userCurrentSpaceShipColor = 1.0, 0.0, 0.0
                
            if(health_count>0):
                userCurrentSpaceShipCenter = userSpaceShipInitialPosition

                # RESETTING THE EXHAUST POSITION
                ox, oy = userCurrentSpaceShipCenter
                for i in range(num_exhaust):
                    exhaustX = ox + i*2.5 - (5)
                    exhaustY = random.randint(oy-70, oy-60)
                    exhaust[i] = (exhaustX, exhaustY)

            
            print("crash hit")
            enemyY = 200
            enemyX = random.randrange(-230, 230)
            enemyCenter = enemyX, enemyY
            enemyColor = random.choice(enemyColorList)

            # UPDATE ENEMY EXHAUST COORDINATES
            for i in range(num_enemyExhaust):
                enemyExhaustX = enemyX + i*3 - 12
                enemyExhaustY = random.randint(enemyY+14, enemyY+18)
                enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)

    elif(enemyY>(-240-30)):
        enemyY-=speed
        # enemyY-=0.0000001
        enemyCenter = enemyX, enemyY

        # UPDATE ENEMY EXHAUST COORDINATES
        for i in range(num_enemyExhaust):
            enemyExhaustX, enemyExhaustY = enemyExhaust[i]
            enemyExhaustY-=speed
            enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)
    else:
        

        enemyY = 200
        enemyX = random.randrange(-230, 230)
        enemyCenter = enemyX, enemyY
        enemyColor = random.choice(enemyColorList)

        # UPDATE ENEMY EXHAUST COORDINATES
        for i in range(num_enemyExhaust):
            enemyExhaustX, enemyExhaustY = enemyExhaust[i]
            enemyExhaustX = enemyX + i*3 - 12
            enemyExhaustY = random.randint(enemyY+14, enemyY+18)
            enemyExhaust[i] = (enemyExhaustX, enemyExhaustY)

    speed+=0.001





    # USER SHIP EXHAUST
    ox, oy = userCurrentSpaceShipCenter
    for i in range(num_exhaust):
        x, y = exhaust[i]
        y -= 0.9
        if y < oy-70:
            y = oy-60
        
        exhaust[i] = (x, y)


    # ENEMY SHIP EXHAUST
    ex, ey = enemyCenter
    for i in range(num_enemyExhaust):
        x, y = enemyExhaust[i]
        y += 0.6
        if y > ey+20:
            y = ey+14
        
        enemyExhaust[i] = (x, y)


    # STARS
    for i in range(num_stars):
        x, y = stars[i]
        y -= (1)
        if(y < -Window_Height/2):
            y = Window_Height/2

        stars[i] = (x, y)

    glutPostRedisplay()



def idleFunction():
    if(not gameOver):
        if(not paused):
            animate()
    



def specialKeyListener(key, x, y):
    global userCurrentSpaceShipCenter, exhaust
    x, y = userCurrentSpaceShipCenter
    if(not gameOver and not paused):
        if key==GLUT_KEY_LEFT:
            if(x>-250+80):
                x-=10
                
                
                
                for i in range(num_exhaust):
                    exhaustX, exhaustY = exhaust[i]
                    exhaustX-=10
                    exhaust[i] = (exhaustX, exhaustY)

        if key==GLUT_KEY_RIGHT:
            if(x<250-80):
                x+=10

                ox, oy = userCurrentSpaceShipCenter
                for i in range(num_exhaust):
                    exhaustX, exhaustY = exhaust[i]
                    exhaustX+=10
                    exhaust[i] = (exhaustX, exhaustY)   

        if key==GLUT_KEY_UP:
            if(y<((Window_Height/2)-150)):
                y+=10

                ox, oy = userCurrentSpaceShipCenter
                for i in range(num_exhaust):
                    exhaustX, exhaustY = exhaust[i]
                    exhaustY+=10
                    exhaust[i] = (exhaustX, exhaustY)
                                    
        if key==GLUT_KEY_DOWN:
            if(y>(-(Window_Height/2)+200)):
                y-=10

                ox, oy = userCurrentSpaceShipCenter
                for i in range(num_exhaust):
                    exhaustX, exhaustY = exhaust[i]
                    exhaustY-=10
                    exhaust[i] = (exhaustX, exhaustY)

        userCurrentSpaceShipCenter = x, y
    glutPostRedisplay()


def closeGame():
    global previous_score
    print(f'Goodbye! Score: {score}')

    # Saving Highest Score to file     
    if(score > previous_score):
        previous_score = score
    with open("score.txt", "w") as file:
        file.write(str(previous_score))

    glutLeaveMainLoop()


def mouseListener(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        btnX, btnY = button_center
        c_x, c_y = convert_coordinate(x, y)

        if(c_x < -150):
            c_x = c_x - 6
        if(c_x>=btnX+200 and c_x<=btnX+240 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
            closeGame()
        elif(c_x>=btnX-240 and c_x<=btnX-200 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
            reset()
        else:
            c_x, c_y = c_x - 6 , c_y
            if(not paused):
                if(c_x>=btnX-10 and c_x<=btnX+10 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
                    paused = True
            else:
                if(c_x>=btnX-20 and c_x<=btnX+20 and c_y>=btnY-12.5 and c_y<=btnY+12.5):
                    paused = False





def main():

    global exhaust, enemyExhaust, stars

    ox, oy = userCurrentSpaceShipCenter

    ex, ey = enemyCenter

    # Initialize userShip Exhaust positions
    for _ in range(num_exhaust):
        x = ox + _*2.5 - (5)
        y = random.randint(oy-70, oy-60)
        exhaust.append((x, y))

    # Initialize enemyShip Exhaust positions
    for _ in range(num_enemyExhaust):
        x = ex + _*3 - (12)
        y = random.randint(ey+14, ey+18)
        enemyExhaust.append((x, y))


    # Initialize stars
    for _ in range(num_stars):
        x = random.randint(-Window_Width//2, Window_Width//2)
        y = random.randint(-Window_Height//2, Window_Height//2)
        stars.append((x, y))

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(Window_Width, Window_Height)
    glutInitWindowPosition(560, 0)
    glutCreateWindow(b"Catch The enemy Game")
    glutIdleFunc(idleFunction)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    glutDisplayFunc(display)
    init()

    
    glutMainLoop()

if __name__ == "__main__":
    main()














# https://mcfletch.github.io/pyopengl/documentation/manual/glutSpecialFunc.html