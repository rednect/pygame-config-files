import pygame

pygame.init()
width, height = 1200, 700
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pet Warriors')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

tile_map = (
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '.......XXXXXXXXX........',
    '........................',
    '........................',
    'XXXXXXX..........XXXXXXX',
    'XXXXXXXXXXX...XXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXX'
)

class Character:
     def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

class Player(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 10)


def draw_window(current_map, player):
    surface.fill(PRETO)
    for y in range(len(current_map)):
        for x in range(len(current_map[y])):
            if current_map[y][x] == 'X':
                rect = pygame.Rect(x * 50, y * 50, 50, 50)
                pygame.draw.rect(surface, BRANCO, rect)

    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    pygame.draw.rect(surface, VERMELHO, player_rect)
    
    pygame.display.update()


def main ():
    run = True
    clock = pygame.time.Clock()
    fps = 60

    player = Player(50, 500, 5, 50)

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(tile_map, player)

if __name__ == '__main__':
    main()