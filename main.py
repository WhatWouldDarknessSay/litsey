import json
import sys
import time
import math
import pygame
import threading
import random
# variables
score = 0
level_k = 1
menu_flag = True
new_level_flag = False
stop_flag = False
mainloop_stop_flag = False
ans_flag = False
# main pygame stuff
pygame.init()
screen = pygame.display.set_mode((300, 500))
pygame.display.set_caption("TouchColor on PyGame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 30)
#load data
with open('data.json') as file:
    data = json.load(file)
    personal_best = data["Personal Best"]
# background
background = pygame.image.load('media/touchcolorbg.png')
background = pygame.transform.scale(background, (300, 500))
# text
menu_personal_best_surface = pygame.font.SysFont("Calibri", 20).render('Personal Best: ' + str(personal_best), True, (157, 0, 255))
menu_logo_surface = pygame.transform.scale(pygame.image.load('media/TouchColorText.png'), (200, 30))
personal_best_text_surface = pygame.font.SysFont("Calibri", 20).render('PB: ' + str(personal_best), True, (157, 0, 255))
score_text_surface = font.render(str(score), True, (0, 0, 0))
level_text_surface = pygame.font.SysFont("Calibri", 40).render('Level ' + str(score // 10 + 1), True, (0, 0, 0))

def score_update(): # renders scores for pb and current
    global score_text_surface, personal_best_text_surface, score, personal_best
    score_text_surface = font.render(str(score), True, (0, 0, 0))
    if score > personal_best:
        personal_best = score
    personal_best_text_surface = pygame.font.SysFont("Calibri", 20).render('PB: ' + str(personal_best), True, (157, 0, 255))


# main program


class SimpleRect: # just rectangles
    def __init__(self, pos, size, color):
        self.x, self.y = pos
        self.i = 0
        self.size = size
        self.color = color
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def change_color(self, color): # animation of changing color
        global new_level_flag
        self.color = color
        self.i = 0
        tmp = -3.14
        while tmp <= 3.14:
            self.i = (math.cos(tmp) + 1) * 5
            self.surface = pygame.Surface((self.size[0] + self.i * 2, self.size[1] + self.i * 2))
            self.surface.fill(self.color)
            if new_level_flag:
                break
            game_show()
            try: # for case when app is closed, but function is still running
                pygame.display.update()
            except:
                exit()
            tmp += 0.01 / level_k
        self.i = 0
        if not new_level_flag:
            game_show()
            pygame.display.update()

    def show(self):
        screen.blit(self.surface, (self.x - self.i, self.y - self.i))
        pygame.display.update()


class Button:
    def __init__(self, pos, size, color, type='game', text='', image='', text_color='pink', alpha=255):
        self.type = type
        # position, size
        self.i = 0
        self.x, self.y = pos
        self.size = size
        # color
        self.color = color
        self.text_color = text_color
        self.alpha = alpha
        self.image_flag = False
        if image != '':
            self.image_flag = True
            self.image = pygame.transform.scale(pygame.image.load(image), self.size)
        # rendering surfaces
        self.text_flag = False
        if text != '':
            self.text_flag = True
            self.text = pygame.font.SysFont("Calibri", 20).render(text, True, self.text_color)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.surface.set_alpha(self.alpha)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        screen.blit(self.surface, (self.x + self.i, self.y + self.i))
        if self.image_flag:
            screen.blit(self.image, (self.x, self.y))
        if self.text_flag:
            screen.blit(self.text, (self.x + (self.surface.get_width() - self.text.get_width()) // 2, self.y + (self.surface.get_height() - self.text.get_height()) // 2))


    def to_menu_button_action(self):
        global menu_flag
        menu_personal_best_surface = pygame.font.SysFont("Calibri", 20).render(
            'Personal Best: ' + str(personal_best), True, (157, 0, 255))
        menu_flag = True

    def menu_button_action(self): # action function for buttons of 'menu' type
        global menu_flag
        menu_flag = False
        starttimer()

    def game_button_action(self):  # when button is pressed(for buttons of 'game' type)
        t = threading.Thread(target=lambda: answ(self.color))
        t.start()
        self.i = 0
        tmp = -3.14
        while tmp <= 3.14 and not new_level_flag:
            self.i = (math.cos(tmp) + 1) * 3
            self.surface = pygame.Surface((self.size[0] - self.i * 2, self.size[1] - self.i * 2))
            self.surface.fill(self.color)
            if not new_level_flag:
                game_show()
                pygame.display.update()
            tmp += 0.01
        self.surface = pygame.Surface((self.size[0], self.size[1]))
        self.surface.fill(self.color)
        self.i = 0
        if not new_level_flag:
            game_show()
            pygame.display.update()

    def click(self, event): # detection of clicking and later instructions
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.rect.collidepoint(x, y):
                    if not new_level_flag:
                        if self.type == 'menu': # starting different functions for different types of buttons
                            self.menu_button_action()
                        elif self.type == 'to_menu':
                            self.to_menu_button_action()
                        elif self.type == 'game':
                            self.game_button_action()




def new_level(): # function of changing a level
    global score, level_text_surface, personal_best_text_surface, new_level_flag, level_k
    level_k = level_k / 1.1
    screen.blit(background, (0, 0))
    level_text_surface = pygame.font.SysFont("Calibri", 40).render('Level ' + str(score // 10 + 1), True, (0, 0, 0, 0))
    new_level_show()
    screen.blit(level_text_surface, (150 - level_text_surface.get_size()[0] // 2 - 1, 150 - level_text_surface.get_size()[1] // 2))
    pygame.display.update()
    new_level_show()
    for _ in range(24):
        pygame.display.update()
        level_text_surface.set_alpha(_ * 10)
        new_level_show()
        pygame.display.update()
        time.sleep(0.03125)
    time.sleep(0.75)
    for _ in range(24):
        pygame.display.update()
        level_text_surface.set_alpha((12 - _) * 10)
        new_level_show()
        pygame.display.update()
        time.sleep(0.03125)

    new_level_flag = False

def answ(color): # when user is answering by pressing a button
    global score, stop_flag, ans_flag, new_level_flag, score_text_surface, level_k
    present_color = ShowColor.color
    if color == present_color and not ans_flag:
        score += 1
        score_update()
    elif not ans_flag:
        score = 0
        level_k = 1
        score_update()
    if score != 0 and score % 10 == 0:
        new_level_flag = True
    ans_flag = True
    stop_flag = True


def starttimer():
    global stop_flag, ans_flag, menu_flag
    if menu_flag:
        exit()
    prev_cl = ShowColor.color
    t = threading.Thread(target=lambda: ShowColor.change_color(random.choice([_ for _ in ['red', 'blue', 'purple', 'yellow', 'green', (0, 255, 255)] if _ != prev_cl])))
    t.start()
    timer1sec = threading.Thread(target=wait1sec)
    stop_flag = False
    ans_flag = False
    timer1sec.start()


def wait1sec():
    global stop_flag, new_level_flag, level_k
    if stop_flag:
        sys.exit(0)
    time.sleep(level_k)
    if mainloop_stop_flag or menu_flag:
        exit(0)
    elif new_level_flag:
        new_level()
    starttimer()
    sys.exit(0)


def mainloop():
    global mainloop_stop_flag, menu_flag
    if not menu_flag:
        starttimer()
    while True:
        clock.tick(144)
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop_stop_flag = True
                with open('data.json', 'w') as file:
                    data['Personal Best'] = personal_best
                    json.dump(data, file)
                pygame.quit()
                exit(0)
            if not menu_flag:
                all_button_click(event)
            else:
                MenuStartButton.click(event)
        if menu_flag:
            screen.blit(menu_personal_best_surface, menu_personal_best_surface.get_rect(center=(300/2, 150)))
            screen.blit(menu_logo_surface, (50, 50))
            MenuStartButton.show()
            pygame.display.flip()
        if not new_level_flag and not menu_flag:
            game_show()
            pygame.display.flip()


def all_button_click(event):
    RedButton.click(event)
    GreenButton.click(event)
    PurpleButton.click(event)
    LightBlueButton.click(event)
    YellowButton.click(event)
    BlueButton.click(event)
    GameButtonToMenu.click(event)


def game_show():
    screen.blit(background, (0, 0))
    screen.blit(score_text_surface, (150 - score_text_surface.get_size()[0] // 2 - 1, 30))
    screen.blit(personal_best_text_surface, (0, 0))
    GameButtonToMenu.show()
    RedButton.show()
    GreenButton.show()
    PurpleButton.show()
    LightBlueButton.show()
    YellowButton.show()
    BlueButton.show()
    ShowColor.show()


def new_level_show():
    screen.blit(background, (0, 0))
    screen.blit(level_text_surface, (150 - level_text_surface.get_size()[0] // 2 - 1, 200 - level_text_surface.get_size()[1] // 2))
    screen.blit(personal_best_text_surface, (0, 0))

# interface blocks(buttons, rects, etc.)

MenuStartButton = Button(
    (50, 200),
    (200, 50),
    (0, 255, 255),
    type='menu',
    alpha=0,
    image='media/TCFinalButton.png'
)
GameButtonToMenu = Button(
    (250, 0),
    (50, 20),
    (0, 0, 0),
    type='to_menu',
    text='menu',
    text_color='purple',
    alpha=0
)
RedButton = Button(
    (0, 300),
    (100, 100),
    'red',
    type='game'
)
GreenButton = Button(
    (0, 400),
    (100, 100),
    'green',
    type='game'
)
PurpleButton = Button(
    (100, 300),
    (100, 100),
    'purple',
    type='game'
)
LightBlueButton = Button(
    (100, 400),
    (100, 100),
    (0, 255, 255),
    type='game'
)
YellowButton = Button(
    (200, 300),
    (100, 100),
    'yellow',
    type='game'
)
BlueButton = Button(
    (200, 400),
    (100, 100),
    'blue',
    type='game'
)
ShowColor = SimpleRect(
    (100, 100),
    (100, 100),
    'blue',
)
mainloop()
