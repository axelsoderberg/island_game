import pygame as pg
import math
import collections

pg.init()

game_version = "V0.10"
screen_width = 800
screen_height = 600
font_size = 16

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Island Game")

img_map = pg.image.load("img/map.png")
font = pg.font.SysFont('helvetica', font_size)
font_small = pg.font.SysFont('helvetica', 10)

max_lines = math.floor(160 / (font_size * 1.2))
lines = collections.deque([""] * max_lines)

surface_game_version = font_small.render(game_version, True, pg.Color('black'))


def draw_background():
    screen.fill(pg.Color('black'))
    screen.blit(img_map, (0, 0))
    screen.blit(surface_game_version, (screen_width - 35, 5))


def update():
    pg.display.update()


def draw_text_box():
    pg.draw.rect(screen, (20, 20, 20), (0, screen_height - 200, screen_width, 200))


def draw_input_box(text):
    pg.draw.rect(screen, (40, 40, 40), (5, screen_height - 30, screen_width - 10, 25), border_radius=3)
    text_surface = font.render(text, True, pg.Color('white'))
    screen.blit(text_surface, (10, screen_height - 27))


def draw_text(text):
    draw_text_box()

    text_split = text.splitlines()
    text_split.reverse()
    lines_to_shift = len(text_split)

    lines.rotate(lines_to_shift)

    for i in range(0, lines_to_shift):
        lines[i] = text_split[i]

    old_pos = screen_height - 190
    for row in reversed(list(lines)):
        if row:
            text_surface = font.render(row, True, pg.Color('white'))
            if text_surface.get_width() > screen_width - 20:
                print("Line: " + row + "\nIs too long, add a linebreak")
                exit()
            screen.blit(text_surface, (10, old_pos))
            old_pos += font_size * 1.2
