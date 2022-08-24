import sys
import os
# import shutil
import random
from PIL import Image, ImageDraw
import pygame as pg
import time

from A_star_search import solve, print_solution
from colors import color_text

MAX_NEW_FIRES = 3
STEPS = 10
SQUARE_SIZE = 40
TILE_SIZE = 25
MAX_WIDTH = 1280
MAX_HEIGHT = 648
START = (255, 0, 255)
GOAL = (0, 0, 255)
WALL = (96, 96, 96)
CLEAR = (255, 255, 255)
PATH = (0, 204, 0)
BLACK = (0, 0, 0)


def main():
    os.system('color')
    if len(sys.argv) != 2:
        print("Usage: python main.py layout")
        return

    # route_dir = os.getcwd() + os.sep + "route"
    # if os.path.exists(route_dir):
    #     shutil.rmtree(route_dir)
    # os.mkdir(route_dir)

    layout, sensors, start, goals = get_layout(sys.argv[1])
    new_fires = start_fire(layout, sensors, 1)
    fires = [new_fires]

    try:
        path = solve(layout, start, goals)[:STEPS]
        # print_step(layout, path, start, goals, f"{route_dir}{os.sep}step0.png")
    except:
        print(color_text("NO WAY OUT", color="red"))
        generate_animation(layout, len(layout), len(layout[0]), [start], start, goals, fires, True)
        return

    # i = 1
    while path[-1] not in goals:
        new_fires = start_fire(layout, sensors, random.randint(0, MAX_NEW_FIRES))
        fires.append(new_fires)
        temp_start = path[-1]
        try:
            temp_path = solve(layout, temp_start, goals)[:STEPS]
            path.extend(temp_path)
            # print_step(layout, temp_path, start, goals, f"{route_dir}{os.sep}step{i}.png")
            # i += 1
        except:
            # print_solution(layout, path, start, goals)
            print(color_text("NO WAY OUT", color="red"))
            generate_animation(layout, len(layout), len(layout[0]), path, start, goals, fires, True)
            return

    # print_step(layout, path, start, goals, f"{route_dir}{os.sep}final.png")
    generate_animation(layout, len(layout), len(layout[0]), path, start, goals, fires)
    # generate_image(layout, len(layout), len(layout[0]), path, start, goals, "route.png")


def get_layout(file):
    layout = []
    sensors = []
    goals = []
    with open(file, "r") as f:
        for row in f:
            row = row.strip()
            temp = [1 if ch == "#" else 0 for ch in row]
            layout.append(temp)
            if "A" in row:
                start = (layout.index(temp), row.index("A"))
            while "B" in row:
                goals.append((layout.index(temp), row.index("B")))
                row = row.replace("B", "_", 1)
            while "^" in row:
                sensors.append((layout.index(temp), row.index("^")))
                row = row.replace("^", "_", 1)
    return layout, sensors, start, goals


def start_fire(layout, sensors, count):
    fire_count = min(count, len(sensors))
    fires = []
    for i in range(fire_count):
        line, col = random.choice(sensors)
        layout[line][col] = random.random()
        fires.append(((line, col), layout[line][col]))
    return fires


def print_step(layout, path, start, goals, file):
    print_solution(layout, path, start, goals)
    generate_image(layout, len(layout), len(layout[0]), path, start, goals, file)


def generate_image(layout, height, width, path, start, goals, file):
    file = "route" + os.sep + file
    img = Image.new("RGB", (SQUARE_SIZE * width, SQUARE_SIZE * height))
    pixdata = img.load()
    draw = ImageDraw.Draw(img)
    for i in range(height):
        for j in range(width):
            msg, fire = "", ""
            if (i, j) == start:
                color = START
                msg = "START"
            elif (i, j) in goals:
                color = GOAL if (i, j) not in path else PATH
                msg = "EXIT"
            elif (i, j) in path:
                color = PATH
            elif layout[i][j] == 1:
                color = WALL
            elif 0.1 <= layout[i][j] < 0.3:
                fire = "icons" + os.sep + "light_fire.png"
            elif 0.3 <= layout[i][j] < 0.6:
                fire = "icons" + os.sep + "medium_fire.png"
            elif 0.6 <= layout[i][j] < 1:
                fire = "icons" + os.sep + "heavy_fire.png"
            else:
                color = CLEAR

            if len(fire):
                fire_img = Image.open(fire)
                img.paste(fire_img, (j * SQUARE_SIZE, i * SQUARE_SIZE))
            else:
                for x in range(SQUARE_SIZE):
                    for y in range(SQUARE_SIZE):
                        pixdata[y + j * SQUARE_SIZE, x + i * SQUARE_SIZE] = color
                w, h = draw.textsize(msg)
                draw.text((j * SQUARE_SIZE + (SQUARE_SIZE - w) / 2, i * SQUARE_SIZE + (SQUARE_SIZE - h) / 2), msg,
                          fill=(0, 0, 0))

    img.save(file, "PNG")


def generate_animation(layout, layout_h, layout_w, path, start, goals, fires, stuck=False):
    # Snap to top left corner
    # os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

    pg.init()

    width = min(layout_w * TILE_SIZE, MAX_WIDTH)
    height = min(layout_h * TILE_SIZE, MAX_HEIGHT)
    tile_w = width // layout_w
    tile_h = height // layout_h
    path_copy = path.copy()
    n = len(path)

    screen = pg.display.set_mode((width, height), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
    pg.display.set_caption("press SPACE to begin")
    clock = pg.time.Clock()

    def draw(cell, color):
        rect = pg.Rect((cell[1] * tile_w, cell[0] * tile_h), (tile_w, tile_h))
        pg.draw.rect(screen, color, rect)

    def write(cell, text, size):
        font = pg.font.Font('freesansbold.ttf', size)
        txt = font.render(text, True, BLACK)
        text_rect = txt.get_rect(center=(cell[1] * tile_w + tile_w // 2, cell[0] * tile_h + tile_h // 2))
        screen.blit(txt, text_rect)

    def draw_board():
        for i in range(layout_h):
            for j in range(layout_w):
                if (i, j) == start:
                    draw((i, j), START)
                    write((i, j), 'start', 11)
                elif (i, j) in goals:
                    draw((i, j), GOAL)
                    write((i, j), 'exit', 12)
                elif layout[i][j] < 1:
                    draw((i, j), CLEAR)

    def draw_path():
        if len(path_copy) == 1 and stuck:
            skull_img = pg.image.load(f"icons{os.sep}skull.png").convert_alpha()
            skull_img = pg.transform.scale(skull_img, (tile_w, tile_h))
            img_rect = skull_img.get_rect(
                center=(path_copy[0][1] * tile_w + tile_w // 2, path_copy[0][0] * tile_h + tile_h // 2))
            screen.blit(skull_img, img_rect)
            time.sleep(0.25)
        elif len(path_copy):
            draw(path_copy[0], PATH)
            path_copy.pop(0)
            time.sleep(0.25)
        elif len(path_copy) == 0:
            for cell in path:
                draw(cell, PATH)
            write(path[-1], 'exit', 12)

    def draw_fires():
        light_fire = pg.transform.scale(light_fire_img, (tile_w, tile_h))
        medium_fire = pg.transform.scale(medium_fire_img, (tile_w, tile_h))
        heavy_fire = pg.transform.scale(heavy_fire_img, (tile_w, tile_h))

        x = (n - len(path_copy) + stuck) // 10
        if x >= len(fires):
            return
        for k in range(x + 1):
            for fire in fires[k]:
                i, j = fire[0]
                intensity = fire[1]
                if 0.1 <= intensity < 0.3:
                    img_rect = light_fire.get_rect(
                        center=(j * tile_w + tile_w // 2, i * tile_h + tile_h // 2))
                    screen.blit(light_fire, img_rect)
                elif 0.3 <= intensity < 0.6:
                    img_rect = medium_fire.get_rect(
                        center=(j * tile_w + tile_w // 2, i * tile_h + tile_h // 2))
                    screen.blit(medium_fire, img_rect)
                elif 0.6 <= intensity < 1:
                    img_rect = heavy_fire.get_rect(
                        center=(j * tile_w + tile_w // 2, i * tile_h + tile_h // 2))
                    screen.blit(heavy_fire, img_rect)

    light_fire_img = pg.image.load(f"icons{os.sep}light_fire.png").convert_alpha()
    medium_fire_img = pg.image.load(f"icons{os.sep}medium_fire.png").convert_alpha()
    heavy_fire_img = pg.image.load(f"icons{os.sep}heavy_fire.png").convert_alpha()

    go = False
    running = True
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                width = event.w
                height = event.h
                tile_w = width // layout_w
                tile_h = height // layout_h
                screen = pg.display.set_mode((width, height), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    go = True
                    pg.display.set_caption("press R to view again" if not stuck else "NO WAY OUT")
                elif event.key == pg.K_r:
                    path_copy = path.copy()
        screen.fill(WALL)
        draw_board()
        if go:
            draw_fires()
            draw_path()
        pg.display.flip()


if __name__ == "__main__":
    main()
