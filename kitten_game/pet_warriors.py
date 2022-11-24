import pygame as pg
import sys, random
from classes import Cat, Dog, Floor, Obstacle, Platform, Button

pg.init()

FPS = 60
WIN_X, WIN_Y = 1080, 720
SCENE = "MENU"

sc = pg.display.set_mode([WIN_X, WIN_Y])
pg.display.set_caption('Pet Warriors')
clock = pg.time.Clock()

pg.font.init()
font1 = pg.font.Font('assets/joystix monospace.ttf', 30)
font = pg.font.Font('assets/joystix monospace.ttf', 70)

cat = Cat()
floor1 = Floor(1)
floor2 = Floor(2)

all_moving = pg.sprite.Group()
distance_moved = 0
obstacle_group = pg.sprite.Group()
dogs_group = pg.sprite.Group()

heart = pg.transform.scale(pg.image.load("assets/heart.png").convert_alpha(), (45 * 1.5, 45 * 1.5))
background = pg.transform.scale(pg.image.load("assets/background.png").convert_alpha(), (1920*0.75, 1080*0.75))

distance_of_prev_gen = 0

pg.mixer.music.load("assets/music.wav")
pg.mixer.music.play(loops=-1)

play_button = Button(WIN_X//2, WIN_Y//2 + 100, "Play", font)
mute_button = Button(WIN_X//2, WIN_Y//2 + 200, "Mute", font1)


def restart():
    global cat, SCENE, obstacle_group, dogs_group, all_moving
    cat = Cat()
    SCENE = "GAME"
    obstacle_group = pg.sprite.Group()
    dogs_group = pg.sprite.Group()
    all_moving = pg.sprite.Group()

def moveX(distance: int):
    global distance_moved, distance_of_prev_gen
    if distance < 0:
        cat.direction = "left"
        cat.rect.x += distance
        for obs in obstacle_group:
            if cat.rect.colliderect(obs.rect):
                cat.rect.x -= distance
                break

    elif distance > 0:
        cat.direction = "right"
        if cat.rect.x < 500:
            cat.rect.x += distance
            for obs in obstacle_group:
                if cat.rect.colliderect(obs.rect):
                    cat.rect.x -= distance
                    break

        else:
            cat.rect.x += distance
            for obs in obstacle_group:
                if cat.rect.colliderect(obs.rect):
                    cat.rect.x -= distance
                    break
            else:
                cat.rect.x -= distance
                for sprite in all_moving.sprites():
                    sprite.rect.x -= distance
                floor1.rect.x -= distance
                floor2.rect.x -= distance
                distance_moved += distance
    if distance_moved > distance_of_prev_gen + 1000:
        distance_of_prev_gen = distance_moved
        generate_obstacles()
    cat.time += 1
    if distance > 0 and distance_moved / 150 > cat.score: cat.score += distance / 200

    elif cat.score >= 100:
        cat.score += distance / 80
        


def generate_obstacles():
    rand = random.randint(0, 4)

    if rand == 0 or rand == 4:
        ob = Obstacle(1100, 720 - 50 - random.randint(60, 230))
        ob2 = Obstacle(1800, 720 - 50 - random.randint(60, 230))
        all_moving.add(ob)
        obstacle_group.add(ob)
        all_moving.add(ob2)
        obstacle_group.add(ob2)
        dog = Dog(1300)
        all_moving.add(dog)
        dogs_group.add(dog)

    elif rand == 1:
        plat = Platform(1100, 720 - 50 - random.randint(120, 230), 3)
        all_moving.add(plat)
        obstacle_group.add(plat)
        dog = Dog(1150, platform=plat)
        all_moving.add(dog)
        dogs_group.add(dog)

    elif rand == 2:
        plat = Platform(1100, 720 - 50 - random.randint(120, 230), 2)
        all_moving.add(plat)
        obstacle_group.add(plat)
        dog = Dog(1150, platform=plat)
        all_moving.add(dog)
        dogs_group.add(dog)

    elif rand == 3:
        plat = Platform(1100, 720 - 50 - random.randint(120, 230), 1)
        all_moving.add(plat)
        obstacle_group.add(plat)
        plat2 = Platform(1500, 720 - 50 - random.randint(120, 230), 2)
        all_moving.add(plat2)
        obstacle_group.add(plat2)
        dog = Dog(1550, platform=plat2)
        all_moving.add(dog)
        dogs_group.add(dog)


def draw():
    sc.fill((255, 255, 255))
    sc.blit(background, (0, 0))
    if SCENE == "GAME":
        for sprite in all_moving.sprites():
            sprite.update(sc, obstacle_group, cat)

        floor1.update(sc)
        floor2.update(sc)

        scoreText = font.render(str(round(cat.score)), False, (0, 0, 0))
        scoreRect = scoreText.get_rect()
        scoreRect.topleft = (20, 10)
        sc.blit(scoreText, scoreRect)

        heathText = font.render(str(round(cat.lives)) + "x", False, (0, 0, 0))
        healthRect = heathText.get_rect()
        healthRect.topright = (1080-100, 10)
        sc.blit(heathText, healthRect)

        sc.blit(heart, (1080-90, 25))

        cat.update(sc, obstacle_group, cat, dogs_group)

    elif SCENE == "MENU":
        scoreText = font.render("Pet Warriors", False, (255,255,255))
        scoreRect = scoreText.get_rect()
        scoreRect.center = (WIN_X // 2, 60)
        sc.blit(scoreText, scoreRect)

        if play_button.rect.collidepoint(pg.mouse.get_pos()):
            play_button.draw(sc, True)
        else: play_button.draw(sc, False)

        if mute_button.rect.collidepoint(pg.mouse.get_pos()):
            mute_button.draw(sc, True)
        else: mute_button.draw(sc, False)

        if cat.score != 0:
            scoreText = font1.render(f"Score:{round(cat.score)}", False, (255,255,255))
            scoreRect = scoreText.get_rect()
            scoreRect.center = (WIN_X//2, 130)
            sc.blit(scoreText, scoreRect)

    pg.display.update()


generate_obstacles()
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                generate_obstacles()
            if SCENE == "END" and event.key == pg.K_SPACE:
                restart()
        elif SCENE == "MENU" and event.type == pg.MOUSEBUTTONDOWN:
            if play_button.rect.collidepoint(pg.mouse.get_pos()):
                SCENE = "GAME"
                restart()
            elif mute_button.rect.collidepoint(pg.mouse.get_pos()):
                if pg.mixer.music.get_volume() == 0:
                    mute_button = Button(1080//2, 720//2 + 200, "Mute", font1)
                    pg.mixer.music.set_volume(100)
                else:
                    mute_button = Button(1080//2, 720//2 + 200, "UnMute", font1)
                    pg.mixer.music.set_volume(0)

    if SCENE == "GAME":
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            moveX(-5)
        if keys[pg.K_RIGHT]:
            moveX(5)
        if keys[pg.K_SPACE]:
            if not cat.jumping:
                cat.jump()

    if cat.score >= 75:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            moveX(-10)
        if keys[pg.K_RIGHT]:
            moveX(10)
        if keys[pg.K_SPACE]:
            if not cat.jumping:
                cat.jump()
    
    elif cat.score >= 300:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            moveX(-15)
        if keys[pg.K_RIGHT]:
            moveX(15)
        if keys[pg.K_SPACE]:
            if not cat.jumping:
                cat.jump()
    
    if cat.lives <= 0:
        SCENE = "MENU"

    draw()

pg.quit()
