# Импортируем необходимые библиотеки
import pygame as pg
import random as rd

# Инициализируем часы для управления частотой кадров
clock = pg.time.Clock()
pg.init()

# Устанавливаем размеры окна и создаем окно без рамки
display_width, display_height = 1300, 790
win = pg.display.set_mode((display_width, display_height), flags=pg.NOFRAME)

# Устанавливаем заголовок окна и иконку
pg.display.set_caption('Mario')
pg.display.set_icon(pg.image.load('images/Details/icon.png'))

# Загружаем изображения фона, опыта, снежинок и грибов
bg_image = pg.image.load('images/details/fon.png').convert_alpha()
christmas_tree_image = pg.image.load('images/details/Christmas tree.png').convert_alpha()
menu_image = pg.image.load('images/details/menu.jpg').convert_alpha()
xp_image = pg.image.load('images/details/xp.png').convert_alpha()
snowflake_image = pg.image.load('images/details/snowflake.png').convert_alpha()
snowball_image = pg.image.load('images/details/snowball.png').convert_alpha()
snowball_big_image = pg.image.load('images/details/snowball big.png').convert_alpha()

snowball = []

# Список изображений грибов
mushroom_images = [
    pg.image.load('images/details/mushroom1.png').convert_alpha(),
    pg.image.load('images/details/mushroom2.png').convert_alpha(),
]

# Списки изображений Марио при движении вправо и влево
mario_right = [
    pg.image.load('images/mario/mario1.png').convert_alpha(),
    pg.image.load('images/mario/mario2.png').convert_alpha(),
    pg.image.load('images/mario/mario3.png').convert_alpha(),
    pg.image.load('images/mario/mario4.png').convert_alpha(),
    pg.image.load('images/mario/mario5.png').convert_alpha(),
    pg.image.load('images/mario/mario6.png').convert_alpha(),
    pg.image.load('images/mario/mario7.png').convert_alpha(),
]

mario_left = [
    pg.image.load('images/mario2/mario1.png').convert_alpha(),
    pg.image.load('images/mario2/mario2.png').convert_alpha(),
    pg.image.load('images/mario2/mario3.png').convert_alpha(),
    pg.image.load('images/mario2/mario4.png').convert_alpha(),
    pg.image.load('images/mario2/mario5.png').convert_alpha(),
    pg.image.load('images/mario2/mario6.png').convert_alpha(),
    pg.image.load('images/mario2/mario7.png').convert_alpha(),
]

# Загрузка шрифта и создание текста для паузы
font = pg.font.Font('images/Details/text.ttf', 70)
paused_text = font.render('The game is suspended', True, (0, 32, 255))
time_font = pg.font.Font('images/details/text.ttf', 24)


# Переменные для анимации и движения Марио
anim_count = 0
mario_speed = 10
mario_x, mario_y = 10, 192
mushroom_x, mushroom_y = 200, 201
mushroom_x2, mushroom_y2 = 761, 464
mushroom_x3, mushroom_y3 = 300, 728
jump_count = 6
border_top = 0
border_bottom = 50
mushroom_direction = 1
mushroom_speed = 2
mushroom_frame = 0
animation_speed = 30
star_time = 61
current_time = star_time
fall_start_x = 1210
fall_end_y = 455
snowball_limit = 3

# Текст и цвет для надписи "Game Over"
text = 'game over'
color = (152, 0, 2)
text_x, text_y = 500, 310

# Загрузка звуков
bg_sound = pg.mixer.Sound('sounds/background.mp3')
bg_sound.play(loops=-1)
jump_sound = pg.mixer.Sound('sounds/jump.mp3')
loss_sound = pg.mixer.Sound('sounds/gameover.mp3')
pause_sound = pg.mixer.Sound('sounds/pause.mp3')
button_sound = pg.mixer.Sound('sounds/pause.mp3')
menu_sound = pg.mixer.Sound('sounds/menu.mp3')


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text='', color=(168, 0, 26)):
        # Инициализация параметров кнопки
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self, win):
        # Рисуем кнопку на экране
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        # Если текст не пустой, рисуем его внутри кнопки
        if self.text != '':
            text_surface = font.render(self.text, True, 'green')
            win.blit(text_surface, (
                self.x + (self.width / 2 - text_surface.get_width() / 2),
                self.y + (self.height / 2 - text_surface.get_height() / 2)))

    def is_over(self, pos):
        # Проверяем, находится ли указатель мыши над кнопкой
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


# Функция главного меню
def main_menu():
    global running
    menu_running = True
    start_button = Button(150, 150, 300, 100, 'Start Game')

    while menu_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                menu_running = False
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if start_button.is_over(pos):
                    button_sound.play()
                    menu_running = False

        # Заливаем фон красным цветом
        win.blit(menu_image, (0, 0))

        # Рисуем кнопку старта
        start_button.draw(win)

        # Обновляем дисплей
        pg.display.update()

        # Ограничение частоты кадров
        clock.tick(60)


# Функция для вывода текста на экран
def print_text(message, x, y, font_color=(255, 255, 255), font_type='images/details/text.ttf', font_size=50):
    # Загрузить шрифт и создать текстовый объект
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)

    # Отобразить текст на экране
    win.blit(text, (x, y))


# Функция для отображения текста на поверхности
def draw_text(surface, text, color, x, y):
    # Создать текстовый объект и получить его прямоугольник
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()

    # Установить верхний левый угол прямоугольника текста
    textrect.topleft = (x, y)

    # Отрисовать текст на поверхности
    surface.blit(textobj, textrect)


# Функция для отображения экрана паузы
def draw_paused_win():
    # Отображаем текст "Игра приостановлена" посередине экрана
    win.blit(paused_text, paused_text.get_rect(center=(600, 350)))

    # Обновляем дисплей
    pg.display.flip()


# Класс Снежинки
class Snowflake:
    def __init__(self, x, y, speed):
        # Инициализация параметров снежинки
        self.image = snowflake_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        # Обновление позиции снежинки
        self.rect.y += self.speed

        # Если снежинка выходит за пределы экрана, перемещаем её обратно вверх
        if self.rect.top > display_height:
            self.rect.bottom = 0
            self.rect.centerx = rd.randrange(display_width)


# Создание списка снежинок
snowflakes = [
    Snowflake(rd.randrange(display_width), rd.randrange(-50, display_height), rd.randint(1, 3)) for _ in range(100)
]


def main():
    global snowball_limit


# Флаги состояния игры
game_paused = False
game_over = False
jump = False
running = True

# Запуск главного меню
main_menu()

# Основной цикл игры
while running:

    # Отображение фона
    win.blit(bg_image, (0, 0))

    # Обновление положения снежинок
    for snowflake in snowflakes:
        win.blit(snowflake.image, snowflake.rect)
        snowflake.update()

    win.blit(christmas_tree_image, (1100, 598))

    # Позиции значков опыта
    xp_positions = [(20, 20), (55, 20), (88, 20)]

    # Отображение значков опыта
    for pos in xp_positions:
        win.blit(xp_image, pos)

    # Получение состояний клавиш
    keys = pg.key.get_pressed()

    # Анимация движения Марио влево или вправо
    if keys[pg.K_a]:
        win.blit(mario_left[anim_count], (mario_x, mario_y))
    else:
        win.blit(mario_right[anim_count], (mario_x, mario_y))

    # Движение Марио влево и вправо
    if keys[pg.K_a] and mario_x > 1:
        mario_x -= mario_speed
    elif keys[pg.K_d] and mario_x < 1280:
        mario_x += mario_speed

    # Управление прыжком Марио
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

    # Обновление кадра анимации
    if anim_count == 6:
        anim_count = 0
    elif keys[pg.K_a] or keys[pg.K_d]:
        anim_count += 1

    if snowball:
        for (i, el) in enumerate(snowball):
            win.blit(snowball_image, (el.x, el.y))
            el.x += 4

            if el.x > 1300:
                snowball.pop(i)

    # Выбор текущего изображения гриба
    current_mushroom_image = mushroom_images[mushroom_frame // (animation_speed // len(mushroom_images))]

    # Отображение гриба
    win.blit(current_mushroom_image, (mushroom_x, mushroom_y))
    win.blit(current_mushroom_image, (mushroom_x2, mushroom_y2))
    win.blit(current_mushroom_image, (mushroom_x3, mushroom_y3))

    # Прямоугольники для проверки столкновений
    player_rect = mario_left[0].get_rect(topleft=(mario_x, mario_y))
    mushroom_rect = mushroom_images[0].get_rect(topleft=(mushroom_x, mushroom_y))
    mushroom_rect2 = mushroom_images[0].get_rect(topleft=(mushroom_x2, mushroom_y2))
    mushroom_rect3 = mushroom_images[0].get_rect(topleft=(mushroom_x3, mushroom_y3))

    # Проверка столкновения игрока с грибом
    if player_rect.colliderect(mushroom_rect and mushroom_rect2):
        draw_text(win, text, color, text_x, text_y)
    if player_rect.colliderect(mushroom_rect3):
        draw_text(win, text, color, text_x, text_y)

    mushroom_x += mushroom_speed * mushroom_direction
    mushroom_x2 += mushroom_speed * mushroom_direction
    mushroom_x3 += mushroom_speed * mushroom_direction

    # Изменение направления движения гриба при достижении границ
    if mushroom_x <= 0 or mushroom_x >= 495 - mushroom_images[0].get_width():
        mushroom_direction *= -1
    if mushroom_x2 <= 0 or mushroom_x2 >= 1100 - mushroom_images[0].get_width():
        mushroom_direction *= -1
    if mushroom_x3 <= 0 or mushroom_x3 >= 1300 - mushroom_images[0].get_width():
        mushroom_direction *= -1

    # Обновление текущей картинки гриба
    mushroom_frame += 1
    if mushroom_frame >= animation_speed:
        mushroom_frame = 0

    # Время, прошедшее с последнего обновления
    dt = clock.tick(140) / 100

    # Обновление таймера времени
    current_time -= dt
    if current_time <= 0:
        current_time = 0
    if current_time == 0:
        draw_text(win, text, color, text_x, text_y)

    # Отображение оставшегося времени
    time_text = time_font.render(f'Time: {int(current_time)}', True, 'blue')
    win.blit(time_text, (600, 20))

    # Падение Марио через пропасть
    if mario_x >= fall_start_x:
        mario_y += 15
        if mario_y >= fall_end_y:
            mario_y = fall_end_y

    # Отображение паузы
    if game_paused:
        draw_paused_win()

    # Проверка проигрыша
    if not game_over and player_rect.colliderect(mushroom_rect):
        loss_sound.play()
        draw_text(win, text, color, text_x, text_y)
        game_over = True
    if not game_over and player_rect.colliderect(mushroom_rect2):
        loss_sound.play()
        draw_text(win, text, color, text_x, text_y)
        game_over = True
    if not game_over and player_rect.colliderect(mushroom_rect3):
        loss_sound.play()
        draw_text(win, text, color, text_x, text_y)
        game_over = True

    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pause_sound.play()
                game_paused = not game_paused
            if running and event.key == pg.K_f and snowball_limit > 0:
                snowball.append(snowball_image.get_rect(topleft=(mario_x + 30, mario_y + 10)))
                snowball_limit -= 1

    for i in range(snowball_limit):
        win.blit(snowball_big_image, (170 + i * 35, 26))

    # Ограничение частоты кадров
    clock.tick(15)

    # Обновление дисплея
    pg.display.update()
