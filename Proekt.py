import pygame
import os
import sys
from random import choice

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
# создание групп спрайтов
character_group = pygame.sprite.Group()
all_barriers = pygame.sprite.Group()
presents = pygame.sprite.Group()
one_present = pygame.sprite.Group()
sleigh = pygame.sprite.Group()
all_particle = pygame.sprite.Group()
money_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
spicok = []
screen_rect = (0, 0, 500, 500)
portal = -25
main_character_images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '9a.png', '9b.png', '9c.png']
main_character_images_reverse = ['santa1.png', 'santa2.png', 'santa3.png', 'santa4.png', 'santa5.png', 'santa6.png', 'santa7.png', 'santa8.png',
                                 'santa9.png', 'santa9a.png', 'santa9b.png', 'santa9c.png']
money = ['money1.png', 'money2.png', 'money3.png', 'money4.png', 'money5.png', 'money6.png']


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level):
    new_character, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '&':
                Barrier('cloud', x, y)
            elif level[y][x] == '#':
                Barrier('wall', x, y)
            elif level[y][x] == '@':
                new_character = Main_character(character_group, x, y)
            elif level[y][x] == '.':
                Barrier('box', x, y)
            elif level[y][x] == '$':
                Present(x, y, presents)
            elif level[y][x] == ']':
                Sleigh(x, y)
            elif level[y][x] == ')':
                Money(x, y)
    return new_character, x, y


# функция отображения количества подарков на экране
def draw_amount_presents(amount_presents):
    font = pygame.font.Font(None, 50)
    text = font.render(str(amount_presents), 1, (0, 0, 0))
    text_x = 425
    text_y = 0
    screen.blit(text, (text_x, text_y))


# функция отображения времени на экране
def draw_time(time):
    font = pygame.font.Font(None, 30)
    text = font.render('time: {}'.format(time), 1, (0, 0, 0))
    text_x = 325
    text_y = 0
    screen.blit(text, (text_x, text_y))


def end_screen():
    intro_text = ["GAME OVER!"]

    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            # проверка на выход из игры
            if event.type == pygame.QUIT:
                terminate()
            # проверка на завершение игры
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(fps)


# стартовый экран
def start_screen():
    intro_text = ['']

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            # проверка на выход из игры
            if event.type == pygame.QUIT:
                terminate()
            # проверка на начало игры
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return generate_level(load_level('map_1.txt'))
        pygame.display.flip()
        clock.tick(fps)


# класс дополнительной цели(монеты)
class Money(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(money_group)
        self.n = 0
        self.image = load_image(money[self.n])
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.y = y * 25
        self.rect.x = x * 25

    def update(self, side, amount):
        if amount != 0:
            # смена позиции
            if side == 1:
                self.rect.x -= amount
            else:
                self.rect.x += amount
        else:
            # анимация
            self.n += 1
            self.image = load_image(money[self.n])
            self.image = pygame.transform.scale(self.image, (25, 25))
            if self.n + 1 == len(money):
                self.n = -1

    def invisibility(self):
        self.rect.x = -100
        self.rect.y = 700


class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(portal_group)
        self.n = 0
        self.image = load_image('portal.jpg')
        self.image = pygame.transform.scale(self.image, (25, 50))
        self.rect = self.image.get_rect()
        self.rect.y = 400
        self.y = 400
        self.rect.x = -25
        self.x = -25

    def update(self, side, amount):
        if side == 1:
            self.rect.x -= amount
        else:
            self.rect.x += amount
        self.rect.y = self.y

class Button:
    # создание кнопки
    def create_button(self):
        surface = self.draw_button()
        surface = self.write_text()
        self.rect = pygame.Rect(0, 0, 40, 20)
        return surface

    def write_text(self):
        font_size = 8
        myFont = pygame.font.SysFont("Выход", font_size)
        myText = myFont.render("Выход", 1, (255, 255, 255))
        screen.blit(myText, (20 - round(myText.get_width() / 2), round(10) - round(myText.get_height() / 2)))
        return screen

    def draw_button(self):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 40, 20), width)
        screen.blit(screen, (0, 0))
        return screen

    def pressed(self):
        terminate()


# анимация частиц
class Particle(pygame.sprite.Sprite):
    fire = [load_image("money1.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_particle)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 20

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 10
    numbers = range(-20, 25)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


# класс персонажа
class Main_character(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.n = 0
        self.speed = 5
        self.image = load_image(main_character_images[self.n])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = (y - 1) * 25
        self.rect.x = x * 25
        self.x = x * 25
        self.y = (y - 1) * 25

    def update(self, is_on_land):
        self.n += 1
        self.image = load_image(main_character_images[self.n])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        if self.n + 1 == len(main_character_images):
            self.n = -1

    def update_reverse(self, is_on_land):
        self.n += 1
        self.image = load_image(main_character_images_reverse[self.n])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        if self.n + 1 == len(main_character_images_reverse):
            self.n = -1


class Barrier(pygame.sprite.Sprite):
    def __init__(self, b, x, y):
        super().__init__(all_barriers)
        if b == 'wall':
            self.image = load_image('wall.png')
        elif b == 'cloud':
            self.image = load_image('cloud.png')
        elif b == 'box':
            self.image = load_image('box.jpg')
            spicok.append([x * 25, y * 25])
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x * 25
        self.rect.y = y * 25

    def update(self, side, amount):
        if side == 1:
            self.rect.x -= amount
        else:
            self.rect.x += amount


class Present(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = load_image('present.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.y = y * 25
        self.rect.x = x * 25

    def update(self, side, amount):
        if side == 1:
            self.rect.x -= amount
        else:
            self.rect.x += amount

    def invisibility(self):
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 700


class Sleigh(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(sleigh)
        self.image = load_image('sleigh.jpg')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y = (y - 3) * 25
        self.rect.x = x * 25

    def update(self, side, amount):
        if side == 1:
            self.rect.x -= amount
        else:
            self.rect.x += amount


fps = 60
count = 0
# запуск игры
main_character, level_x, level_y = start_screen()
pygame.mouse.set_visible(False)
button = Button()
character_on_land = True
present = Present(19, 0, one_present)
portal1 = Portal()
pygame.display.flip()
jump_height = 0
level = 1
amount = 10
amount_presents = 0
k = 0
drawing = 0
time = 60
second = 0
side = 1
while True:
    for event in pygame.event.get():
        # проверка на выход из игры
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            # движение вправо
            if event.key == pygame.K_RIGHT:
                side = 1
                drawing = 1
                mods = pygame.key.get_mods()
            # движение влево
            if event.key == pygame.K_LEFT:
                side = 2
                drawing = 1
            # прыжок
            if event.key == pygame.K_UP:
                if character_on_land:
                    character_on_land = False
                    if jump_height == 0:
                        jump_height = 1
            # прыжок
            if event.key == pygame.K_SPACE:
                if character_on_land:
                    character_on_land = False
                    if jump_height == 0:
                        jump_height = 1
        # проверка на прекращение движения
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                drawing = 0
    # анимация ходьбы + движение игрока
    if drawing:
        if side == 1:
            for i in spicok:
                # проверка на пересечение с правой стороны
                if 75 >= i[0] >= 50:
                    if (i[1] - 1) >= main_character.rect.y >= (i[1] - 25):
                        amount = abs(main_character.rect.x + 50 - i[0])
                        break
                    elif main_character.rect.y == (i[1]):
                        amount = abs(main_character.rect.x + 50 - i[0])
                        break
                    else:
                        continue
                else:
                    continue
            all_barriers.update(side, amount)
            presents.update(side, amount)
            sleigh.update(side, amount)
            money_group.update(side, amount)
            portal_group.update(side, amount)
            for i in spicok:
                i[0] -= amount
            portal -= amount
            main_character.update(character_on_land)
        else:
            # проверка на пересечение с левой стороны
            for i in spicok:
                if 0 >= i[0] >= -25:
                    if (i[1] - 1) >= main_character.rect.y >= (i[1] - 25):
                        amount = 0
                        break
                    else:
                        continue
                else:
                    continue
            all_barriers.update(side, amount)
            presents.update(side, amount)
            sleigh.update(side, amount)
            money_group.update(side, amount)
            portal_group.update(side, amount)
            for i in spicok:
                i[0] += amount
            portal += amount
            main_character.update_reverse(character_on_land)
    amount = 10
    z = 0
    # прыжок
    if not character_on_land:
        if jump_height != 0:
            jump_height += 10
            main_character.rect.y -= 10
            main_character.y = main_character.rect.y
            if jump_height >= 21:
                main_character.rect.y -= 5
                main_character.y = main_character.rect.y
                jump_height = 0
                k = 4
        else:
            if k == 0:
                character_on_land = True
                main_character.y = main_character.rect.y
                all_barriers.update(side, 30)
                presents.update(side, 30)
                sleigh.update(side, 30)
                money_group.update(side, 30)
                portal_group.update(side, 30)
                for i in spicok:
                    if side == 1:
                        i[0] -= 30
                    else:
                        i[0] += 30
                if side == 1:
                    portal -= 30
                else:
                    portal += 30
                if side == 1:
                    main_character.update(character_on_land)
                else:
                    main_character.update_reverse(character_on_land)
            else:
                k -= 1
    else:
        while not pygame.sprite.spritecollideany(main_character, all_barriers):
            main_character.rect.y += 1
            main_character.y += 1
            z += 1
            if z >= 3:
                break
            if main_character.rect.y >= 400:
                break
    # проверка на нахождение героя на поле
    if main_character.rect.y > 400:
        main_character.rect.y = 400
    if portal >= 0:
        count += 1
        character_group = pygame.sprite.Group()
        all_barriers = pygame.sprite.Group()
        presents = pygame.sprite.Group()
        one_present = pygame.sprite.Group()
        sleigh = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        money_group = pygame.sprite.Group()
        spicok = []
        portal = -25
        portal1 = Portal()
        time = 60
        if count % 2 == 1:
            main_character, level_x, level_y = generate_level(load_level('map_bonus.txt'))
        else:
            main_character, level_x, level_y = generate_level(load_level('map_1.txt'))
    # проверка на подбор подарка
    if pygame.sprite.spritecollideany(main_character, presents):
        main_character_rect = pygame.Rect(main_character.rect.x, main_character.rect.y, 50, 50)
        for sprite in presents:
            if main_character_rect.colliderect(sprite):
                sprite.invisibility()
                amount_presents += 1
    # проверка на окончание уровня
    if pygame.sprite.spritecollideany(main_character, sleigh):
        character_group = pygame.sprite.Group()
        all_barriers = pygame.sprite.Group()
        presents = pygame.sprite.Group()
        sleigh = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        money_group = pygame.sprite.Group()
        spicok = []
        portal = -25
        portal1 = Portal()
        # переход от первого уровня ко второму
        if level == 1:
            end_screen()
    # проверка на пересечение персонажа с монетой
    if pygame.sprite.spritecollideany(main_character, money_group):
        for sprite in money_group:
            sprite.invisibility()
    # проверка на заканчивание времени
    if time == 0:
        character_group = pygame.sprite.Group()
        all_barriers = pygame.sprite.Group()
        presents = pygame.sprite.Group()
        sleigh = pygame.sprite.Group()
        bonus_group = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        money_group = pygame.sprite.Group()
        spicok = []
        portal = -25
        main_character, level_x, level_y = generate_level(load_level('map_1.txt'))
        amount_presents = 0
        portal1 = Portal()
        time = 60
    second += 1
    if second == 60:
        second = 0
        time -= 1
    # смена кадра
    screen.fill((255, 255, 255))
    all_barriers.draw(screen)
    presents.draw(screen)
    one_present.draw(screen)
    character_group.draw(screen)
    sleigh.draw(screen)
    money_group.draw(screen)
    portal_group.draw(screen)
    money_group.update(side, 0)
    draw_amount_presents(amount_presents)
    draw_time(time)
    pygame.display.flip()
    clock.tick(fps)