import pygame, random, numpy, json
import sys

pygame.mixer.init()


def parse(s):
    f = json.load(open(s))
    x = f['layers'][1]['data']
    # pprint(len(x))
    x = numpy.array(x)
    x.resize(f['layers'][1]['height'], f['layers'][1]['width'])
    # pprint(x)
    return list(x)


def step_able(z):
    f0 = int(z.x + z.d) + 1 < len(main_arr[0])
    if not f0:
        return False
    f1 = main_arr[z.y + 1][int(z.x + z.d)] not in [0, 2783] and main_arr[z.y + 1][int(z.x + z.d) + 1] not in [0, 2783]
    f2 = main_arr[z.y][int(z.x + z.d)] in [0] and main_arr[z.y][int(z.x + z.d) + 1] in [0]
    f3 = main_arr[z.y - 1][int(z.x + z.d)] in [0] and main_arr[z.y - 1][int(z.x + z.d) + 1] in [0]
    return f1 and f2 and f3


pygame.init()


def terminate():
    pygame.quit()
    sys.exit();


def startScreen():
    # здесь можно вывести красивую картинку
    # ...

    introText = ["ЗАСТАВКА", "", 'надо засунуть сюда кнопки', 'и картиночку какую-нить']

    screen.fill(pygame.Color('blue'))
    font = pygame.font.Font(None, 30)
    textCoord = 50
    for line in introText:
        stringRendered = font.render(line, 1, pygame.Color('white'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 10
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)


# kek


class Health:
    def __init__(self):
        self.health = 100
        self.x = 30
        self.y = 50
        self.h = 50

    def render(self):

        pygame.draw.rect(screen, pygame.Color('green'), (self.x, self.y, self.health, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (30, 50, 100, 50), 3)

    def damage(self):
        if self.health - 5 >= 0:
            self.health -= 5
            if self.health == 0:
                print('game over')
                sys.exit()


class Gun:
    def __init__(self):
        self.health = 100
        self.x = 160
        self.y = 50
        self.h = 50
        self.reload = True

    def render(self):
        pygame.draw.rect(screen, pygame.Color('blue') if self.reload else pygame.Color('red'),
                         (self.x, self.y, self.health, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (160, 50, 100, 50), 3)

    def damage(self):
        if self.health - 20 >= 0:
            self.health -= 20
            if self.health < 20:
                self.reload = False

    def update(self):
        if self.health + 1 < 101:
            self.health += 1
        else:
            self.reload = True


class Count:
    def __init__(self):
        self.text = '0'
        self.font = pygame.font.SysFont('monospace', 50)

    def render(self):
        x = self.font.render(self.text, True, pygame.Color('red'))
        screen.blit(x, (600, 10))

    def add(self):
        self.text = str(int(self.text) + 1)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.d = random.choice([0.1, -0.1])
        self.moving = 0
        self.z_d_move = {1: 'r', -1: 'l'}
        self.image = pygame.image.load(
            'appear2/appear_{}.png'.format(1))
        self.rect = self.image.get_rect()
        self.rect.x = (self.x - 1) * 32
        self.rect.y = (self.y - 1) * 32 - 16
        self.kk = 0
        self.kk0 = 1
        self.kk2 = 0
        self.stage = -1
        self.damage = True

    def move_cam(self):
        self.moving -= 1
        self.rect.x -= 1

    def move(self):
        if self.stage == -1:
            if 0 <= (self.x - 1) * 32 + self.moving <= 600:
                self.stage += 1

                pygame.mixer.Sound('music/brains%d.wav' % (random.randint(1, 3))).play()

        if self.stage == 0:
            self.kk0 += 1
            if self.kk0 == 12.0:
                self.stage += 1
                # self.y -= 1
                self.rect.y -= 16
                return
            if int(self.kk0) == 12:
                self.stage += 1
                self.rect.y -= 16
                return
            self.image = pygame.image.load(
                'appear2/appear_{}.png'.format(
                    int(self.kk0)))
        elif self.stage == 1:
            self.d *= random.choice([1] * 99 + [-1])

            if self.x + self.d <= 0:
                self.d *= -1
                return
            if step_able(self):
                self.x += self.d

                self.rect.x = self.x * 32 + self.moving
                if self.rect.x < 0 and self.damage:
                    health.damage()
                    self.damage = False
                    self.stage += 1
                if self.rect.x > 0:
                    self.damage = True

                if self.rect.x < -250:
                    all_sprites.remove(self)
                    gui.erase(self)
                    del self

                else:
                    self.kk = (self.kk + 1) % 10 + 1
                    self.image = pygame.image.load(
                        'walk2/go_{}_r.png'.format(self.kk,
                                                   self.z_d_move[
                                                       self.d * 10]))
                    if self.d < 0:
                        self.image = pygame.transform.flip(self.image, True, False)
                    else:
                        pass

            else:
                self.d *= -1
        elif self.stage == 2:
            self.kk2 += 1
            if self.kk2 == 10:
                all_sprites.remove(self)
                gui.erase(self)
                del self
            else:
                self.image = pygame.image.load(
                    'die2/die_{}_r.png'.format(self.kk2,
                                               self.z_d_move[
                                                   self.d * 10]))
                if self.d < 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    pass

    def render(self):
        pass

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(
                event.pos) and self.stage == 1 and gun.reload:
            self.stage = 2
            pygame.mixer.Sound('music/dead_sound%d.wav' % (random.randint(1, 3))).play()
            x, y = self.rect.topleft
            self.rect = pygame.image.load(
                'die2/die_1_r.png').get_rect()
            self.rect.x = x
            self.rect.y = ((self.y + 1) * 32) - self.rect.height
            sch.add()


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render()

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

    def move_cam(self):
        for element in self.elements:
            move_cam = getattr(element, "move_cam", None)
            if callable(move_cam):
                element.move_cam()

    def move(self):
        for element in self.elements:
            move = getattr(element, "move", None)
            if callable(move):
                element.move()

    def erase(self, x):
        for i in range(len(self.elements)):
            if self.elements[i] is x:
                self.elements.pop(i)
                break

    def zero(self):
        for element in self.elements:
            zero = getattr(element, "zero", None)
            if callable(zero):
                element.zero()


class Background:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rep = False

    def move_cam(self):
        if self.x > -(len(main_arr[0]) * 32 - 700):
            self.x -= 1
        elif self.x == -(len(main_arr[0]) * 32 - 700):
            self.rep = True
            self.x -= 1
        elif -(len(main_arr[0]) * 32 - 700) > self.x > -(len(main_arr[0]) * 32):
            self.x -= 1
            self.rep = True
        else:
            self.x += len(main_arr[0]) * 32
            self.rep = False
            gui.zero()

    def render(self):
        screen.blit(self.img, (self.x, self.y))
        if self.rep:
            screen.blit(self.img, (self.x + len(main_arr[0]) * 32, self.y))

    def zero(self):
        self.rep = False
        self.x = 0
        spawn_z(all_sprites)
        print('yay')


def find_up(g):
    ans = len(main_arr[0])
    for i in range(5, len(main_arr[0])):
        if main_arr[i][g] != 0:
            ans = min(ans, i)
            return ans - 1
    return -1


def spawn_z(all_sprites):
    for i in range(10, len(main_arr[0]), 5):
        y = find_up(i)
        gui.add_element(Zombie(i, y, all_sprites))


def find_kekes(d):
    maxy = 0
    miny = len(d)
    for i in range(len(d[0])):
        for j in range(len(d)):
            if d[j][i] != 0:
                maxy = max(maxy, j)
                miny = min(miny, j)

    return miny, maxy


gui = GUI()
health = Health()
gun = Gun()

pp = pygame.image.load('final2.png')
main_arr = parse('final2.json')
# print(main_arr)
# print(gui.elements)
miny, maxy = find_kekes(main_arr)
size = w, h = 700, (maxy * 32 - miny * 32)
bg = Background(0, 0, pp)
sch = Count()
gui.add_element(bg)
gui.add_element(sch)
gui.add_element(health)
gui.add_element(gun)

all_sprites = pygame.sprite.Group()
spawn_z(all_sprites)
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()

cursor = pygame.image.load('aim1.png')
cursor = pygame.transform.scale(cursor, (60, 60))
pygame.mixer.init()
flag = False

background = pygame.Surface(screen.get_size())
background.fill((230, 230, 250))

pygame.mixer.music.set_volume(0.5)
soundtrack = pygame.mixer.music.load('music/soundtrack.mp3')
pygame.mixer.music.play()

startScreen()
while running:
    screen.fill(pygame.Color('white'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gun.reload:
                gun.damage()
                cursor = pygame.transform.scale(cursor, (40, 40))
                snd = pygame.mixer.Sound('music/pistol2.ogg')
                snd.set_volume(0.3)
                snd.play()
            else:
                snd = pygame.mixer.Sound('music/outofammo.ogg')
                snd.set_volume(0.7)
                snd.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            cursor = pygame.image.load('aim1.png')
            cursor = pygame.transform.scale(cursor, (60, 60))
        gui.get_event(event)
        flag = pygame.mouse.get_focused()
        x, y = pygame.mouse.get_pos()

    pygame.mouse.set_visible(False)

    gui.move_cam()
    gui.move()
    gui.render(screen)
    all_sprites.draw(screen)
    if flag:
        c = cursor.get_rect().width
        screen.blit(cursor, (x - c // 2, y - c // 2))
    gui.update()
    pygame.display.flip()
    clock.tick(30)
pygame.mixer.quit()
print('testing')
