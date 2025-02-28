import sys

import pygame
import os

FPS = 50
pygame.init()
pygame.display.set_caption('Игра "Яндекс доставка"')
pygame.key.set_repeat(200, 70)
size = width, height = WIDTH, HEIGHT = 500, 1000
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
left_right = 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    size = width, height = WIDTH, HEIGHT = 1000, 1000
    screen = pygame.display.set_mode(size)
    intro_text = ["Вправо или влево чтобы управлять", "Нажмите чтобы начать"]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('Fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
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
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('barrier.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('player.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            self.add(wall_group)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 5)
        self.start_coords = [tile_width * pos_x, tile_height * pos_y + 5]

    def mover(self, tx):

        rect = self.rect
        self.rect = self.rect.move(0, tx)

        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect = rect
            return False
        return True

    def update(self, *args):
        global left_right
        if args:
            key = args[0].key
            rect = self.rect
            if key == pygame.K_RIGHT or key == pygame.K_d:
                self.rect = self.rect.move(tile_width, 0)
                if left_right == 1:
                    pass
                else:
                    self.image = pygame.transform.flip(self.image, True, False)
                    screen.blit(self.image, ((500 - 50) // 2, (1000 - 50) // 2))
                    pygame.display.flip()
                    left_right = 1
            elif key == pygame.K_LEFT or key == pygame.K_a:
                self.rect = self.rect.move(-tile_width, 0)
                if left_right == 0:
                    pass
                else:
                    self.image = pygame.transform.flip(self.image, True, False)
                    screen.blit(self.image, ((500 - 50) // 2, (1000 - 50) // 2))
                    pygame.display.flip()
                    left_right = 0

            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect = rect


class Camera:

    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.y > height:
            obj.rect.y -= height
        elif obj.rect.y < 0:
            obj.rect.y += height
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)

                new_player = Player(x, y)

    return new_player, x, y


def end_screen(score):
    size = width, height = WIDTH, HEIGHT = 1000, 1000
    screen = pygame.display.set_mode(size)
    with open("score.txt", "r") as f:
        best_score = int(f.read())
        if score > best_score:
            best_score = score
            with open("score.txt", 'w') as file:
                pass
                file.write(str(best_score))

    intro_text = ["Конец игры", f"Ваш счёт: {score}", f"Рекорд {best_score}"]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('Fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 65)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()

        intro_rect.top = text_coord
        intro_rect.x += 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:

                return True
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    pygame.key.set_repeat(200, 70)
    size = width, height = WIDTH, HEIGHT = 500, 1000
    screen = pygame.display.set_mode(size)
    player, level_x, level_y = generate_level(load_level('level_1.txt'))
    pygame.mixer.music.load("data/backtrack.mp3")
    pygame.mixer.music.play(-1)
    tx = 5
    v = 10
    score = 0
    clock = pygame.time.Clock()
    camera = Camera()
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                tx += 0.01
                player_group.update(event)

        screen.fill('black')
        score += 1

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)
        if not player.mover(tx):
            running = False
            pygame.mixer.music.stop()
            end_screen(score)

        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()
