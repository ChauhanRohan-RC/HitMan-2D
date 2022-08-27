import math


def get_angle(pos, ref_pos):
    """
    return: angle in radians which line joining position and reference position makes with horizon
            None if points are same

    usage : if event.type == pygame.MOUSEMOTION:
                if MOUSE_AIM_REF_POS is None:
                    MOUSE_AIM_REF_POS = pygame.mouse.get_pos()
                else:
                    draw_aim_angle(win, MOUSE_AIM_REF_POS)
            else:
                MOUSE_AIM_REF_POS = None
    """
    del_x, del_y = pos[0] - ref_pos[0], ref_pos[1] - pos[1]
    if del_x == 0:
        if del_y > 0:
            return 1.5707
        if del_y < 0:
            return 4.7123
        return None

    if del_y == 0:
        if del_x > 0:
            return 0
        return 3.141

    if del_x > 0 and del_y > 0:                         # Quadrant 1
        return math.atan(del_y / del_x)
    if del_x < 0 and del_y > 0:                         # Quadrant 2
        return 3.141 - math.atan(del_y / -del_x)
    if del_x < 0 and del_y < 0:                         # Quadrant 3
        return 3.141 + math.atan(del_y / del_x)
    return 6.282 - math.atan(-del_y / del_x)            # Quadrant 4
