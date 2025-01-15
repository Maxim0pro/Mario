import pygame as pg  # импортирую библиотеку pygame
import random as rd

clock = pg.time.Clock()
pg.init()

display_width, display_height = 1300, 790
screen = pg.display.set_mode((display_width, display_height), flags=pg.NOFRAME)

pg.display.set_caption('Mario')
pg.display.set_icon(pg.image.load('Mario/images/Details/icon.png'))

bg_image = pg.image.load('Mario/images/details/fon.png').convert_alpha()
menu_image = pg.image.load('Mario/images/details/menu.jpg').convert_alpha()
snowflake_image = pg.image.load('Mario/images/details/snowflake.png').convert_alpha()
snowball_image = pg.image.load('Mario/images/details/snowball.png').convert_alpha()
snowball_big_image = pg.image.load('Mario/images/details/snowball big.png').convert_alpha()
gift_image = pg.image.load('Mario/images/details/gift.png').convert_alpha()
gift_big_image = pg.image.load('Mario/images/details/gift big.png').convert_alpha()
tower_image = pg.image.load('Mario/images/details/tower.png').convert_alpha()
mushroom_images = [pg.image.load(f'Mario/images/details/mushroom{i}.png').convert_alpha() for i in range(2)]
mario_right_images = [pg.image.load(f'Mario/images/Mario_right/mario{i}.png').convert_alpha() for i in range(7)]
mario_left_images = [pg.image.load(f'Mario/images/mario_left/mario{i}.png').convert_alpha() for i in range(7)]
snowball = []
font = pg.font.Font('Mario/images/details/text.ttf', 70)
paused_text = font.render('The game is suspended', True, (0, 32, 255))
time_font = pg.font.Font('Mario/images/details/text.ttf', 24)

bg_sound = pg.mixer.Sound('Mario/sounds/background.mp3')
bg_sound.play()
jump_sound = pg.mixer.Sound('Mario/sounds/jump.mp3')
loss_sound = pg.mixer.Sound('Mario/sounds/game over.mp3')
pause_sound = pg.mixer.Sound('Mario/sounds/pause.mp3')
button_sound = pg.mixer.Sound('Mario/sounds/pause.mp3')
menu_sound = pg.mixer.Sound('Mario/sounds/menu.mp3')
snot_sound = pg.mixer.Sound('Mario/sounds/shot.mp3')
explosion_sound = pg.mixer.Sound('Mario/sounds/explosion.mp3')
gift_selection_sound = pg.mixer.Sound('Mario/sounds/gift selection.mp3')
victory_sound = pg.mixer.Sound('Mario/sounds/victory.mp3')

anim_count = 0
gift_count = 0
mario_speed = 10
mario_x, mario_y = 10, 192
mario_direction = 1
jump_count = 6
mushroom_x, mushroom_y = 200, 203
mushroom_x2, mushroom_y2 = 761, 466
mushroom_x3, mushroom_y3 = 300, 730
mushroom_direction1 = 1
mushroom_direction2 = 1
mushroom_direction3 = 1
border_top = 0
border_bottom = 50
mushroom_speed = 2
mushroom_frame = 0
animation_speed = 30
star_time = 60
current_time = star_time
win_timer = 0

fall_start_x1 = 1210
fall_end_x1 = 1240
fall_end_y1 = 455
fall_start_x2 = 210
fall_end_x2 = 260
fall_end_y2 = 720
snowball_limit = 3
game_over_timer = 60

text = 'game over'
color = (152, 0, 2)
text_x, text_y = 500, 310
win_font = pg.font.Font('Mario/images/details/text.ttf', 50)
win_text = win_font.render('You Win!', True, (0, 255, 0))
win_text_rect = win_text.get_rect(center=(display_width // 2, display_height // 3))
player_rect = mario_left_images[0].get_rect(topleft=(mario_x, mario_y))
tower_rect = tower_image.get_rect(topleft=(1204, 662))

jump = False
falling = False
falling2 = False
game_win = False
game_over = False
game_paused = False
is_collision = False
playsound = True
show_gift = True
running = True


def print_text(message, x, y, font_color=(255, 255, 255), font_type='Mario/images/details/text.ttf', font_size=50):
    font_type = pg.font.Font(font_type, font_size)
    text_ = font_type.render(message, True, font_color)

    screen.blit(text_, (x, y))


def draw_text(surface, message, local_color, x, y):
    text_obj = font.render(message, 1, local_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)

    surface.blit(text_obj, text_rect)


def draw_paused_win():
    screen.blit(paused_text, paused_text.get_rect(center=(600, 350)))

    pg.display.flip()


class Gift:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)


gifts = [
    Gift(150, 205, gift_image),
    Gift(320, 205, gift_image),
    Gift(550, 205, gift_image),
    Gift(750, 205, gift_image),
    Gift(920, 205, gift_image),
    Gift(1100, 205, gift_image),
    Gift(1270, 205, gift_image),
    Gift(30, 470, gift_image),
    Gift(150, 470, gift_image),
    Gift(400, 470, gift_image),
    Gift(600, 470, gift_image),
    Gift(750, 470, gift_image),
    Gift(950, 470, gift_image),
    Gift(1150, 470, gift_image),
    Gift(50, 732, gift_image),
    Gift(200, 732, gift_image),
    Gift(400, 732, gift_image),
    Gift(600, 732, gift_image),
    Gift(800, 732, gift_image),
    Gift(950, 732, gift_image)
]


class Button:
    def __init__(self, x, y, width, height, local_text='', normal_color=(168, 0, 26), hover_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = local_text
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.current_color = self.normal_color

    def draw(self, win):
        pg.draw.rect(win, (168, 0, 26), (self.x, self.y, self.width, self.height))

        if self.text != '':
            text_surface = font.render(self.text, True, self.current_color)
            win.blit(text_surface, (
                self.x + (self.width / 2 - text_surface.get_width() / 2),
                self.y + (self.height / 2 - text_surface.get_height() / 2)))

    def is_over(self, pos_pro):
        return self.x < pos_pro[0] < self.x + self.width and self.y < pos_pro[1] < self.y + self.height


def main_menu():
    global running
    menu_running = True
    start_button = Button(150, 150, 300, 100, 'Start Game', normal_color=(0, 204, 102), hover_color=(0, 255, 0))
    quit_button = Button(150, 250, 300, 200, 'Quit Game', normal_color=(0, 204, 102), hover_color=(0, 255, 0))
    menu_sound.play(loops=-1)

    while menu_running:
        for current_event in pg.event.get():
            if current_event.type == pg.QUIT:
                menu_running = False
                running = False
            if current_event.type == pg.MOUSEBUTTONDOWN:
                posing = pg.mouse.get_pos()
                if start_button.is_over(posing):
                    button_sound.play()
                    menu_running = False
                    menu_sound.stop()
                    pg.time.delay(800)
                if quit_button.is_over(posing):
                    button_sound.play()
                    menu_running = False
                    menu_sound.stop()
                    pg.time.delay(800)
                    pg.quit()

        screen.blit(menu_image, (0, 0))
        mouse_pos = pg.mouse.get_pos()

        if start_button.is_over(mouse_pos):
            start_button.current_color = start_button.hover_color
        else:
            start_button.current_color = start_button.normal_color

        if quit_button.is_over(mouse_pos):
            quit_button.current_color = quit_button.hover_color
        else:
            quit_button.current_color = quit_button.normal_color

        start_button.draw(screen)
        quit_button.draw(screen)
        pg.display.update()
        clock.tick(60)


class Snowflake:
    def __init__(self, x, y, speed):
        self.image = snowflake_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > display_height:
            self.rect.bottom = 0
            self.rect.centerx = rd.randrange(display_width)


snowflakes = [
    Snowflake(rd.randrange(display_width), rd.randrange(-50, display_height), rd.randint(1, 3)) for _ in range(50)]


def main():
    global snowball_limit


if bg_sound.get_num_channels() > 0:
    bg_sound.stop()

main_menu()
bg_sound.play()


class Snowball:
    def __init__(self, x, y, direction):
        self.image = snowball_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction

    def update(self):
        self.rect.x += 10 * self.direction

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def handle_collisions(local_player_rect, local_mushroom_rect, local_mushroom_rect2, local_mushroom_rect3):
    global game_over, snowball

    for snowball_ball in list(snowball):
        if snowball_ball.rect.colliderect(local_mushroom_rect):
            explosion_sound.play()
            snowball.remove(snowball_ball)
            global mushroom_x
            mushroom_x = -10000
        if snowball_ball.rect.colliderect(local_mushroom_rect2):
            explosion_sound.play()
            snowball.remove(snowball_ball)
            global mushroom_x2
            mushroom_x2 = -10000
        if snowball_ball.rect.colliderect(local_mushroom_rect3):
            explosion_sound.play()
            snowball.remove(snowball_ball)
            global mushroom_x3
            mushroom_x3 = -10000

    if not game_over and local_player_rect.colliderect(local_mushroom_rect):
        bg_sound.stop()
        loss_sound.play()
        draw_text(screen, text, color, text_x, text_y)
        game_over = True
    if not game_over and local_player_rect.colliderect(local_mushroom_rect2):
        bg_sound.stop()
        loss_sound.play()
        draw_text(screen, text, color, text_x, text_y)
        game_over = True
    if not game_over and local_player_rect.colliderect(local_mushroom_rect3):
        bg_sound.stop()
        loss_sound.play()
        draw_text(screen, text, color, text_x, text_y)
        game_over = True


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pause_sound.play()
                game_paused = not game_paused
            if running and event.key == pg.K_f and snowball_limit > 0:
                snot_sound.play()
                if mario_direction == 1:
                    snowball.append(Snowball(mario_x + 30, mario_y + 10, mario_direction))
                    snowball_limit -= 1
                elif mario_direction == -1:
                    snowball.append(Snowball(mario_x - 15, mario_y + 10, mario_direction))
                    snowball_limit -= 1

    keys = pg.key.get_pressed()

    if game_paused:
        draw_paused_win()
        if bg_sound.get_num_channels() > 0:
            bg_sound.stop()
    else:
        if bg_sound.get_num_channels() == 0 and not game_over:
            bg_sound.play(loops=-1)

    if game_win:
        screen.fill((39, 81, 31))
        screen.blit(win_text, win_text_rect)
        score_text = win_font.render(f'Gifts: {gift_count}', True, (128, 128, 128))
        score_rect = score_text.get_rect(center=(650, 360))
        screen.blit(score_text, score_rect)

        time_text = win_font.render(f'Time: {int(star_time - current_time)}', True, (128, 128, 128))
        time_rect = time_text.get_rect(center=(650, 450))
        screen.blit(time_text, time_rect)

        if win_timer > 0:
            win_timer -= 1
        else:
            running = False

    if not game_paused and not game_over and not game_win:

        screen.blit(bg_image, (0, 0))

        for snowflake in snowflakes:
            screen.blit(snowflake.image, snowflake.rect)
            snowflake.update()

        for i in range(snowball_limit):
            screen.blit(snowball_big_image, (150 + i * 35, 26))

        for gift in gifts:
            gift.draw(screen)

        screen.blit(gift_big_image, (30, 28))
        screen.blit(tower_image, (1204, 662))

        for gift in list(gifts):
            if not gift.collected and player_rect.colliderect(gift.rect):
                gift.collected = True
                gift_count += 1
                gift_selection_sound.play()
                gifts.remove(gift)

        if keys[pg.K_a] and mario_x > 1:
            mario_x -= mario_speed
        elif keys[pg.K_d] and mario_x < 1280:
            mario_x += mario_speed

        if mario_direction == -1:
            screen.blit(mario_left_images[anim_count], (mario_x, mario_y))
        else:
            screen.blit(mario_right_images[anim_count], (mario_x, mario_y))

        if keys[pg.K_a]:
            mario_direction = -1
        elif keys[pg.K_d]:
            mario_direction = 1

        if not jump:
            if keys[pg.K_SPACE]:
                jump = True
                jump_sound.play()
        else:
            if jump_count >= -6:
                if jump_count > 0:
                    mario_y -= (jump_count ** 2) / 2
                else:
                    mario_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                jump = False
                jump_count = 6

        if anim_count == 6:
            anim_count = 0
        elif keys[pg.K_a] or keys[pg.K_d]:
            anim_count += 1

        if fall_start_x1 <= mario_x <= fall_end_x1:
            if mario_y == 192:
                falling = True
        if mario_y < fall_end_y1 and falling:
            mario_y += 15
        elif mario_y > 455 and falling:
            falling = False
            mario_y = fall_end_y1

        if fall_start_x2 <= mario_x <= fall_end_x2:
            if mario_y == 455:
                falling2 = True
        if mario_y < fall_end_y2 and falling2:
            mario_y += 15
        elif mario_y > fall_end_y2 and falling2:
            falling2 = False
            mario_y = fall_end_y2

        if snowball:
            for snowball_item in list(snowball):
                screen.blit(snowball_item.image, snowball_item.rect)
                snowball_item.update()
                if snowball_item.rect.x > 1300:
                    snowball.remove(snowball_item)
                if snowball_item.rect.x < 0:
                    snowball.remove(snowball_item)

        current_mushroom_image = mushroom_images[mushroom_frame // (animation_speed // len(mushroom_images))]

        screen.blit(current_mushroom_image, (mushroom_x, mushroom_y))
        screen.blit(current_mushroom_image, (mushroom_x2, mushroom_y2))
        screen.blit(current_mushroom_image, (mushroom_x3, mushroom_y3))

        player_rect = mario_left_images[0].get_rect(topleft=(mario_x, mario_y))
        player_rect2 = mario_right_images[0].get_rect(topleft=(mario_x, mario_y))
        mushroom_rect = mushroom_images[0].get_rect(topleft=(mushroom_x, mushroom_y))
        mushroom_rect2 = mushroom_images[0].get_rect(topleft=(mushroom_x2, mushroom_y2))
        mushroom_rect3 = mushroom_images[0].get_rect(topleft=(mushroom_x3, mushroom_y3))
        handle_collisions(player_rect, mushroom_rect, mushroom_rect2, mushroom_rect3)

        if player_rect.colliderect(tower_rect):
            game_win = True
            if bg_sound.get_num_channels() > 0:
                bg_sound.stop()
            victory_sound.play()
            win_timer = 10 * 15

        mushroom_x += mushroom_speed * mushroom_direction1
        mushroom_x2 += mushroom_speed * mushroom_direction2
        mushroom_x3 += mushroom_speed * mushroom_direction3

        if mushroom_x <= 0 or mushroom_x >= 1210 - mushroom_images[0].get_width():
            mushroom_direction1 *= -1
        if mushroom_x2 <= 260 or mushroom_x2 >= 1300 - mushroom_images[0].get_width():
            mushroom_direction2 *= -1
        if mushroom_x3 <= 120 or mushroom_x3 >= 1000 - mushroom_images[0].get_width():
            mushroom_direction3 *= -1

        mushroom_frame += 1
        if mushroom_frame >= animation_speed:
            mushroom_frame = 0

        dt = clock.tick(140) / 100

        current_time -= dt
        if current_time <= 0:
            current_time = 0
        if current_time == 0:
            draw_text(screen, text, color, text_x, text_y)
            bg_sound.stop()
            loss_sound.play()
            game_over = True

        time_text = time_font.render(f'Time: {int(current_time)}', True, 'blue')
        screen.blit(time_text, (600, 20))

        print_text(f" {gift_count}", 75, 28, 'green', font_size=30)

        if not game_over and player_rect.colliderect(mushroom_rect):
            bg_sound.stop()
            loss_sound.play()
            draw_text(screen, text, color, text_x, text_y)
            game_over = True
        if not game_over and player_rect.colliderect(mushroom_rect2):
            bg_sound.stop()
            loss_sound.play()
            draw_text(screen, text, color, text_x, text_y)
            game_over = True
        if not game_over and player_rect.colliderect(mushroom_rect3):
            bg_sound.stop()
            loss_sound.play()
            draw_text(screen, text, color, text_x, text_y)
            game_over = True

    if game_over:
        if game_over_timer > 0:
            game_over_timer -= 1
        else:
            running = False

    clock.tick(15)
    pg.display.update()

if __name__ == '__main__':
    main()
