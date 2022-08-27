import pygame
import math
import api
import os
import sys
from threading import Timer

pygame.init()
pygame.font.init()
pygame.display.init()

main_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
icons_dir = os.path.join(main_dir, "icons")

S_WIDTH, S_HEIGHT = 1200, 700
BG_COLOR = (255, 255, 255)

win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Mouse Tracking")
win.fill(BG_COLOR)

clock = pygame.time.Clock()
FPS = 120
MOUSE_AIM_REF_POS = None        # Reference Mouse Position while Aiming
MOUSE_AIM_ANGLE = 0             # in degrees


class Player:
    L_IM = (pygame.image.load(os.path.join("icons", "L1.png")), pygame.image.load(os.path.join("icons", "L2.png")),
            pygame.image.load(os.path.join("icons", "L3.png")), pygame.image.load(os.path.join("icons", "L4.png")),
            pygame.image.load(os.path.join("icons", "L5.png")), pygame.image.load(os.path.join("icons", "L6.png")),
            pygame.image.load(os.path.join("icons", "L7.png")), pygame.image.load(os.path.join("icons", "L8.png")),
            pygame.image.load(os.path.join("icons", "L9.png")))

    R_IM = (pygame.image.load(os.path.join("icons", "R1.png")), pygame.image.load(os.path.join("icons", "R2.png")),
            pygame.image.load(os.path.join("icons", "R3.png")), pygame.image.load(os.path.join("icons", "R4.png")),
            pygame.image.load(os.path.join("icons", "R5.png")), pygame.image.load(os.path.join("icons", "R6.png")),
            pygame.image.load(os.path.join("icons", "R7.png")), pygame.image.load(os.path.join("icons", "R8.png")),
            pygame.image.load(os.path.join("icons", "R9.png")))

    def __init__(self, x, y, s_width=S_WIDTH, s_height=S_HEIGHT):
        self.width, self.height = 30, 50                       # width and height of player image (excluding background)
        self.s_width, self.s_height = s_width, s_height
        self.x, self.y = x, y

        self.facing = 1                                        # 1 for right, -1 for left
        self.move_right = self.move_left = self.move_up = self.move_down = False
        self.walk_count = 0
        self.flight_up_step = 2                                # flight rise in pixels
        self.flight_down_step = 1
        self.walk_step = 3                                     # right or left movement in pixels

        self.movable_area = (10, 10, self.s_width - 10, self.s_height - 100)        # area in which player could move

        self.max_fuel = self.c_fuel = self.movable_area[3] - self.movable_area[1] + 800         # fuel to move up
        self.fuel_filling_time = 2        # in s, in which fuel will will be filled completely
        self.fuel_dec_step = self.flight_up_step
        self.fuel_inc_step = self.fuel_dec_step * 2
        self._fuel_inc_time = (self.fuel_filling_time * self.fuel_inc_step) / self.max_fuel
        self.fuel_fill_start = 1.5        # in ms, after which fuel filling starts

        self.fuel_timer = None

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    @property
    def hitbox(self):
        if self.facing == 1:    # right
            return self.x, self.y, self.width + 5, self.height
        return self.x - 12, self.y, self.width + 5, self.height

    def _fuel_inc(self):
        if self.c_fuel < self.max_fuel:
            self.c_fuel += self.fuel_inc_step
            self.fuel_timer = Timer(self._fuel_inc_time, self._fuel_inc)
            self.fuel_timer.start()
        else:
            if self.fuel_timer:
                self.fuel_timer.cancel()
            self.fuel_timer = None

    def draw(self, surface):
        if self.move_right:
            self.set_right()
            self.move_right = False
        elif self.move_left:
            self.set_left()
            self.move_left = False
        else:
            if self.walk_count:
                self.walk_count = 0

        if self.move_up and self.c_fuel >= self.fuel_dec_step:
            self.set_up()
            self.move_up = False
        else:
            self.move_up = False

            # Filling Fuel
            if self.c_fuel < self.max_fuel and self.fuel_timer is None:
                self.fuel_timer = Timer(self.fuel_fill_start, self._fuel_inc)
                self.fuel_timer.start()

            if self.move_down:
                self.set_down()
            if self.y2 + self.flight_down_step < self.movable_area[3]:
                self.move_down = True
            else:
                self.move_down = False

        if self.walk_count < 0 or self.walk_count >= len(self.L_IM):
            self.walk_count = 0

        if self.facing == 1:
            surface.blit(self.R_IM[self.walk_count], (self.x, self.y))
        else:
            surface.blit(self.L_IM[self.walk_count], (self.x, self.y))

        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def set_right(self):
        if self.x2 + self.walk_step < self.movable_area[2]:
            self.facing = 1
            self.x += self.walk_step
            self.walk_count += 1

    def set_left(self):
        if self.x - self.walk_step > self.movable_area[0]:
            self.facing = -1
            self.x -= self.walk_step
            self.walk_count += 1

    def set_up(self):
        if self.fuel_timer:
            self.fuel_timer.cancel()
            self.fuel_timer = None
        if self.y - self.flight_up_step > self.movable_area[1]:
            self.y -= self.flight_up_step
        self.c_fuel -= self.fuel_dec_step

    def set_down(self):
        if self.y2 + self.flight_down_step < self.movable_area[3]:
            self.y += self.flight_down_step

    def quit(self):
        if self.fuel_timer:
            self.fuel_timer.cancel()
            self.fuel_timer = None


class Gun:
    # Images (max size of image surface even after rotating image is (diagonal, diagonal))
    AKM_IMGS = (pygame.image.load(os.path.join(icons_dir, "akm_r_53x20.png")),
                pygame.image.load(os.path.join(icons_dir, "akm_l_53x20.png")))

    def __init__(self, player__ob: Player, width: int, height: int, images: tuple):
        self.player = player__ob
        self.width, self.height = width, height
        self.images = images                            # in form (right_image, left_image)

        self.diagonal = ((self.width * 2) + (self.height * 2)) ** 0.5

    def draw(self, surface, angle):
        if 90 < angle <= 270:
            __in = 1
            __pos = (self.player.x + (self.player.width / 2) - self.diagonal, self.player.y + 10)
        else:
            __in = 0
            __pos = (self.player.x + (self.player.width / 2), self.player.y + 10)

        surface.blit(pygame.transform.rotate(self.images[__in], angle), __pos)


class PlayerStat:
    fuel_img = pygame.image.load(os.path.join(icons_dir, "akm_r_53x20.png"))
    fuel_img_dim = fuel_img.get_width(), fuel_img.get_height()

    gun_img = None     # need to be set

    def __init__(self, player__ob: Player, x: int, y: int, width: int, height: int):
        self.player = player__ob
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.outline_color = (0, 0, 0)          # also used in bars outline
        self.outline_thickness = 2              # also used in bars outline

        # Fuel Bar ............................................................................................
        self.fuel_bar_color = (255, 120, 46)     # color of fuel bar
        self.fuel_bar_width, self.fuel_bar_height = self.width - self.fuel_img_dim[0] - 20, (self.height / 2) - 6
        self.fuel_bar_x, self.fuel_bar_y = self.x + self.fuel_img_dim[0] + 10, self.y + (self.height / 2) + 3
        self.in_fuel_bar_x, self.in_fuel_bar_y = self.fuel_bar_x + self.outline_thickness, self.fuel_bar_y + self.outline_thickness
        self.in_fuel_bar_max_width = self.fuel_bar_width - (self.outline_thickness * 2)

        self.fuel_img_pos = (self.x, self.fuel_bar_y)

    def draw(self, surface):
        self.draw_fuel_bar(surface)

    def draw_fuel_bar(self, surface):
        surface.blit(self.fuel_img, self.fuel_img_pos)
        pygame.draw.rect(surface, self.outline_color, (self.fuel_bar_x, self.fuel_bar_y, self.fuel_bar_width, self.fuel_bar_height), self.outline_thickness)
        pygame.draw.rect(surface, self.fuel_bar_color, (self.in_fuel_bar_x, self.in_fuel_bar_y, self.in_fuel_bar_max_width * (self.player.c_fuel / self.player.max_fuel), self.fuel_bar_height - (self.outline_thickness * 2)), 0)


def set_aim_angle(ref_pos=MOUSE_AIM_REF_POS):
    global MOUSE_AIM_ANGLE
    angle = api.get_angle(pygame.mouse.get_pos(), ref_pos)
    if angle is not None:
        MOUSE_AIM_ANGLE = math.degrees(angle)


def redraw(surface):
    surface.fill(BG_COLOR)  # or background image

    player.draw(surface)
    Akm.draw(surface, MOUSE_AIM_ANGLE)
    stat.draw(surface)

    pygame.display.update()


player = Player(100, S_HEIGHT - 148)
stat = PlayerStat(player, S_WIDTH - 160, 10, 160, 40)
Akm = Gun(player, 53, 20, Gun.AKM_IMGS)

while True:
    clock.tick(FPS)
    redraw(win)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.quit()
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            if MOUSE_AIM_REF_POS is None:
                MOUSE_AIM_REF_POS = pygame.mouse.get_pos()
            else:
                set_aim_angle(MOUSE_AIM_REF_POS)
        else:
            MOUSE_AIM_REF_POS = None

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player.move_up = True
    if keys[pygame.K_DOWN]:
        player.move_down = True
    if keys[pygame.K_LEFT]:
        player.move_left = True
    if keys[pygame.K_RIGHT]:
        player.move_right = True
