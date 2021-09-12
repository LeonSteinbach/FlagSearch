import os
import sys
import pygame
import math
import random
from pygame.locals import *

import flag_search


class Checkbox:
    def __init__(self, x, y, text, color, checked=False):
        self.x = x
        self.y = y
        self.checked = checked
        self.text = text
        self.color = color

        self.size = 10

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def change_state(self):
        global countries
        if self.checked:
            self.checked = False
            if self.text in search_colors:
                search_colors.remove(self.text)
        else:
            self.checked = True
            if self.text not in search_colors:
                search_colors.append(self.text)

        countries = flag_search.get_flags(search_colors)

    def draw(self):
        if not self.checked:
            pygame.draw.lines(screen, self.color, True,
                              [[self.x, self.y],
                               [self.x + self.size, self.y],
                               [self.x + self.size, self.y + self.size],
                               [self.x, self.y + self.size]])
        else:
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.size, self.size])


def update():
    global cam_y
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for checkbox in checkboxes:
                    if checkbox.rect.collidepoint(pygame.mouse.get_pos()):
                        checkbox.change_state()
                        cam_y = 0
                        break

            if event.button == 4:
                if not cam_y + 50 > 0:
                    cam_y += 30
                else:
                    cam_y = 0

            if event.button == 5:
                if not cam_y < -len(countries) * (img_size[1] + gap) - 50 + height:
                    cam_y -= 30
                else:
                    acm_y = -len(countries) * (img_size[1] + gap) + height


def draw():
    screen.fill((255, 255, 255))

    for i, country in enumerate(countries):
        img = pygame.transform.scale(images[country[0]], (img_size[0], img_size[1]))

        screen.blit(Arial.render('#' + str(i+1), False, (0, 0, 0)), (20, i * (img_size[1] + gap) + img_size[1] / 3 + 50 + cam_y))
        screen.blit(Arial.render(str(country[0]), False, (0, 0, 0)), (50, i * (img_size[1] + gap) + img_size[1] / 3 + 50 + cam_y))
        screen.blit(img, (70, i * (img_size[1] + gap) + 50 + cam_y))
        screen.blit(Arial.render(str(country[1]) + ' [%]', False, (0, 0, 0)), (140, i * (img_size[1] + gap) + img_size[1] / 3 + 50 + cam_y))

    pygame.draw.rect(screen, (200, 200, 200), [20, 5, 125, 20])
    for checkbox in checkboxes:
        checkbox.draw()


def main():
    while True:
        update()
        draw()

        pygame.display.flip()
        fpsClock.tick(fps)


if __name__ == '__main__':
    pygame.init()

    fps = 1000
    fpsClock = pygame.time.Clock()

    width, height = 800, 800
    pygame.display.set_caption('Flag search')
    screen = pygame.display.set_mode((width, height))

    images = {}
    img_dir = os.getcwd() + '/images'
    for file in os.listdir(img_dir):
        if file.endswith('.png'):
            images[file[:2]] = pygame.image.load(img_dir + '/' + file).convert_alpha()

    img_size = (60, 40)
    gap = 5

    cam_y = 0

    search_colors = []

    countries = []

    checkboxes = [
            Checkbox(25, 10, 'red', (255, 0, 0)),
            Checkbox(45, 10, 'green', (0, 255, 0)),
            Checkbox(65, 10, 'blue', (0, 0, 255)),
            Checkbox(85, 10, 'yellow', (255, 255, 0)),
            Checkbox(105, 10, 'white', (255, 255, 255)),
            Checkbox(125, 10, 'black', (0, 0, 0))
        ]

    Arial = pygame.font.SysFont('Arial', 10)

    main()
