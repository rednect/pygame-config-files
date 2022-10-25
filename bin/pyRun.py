import pygame

pygame.init()
width, height = 1200, 700
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pet Warriors')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

tile_map = (
    '........................'
    '........................'
    '........................'
    '........................'
    '........................'
    '........................'
    '........................'
    '........................'
    '........................'
    '.......XXXXXXXXX........'
    '........................'
    'XXXXXXX..........XXXXXXX'
    'XXXXXXXXXXX...XXXXXXXXXX'
    'XXXXXXXXXXXXXXXXXXXXXXXX'
)

def draw_window(current_map):
    surface.fill(BRANCO)
    for y in range(len(current_map)):
        for x in range(len(current_map[y])):
            if current_map[y][x] == 'X':
                rect = pygame.Rect(x * 50, y * 50, 50, 50)
                pygame.draw.rect(surface, PRETO, rect)
    
    pygame.display.update()


def main ():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(tile_map)

if __name__ == '__main__':
    main()