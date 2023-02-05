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
