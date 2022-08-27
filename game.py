import random
from threading import Timer
import pygame

pygame.init()

reloadtime = 1.5
respwantimee = 2
score = 0
resumecountposition = (410, 150)
resumeCount = 0
font1 = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('comicsans', 30)
fontb1 = pygame.font.SysFont('comicsans', 20)
fontc = pygame.font.SysFont('comicsans', 100)
bg = pygame.image.load('res/bg.jpg')
bg1 = pygame.image.load('res/bg1.jpg')

# info
print(
    "\n\n                  WELCOME                           \n\n     Controls: \n  1: click or press LMOUSE to fire "
    "\n  2: click RMOUSE to reload \n  3: press 'a' and 'd' to navigate \n  4: press SPACE to jump \n\n     Rules: \n "
    " 1: Player can fire 10 rounds at a time \n  2: It takes " + str(
        reloadtime) + " seconds to reload  \n  3: Enemy will re-spawn randomly in " + str(
        respwantimee) + "seconds,keep your eyes wide open!  \n  4: Game will continue till the player losses its "
                        "health completely  \n  5: You can see your final score in console  \n\n                    "
                        "CODED BY RC ")

rd = False
run = False

win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("GAME")

# music
pygame.mixer.music.load('res/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
fire = pygame.mixer.Sound('res/bullet1.wav')
hit = pygame.mixer.Sound('res/hit.wav')

# clock
clock = pygame.time.Clock()
# man
char = pygame.image.load('res/standing.png')
wl = [pygame.image.load('res/L1.png'), pygame.image.load('res/L2.png'), pygame.image.load('res/L3.png'),
      pygame.image.load('res/L4.png'), pygame.image.load('res/L5.png'), pygame.image.load('res/L6.png'),
      pygame.image.load('res/L7.png'), pygame.image.load('res/L8.png'), pygame.image.load('res/L9.png')]
wr = [pygame.image.load('res/R1.png'), pygame.image.load('res/R2.png'), pygame.image.load('res/R3.png'),
      pygame.image.load('res/R4.png'), pygame.image.load('res/R5.png'), pygame.image.load('res/R6.png'),
      pygame.image.load('res/R7.png'), pygame.image.load('res/R8.png'), pygame.image.load('res/R9.png')]

# enemy
wle = [pygame.image.load('res/L1E.png'), pygame.image.load('res/L2E.png'), pygame.image.load('res/L3E.png'),
       pygame.image.load('res/L4E.png'), pygame.image.load('res/L5E.png'), pygame.image.load('res/L6E.png'),
       pygame.image.load('res/L7E.png'), pygame.image.load('res/L8E.png'), pygame.image.load('res/L9E.png'),
       pygame.image.load('res/L10E.png'), pygame.image.load('res/L11E.png')]
wre = [pygame.image.load('res/R1E.png'), pygame.image.load('res/R2E.png'), pygame.image.load('res/R3E.png'),
       pygame.image.load('res/R4E.png'), pygame.image.load('res/R5E.png'), pygame.image.load('res/R6E.png'),
       pygame.image.load('res/R7E.png'), pygame.image.load('res/R8E.png'), pygame.image.load('res/R9E.png'),
       pygame.image.load('res/R10E.png'), pygame.image.load('res/R11E.png')]


class Player:
    def __init__(self, x, y, width, height, vel, jp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.jp = jp
        self.wc = 0
        self.jc = 10
        self.left = False
        self.right = False
        self.isjump = False
        self.standing = True
        self.health = 10
        self.hitbox = (self.x + 20, self.y + 12, 24, 52)
        self.visible = True
        self.pause = False

    def draw(self):
        if self.wc + 1 >= 45:
            self.wc = 0
        if not (self.standing):
            if self.left:
                win.blit(wl[self.wc // 5], (self.x, self.y))
                if not (man.pause):
                    self.wc += 1
            elif self.right:
                win.blit(wr[self.wc // 5], (self.x, self.y))
                if not (man.pause):
                    self.wc += 1
        else:
            if self.left:

                win.blit(wl[0], (self.x, self.y))
            else:
                win.blit(wr[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 12, 24, 52)
        pygame.draw.rect(win, (255, 0, 0), (351, 460, 150, 12))
        pygame.draw.rect(win, (0, 125, 0), (351, 460, 150 - ((150 / 10) * (10 - self.health)), 12))
        golicount = font2.render(str(round(10 - reload)) + ' / 10', 1, (120, 0, 0))
        win.blit(golicount, (400, 440))
        pygame.draw.rect(win, (255, 255, 255), (351, 445, 30, 6))
        pygame.draw.rect(win, (0, 0, 255), (351, 445, 30 - ((30 / 10) * reload), 6))

    def hit(self):

        global score
        score -= 1
        if self.health > 0:
            self.visible = True
            self.health -= .8


        else:
            self.visible = False


class Bullet:
    def __init__(self, x, y, color, radius, facing):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.facing = facing
        self.vel = 9 * facing

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy:
    def __init__(self, x, y, width, height, end, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.end = end
        self.wc = 0
        self.hitbox = (self.x + 21, self.y + 1, 20, 55)
        self.health = 19
        self.visible = 1

    def draw(self):

        self.move()
        if self.wc + 1 >= 55:
            self.wc = 0
        if self.vel > 0:
            win.blit(wre[self.wc // 5], (self.x, self.y))
            if not (man.pause):
                self.wc += 1
        else:
            win.blit(wle[self.wc // 5], (self.x, self.y))
            if not (man.pause):
                self.wc += 1
        self.hitbox = (self.x + 21, self.y + 1, 20, 55)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 125, 0),
                         (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / 19) * (19 - self.health)), 10))

    def move(self):
        if not (man.pause):
            if self.vel > 0:
                if self.x + self.width <= self.end:
                    self.x += self.vel

                else:
                    self.vel = self.vel * (-1)
                    self.wc = 0
            else:
                if self.x >= 5:
                    self.x += self.vel

                else:
                    self.vel = self.vel * (-1)
                    self.wc = 0

    def hit(self):
        if self.health > 0:
            self.visible = 1
            self.health -= 1


        else:
            self.visible = 0
        bullets.pop(bullets.index(bullet))


class Button:
    def __init__(self, x, y, width, height, color1, color2=None, text="", font=None, tsize=None, Bold=None, Italic=None,
                 tcolor=None, outc=None, outw=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        self.text = text
        self.font = font
        self.tsize = tsize
        self.Bold = Bold
        self.Italic = Italic
        self.tcolor = tcolor

        self.outc = outc
        self.outw = outw

    def draw(self, win):
        if self.outc:
            pygame.draw.rect(win, self.outc, (
                self.x - self.outw, self.y - self.outw, self.width + (self.outw * 2), self.height + (self.outw * 2)),
                             self.outw)
        pygame.draw.rect(win, self.color1, (self.x, self.y, self.width, self.height))
        if self.text != "":
            if self.tcolor:
                font = pygame.font.SysFont(self.font, self.tsize, self.Bold, self.Italic)
                text = font.render(self.text, True, self.tcolor)
                win.blit(text, (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2)))

    def isover(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        else:
            return False


def do_reload():
    global reload
    global rd

    multiple = 5
    factor = 1 / multiple
    iters = 10 * multiple

    def a():
        global reload
        global rd

        reload -= factor
        if reload <= factor:
            rd = False

    if reload > 0:
        rd = True
        for c in range(1, min(int(reload * multiple), iters) + 1):
            i = Timer((reloadtime * c) / iters, a, args=None, kwargs=None)
            i.start()


def redraw():
    win.blit(bg, (0, 0))

    if not (man.pause):
        buttonPause.text = "PAUSE"
        man.draw()
        if enemy1.visible == 1:
            enemy1.draw()
        else:
            def d():
                enemy1.visible = 1
            t2 = Timer(respwantimee, d, args=None, kwargs=None)
            t2.start()

            enemy1.health = 19
            enemy1.x = random.randint(20, 800)
            enemy1.y = 355
            enemy1.wc = 0
        global rd
        if reload > 8 and not rd:
            reloadkar = font2.render('LOW AMMO', 1, (255, 0, 0))
            win.blit(reloadkar, (380, 240))

        if rd:
            text = font1.render('RELOADING', 1, (0, 120, 0))
            win.blit(text, (380, 240))
            pygame.draw.rect(win, (255, 255, 255), (380, 263, 138, 6))
            pygame.draw.rect(win, (0, 255, 0), (380, 263, 138 - ((138 / 10) * reload), 6))
        hit = font1.render('SCORE: ' + str(score), 1, (0, 0, 0))
        win.blit(hit, (700, 20))
        for bullet in bullets:
            bullet.draw()
    else:
        buttonPause.text = "RESUME"
        man.draw()
        enemy1.draw()
        hit = font1.render('SCORE: ' + str(score), 1, (0, 0, 0))
        win.blit(hit, (700, 20))
        if reload > 8 and not rd:
            reloadkar = font2.render('LOW AMMO', 1, (255, 0, 0))
            win.blit(reloadkar, (380, 240))

        if rd:
            win.blit(font1.render('RELOADING', 1, (0, 120, 0)), (380, 240))

        for bullet in bullets:
            bullet.draw()

        if resumeCount > 0:
            win.blit(fontc.render(str(resumeCount), 1, (255, 0, 0)), resumecountposition)

    buttonPause.draw(win)
    pygame.display.update()


no = 1


def retry():
    win.blit(bg1, (0, 0))
    global score
    global no
    global run
    ready = font2.render("YOUR SCORE : " + str(score), 1, (255, 255, 255))
    win.blit(ready, (350, 200))

    button1.draw(win)
    button2.draw(win)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if button1.isover(pos):
            if no == 1:
                print('Your Scores :\n')
            print(str(no) + ': ' + str(score))

            class player:
                global health
                global visible

            man.health = 11
            enemy1.health = 19
            global reload
            reload = 0
            score = 1
            enemy1.x = random.randint(600, 800)
            man.x = 400
            enemy1.vel = 8
            man.visible = True
            run = True
            no += 1
        if button2.isover(pos):
            run = False
    if event.type == pygame.MOUSEMOTION:
        if button1.isover(pos):
            if button1.color2:
                x1 = button1.color2
                button1.color1 = x1
        else:
            global y1
            button1.color1 = y1
        if button2.isover(pos):

            if button2.color2:
                x2 = button2.color2
                button2.color1 = x2
        else:
            global y2
            button2.color1 = y2

    pygame.display.update()


def resumeGame():
    resumeCounts = 3

    def __in(i):
        global resumeCount
        resumeCount = i

    for i in range(resumeCounts):
        Timer(i, __in, args=(resumeCounts - i, ), kwargs=None).start()

    def final():
        global resumeCount
        resumeCount = 0
        man.pause = False

    Timer(resumeCounts, final, args=None, kwargs=None).start()


man = Player(400, 350, 64, 64, 4, .36)
enemy1 = Enemy(random.randint(600, 800), 355, 64, 64, 840, 8)
button0 = Button(391, 215, 100, 50, (255, 255, 255), (0, 255, 0), "PLAY", 'comicsans', 30, False, False, (0, 0, 0),
                 (0, 0, 0), 2)
button1 = Button(120, 300, 100, 50, (255, 255, 255), (0, 255, 0), "RETRY", 'comicsans', 30, False, False, (0, 0, 0),
                 (0, 0, 0), 2)
button2 = Button(650, 300, 100, 50, (255, 255, 255), (255, 0, 0), "EXIT", 'comicsans', 30, False, False, (0, 0, 0),
                 (0, 0, 0), 2)
buttonPause = Button(20, 20, 100, 27, (255, 255, 255), (0, 255, 0), "PAUSE", 'comicsans', 20, False, False, (0, 0, 0),
                     (0, 0, 0), 2)
# button4 = Button(400, 270, 45, 27, (255, 255, 255), (0, 255, 0), "R", 'comicsans', 30, False, False, (0, 0, 0),
#                  (0, 0, 0), 2)
y1 = button1.color1
y2 = button2.color1
y0 = button0.color1
y3 = buttonPause.color1
# y4 = button4.color1
bullets = []
shootc = 0

reload = 0
score = 0
test = 120
re = False


def start():
    win.blit(bg1, (0, 0))
    ready = font2.render("press any key to continue", 1, (255, 255, 255))

    button0.draw(win)
    global run

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            global run1

            run = False
            run1 = False
        if event.type == pygame.KEYDOWN:
            run = True
            run1 = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button0.isover(pos):
                run = True
                run1 = False
        if event.type == pygame.MOUSEMOTION:

            if button0.isover(pos):
                if button0.color2:
                    x0 = button0.color2
                    button0.color1 = x0
            else:

                button0.color1 = y0
    pygame.display.update()


run1 = True
while run1:
    start()

while run:

    clock.tick(45)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            man.visible = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if not man.pause and reload >= 1:
                    do_reload()
            if event.button == 1:
                if buttonPause.isover(pos):
                    if man.pause:
                        resumeGame()
                    else:
                        man.pause = True

        if event.type == pygame.MOUSEMOTION:
            if buttonPause.isover(pos):
                buttonPause.color1 = buttonPause.color2
            else:
                buttonPause.color1 = y3

    for bullet in bullets:
        if 852 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        if enemy1.visible == 1 and man.visible == True and not (man.pause):
            if bullet.y + bullet.radius > enemy1.hitbox[1] and bullet.y - bullet.radius < enemy1.hitbox[1] + \
                    enemy1.hitbox[3]:
                if bullet.x + bullet.radius > enemy1.hitbox[0] and bullet.x - bullet.radius < enemy1.hitbox[0] + \
                        enemy1.hitbox[2]:
                    enemy1.hit()
                    hit.play()

                    score += 1

    if shootc > 0:
        shootc += 1
    if shootc > 5:
        shootc = 0

    if enemy1.visible == 1 and man.visible == True and not (man.pause):
        if man.hitbox[1] + man.hitbox[3] > enemy1.hitbox[1] and man.hitbox[1] < enemy1.hitbox[1] + enemy1.hitbox[3]:
            if man.hitbox[0] + man.hitbox[2] > enemy1.hitbox[0] and man.hitbox[0] < enemy1.hitbox[0] + enemy1.hitbox[2]:
                man.hit()

    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:

        if shootc == 0:
            if man.left:
                facing = -1
            else:
                facing = 1
            if reload < 10 and man.visible and not (man.pause) and not (rd):
                bullets.append(
                    Bullet(round(man.x + man.width // 2), round(man.y + man.height // 2), (255, 0, 0), 6, facing))
                reload += 1
                fire.play()

            shootc = 1
    if not (man.pause):
        if keys[pygame.K_a] and man.x >= 5:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False

        elif keys[pygame.K_d] and man.x + man.width <= 840:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.wc = 0
        if not (man.isjump):
            if keys[pygame.K_SPACE]:
                man.isjump = True
                man.standing = False
                man.wc = 0
        else:
            if man.jc >= -10:
                n = 1
                if man.jc < 0:
                    n = -1
                man.y -= (man.jc ** 2) * n * man.jp
                man.jc -= 1
            else:
                man.isjump = False
                man.jc = 10

        if keys[pygame.K_LCTRL] and keys[pygame.K_p]:
            man.pause = True
    else:
        if keys[pygame.K_LCTRL] and keys[pygame.K_r]:
             resumeGame()

    if man.visible:
        redraw()

    else:
        retry()

pygame.quit()
