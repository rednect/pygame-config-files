import pygame as pg


pg.mixer.init()
pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pg.init() #turn all of pygame on.

woof = pg.mixer.Sound("assets/woof.wav")
meow = pg.mixer.Sound("assets/meow.wav")


class Cat(pg.sprite.Sprite):
    def __init__(self):
        width = 100
        height = 85
        pg.sprite.Sprite.__init__(self)

        self.imagesNames = ["assets/cat1.png", "assets/cat2.png"]
        self.images = []

        for i in self.imagesNames:
            self.images.append(pg.transform.scale(pg.image.load(i).convert_alpha(), (width, height)))
            self.images.append(
                pg.transform.flip(pg.transform.scale(pg.image.load(i).convert_alpha(), (width, height)), True, False))

        self.rect = pg.Rect(500, 10, width, height)
        self.Yforce = 0
        self.jumping = True
        self.direction = "left"
        self.time = 0
        self.lives = 7
        self.wounded = False
        self.wounded_timer = 120
        self.score = 0

    def update(self, sc, obstacle_group, cat, dogs_group):
        if self.wounded: self.wounded_timer -= 1
        if self.wounded_timer <= 0:
            self.wounded_timer = 120
            self.wounded = False
        if self.rect.y == 720 - 50 - self.rect.height: self.jumping = False
        if self.rect.y < 720 - 50 - self.rect.height:

            self.Yforce -= 50 * 1 / 60
            self.moveY(-self.Yforce)
            for obs in obstacle_group:
                if self.rect.colliderect(obs.rect):
                    if self.Yforce < 0:
                        self.rect.y = obs.rect.y - 85
                        self.jumping = False
                    else:
                        self.rect.y = obs.rect.y + obs.rect.height
                    self.Yforce = 0
                    break
            if self.rect.y > 720 - 50 - self.rect.height:
                self.rect.y = 720 - 50 - self.rect.height
                self.jumping = False
        else:
            self.Yforce = 0

        if self.direction == "left":
            if self.time < 7:
                img = self.images[0]
                if self.wounded:
                    img.set_alpha(50)
                else:
                    img.set_alpha(256)
                sc.blit(img, self.rect)
            else:
                if self.time >= 14: self.time = 0
                img = self.images[2]
                if self.wounded:
                    img.set_alpha(50)
                else:
                    img.set_alpha(256)
                sc.blit(img, self.rect)

        elif self.direction == "right":
            if self.time < 7:
                img = self.images[1]
                if self.wounded:
                    img.set_alpha(50)
                else:
                    img.set_alpha(256)
                sc.blit(img, self.rect)
            else:
                if self.time >= 14:
                    self.time = 0

                img = self.images[3]
                if self.wounded:
                    img.set_alpha(50)
                else:
                    img.set_alpha(256)
                sc.blit(img, self.rect)

        for dog in dogs_group:
            if self.rect.colliderect(dog.rect):
                if self.rect.y + 85 < dog.rect.y + 10 and self.Yforce < 0 and not self.wounded:
                    self.score += 5
                    dog.kill()
                    del dog
                    pg.mixer.Sound.play(woof)

    def moveY(self, distance: int):
        self.rect.y += distance

    def jump(self):
        self.jumping = True
        self.Yforce = 20
        self.moveY(-1)


class Dog(pg.sprite.Sprite):
    def __init__(self, x, platform=None):
        pg.sprite.Sprite.__init__(self)
        self.direction = "left"
        self.time = 0
        self.platform = platform

        self.imagesNames = ["assets/dog1.png", "assets/dog2.png"]
        self.images = []

        for i in self.imagesNames:
            self.images.append(pg.transform.scale(pg.image.load(i).convert_alpha(), (95, 95)))
            self.images.append(
                pg.transform.flip(pg.transform.scale(pg.image.load(i).convert_alpha(), (95, 95)), True, False))

        if self.platform:
            self.rect = pg.Rect(x, self.platform.rect.y - 95, 95, 95)
        else:
            self.rect = pg.Rect(x, 720 - 50 - 95, 95, 95)
        self.speed = 3

    def update(self, sc, obstacle_group, cat):
        self.time += 1
        if self.direction == "left":
            self.rect.x -= self.speed
            for obs in obstacle_group:
                if self.rect.colliderect(obs.rect):
                    self.rect.x += self.speed
                    self.direction = "right"
                    break

            if self.time < 7:
                sc.blit(self.images[0], self.rect)
            else:
                if self.time >= 14: self.time = 0
                sc.blit(self.images[2], self.rect)

        elif self.direction == "right":
            self.rect.x += self.speed
            for obs in obstacle_group:
                if self.rect.colliderect(obs.rect):
                    self.rect.x -= self.speed
                    self.direction = "left"
                    break

            if self.time < 7:
                sc.blit(self.images[1], self.rect)
            else:
                if self.time >= 14: self.time = 0
                sc.blit(self.images[3], self.rect)

        if self.platform:
            if self.rect.x < self.platform.rect.x or self.rect.x + self.rect.width > self.platform.rect.x + self.platform.rect.width:
                if self.direction == "left":
                    self.direction = "right"
                elif self.direction == "right":
                    self.direction = "left"

        if not cat.wounded:
            if self.rect.colliderect(cat.rect):
                if not cat.rect.y + 85 < self.rect.y + 10:
                    cat.lives -= 1
                    cat.wounded = True
                    pg.mixer.Sound.play(meow)

        if self.rect.x < -1000:
            pg.sprite.Sprite.kill(self)
            del self


class Floor(pg.sprite.Sprite):
    def __init__(self, num):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load("assets/floor.png").convert(), (1080, 50))
        self.rect = pg.Rect((num - 1) * 1080, 720 - 50, 1080, 50)

    def update(self, sc):
        if self.rect.x + 1080 < 0:
            self.rect.x += 2160
        elif self.rect.x > 1080:
            self.rect.x -= 2160
        sc.blit(self.image, self.rect)


class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x, y, 100, 300)
        self.image = pg.transform.scale(pg.image.load("assets/obstacle.png").convert_alpha(), (100, 300))

    def update(self, sc, obstacle_group, cat):
        sc.blit(self.image, self.rect)
        if self.rect.x < -1000:
            pg.sprite.Sprite.kill(self)
            del self


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        pg.sprite.Sprite.__init__(self)

        self.imagesNames = [["assets/platform_small.png", 41], ["assets/platform_mid.png", 64],
                            ["assets/platform_large.png", 80]]
        self.images = []
        self.size = size - 1

        for i in self.imagesNames:
            self.images.append(pg.transform.scale(pg.image.load(i[0]).convert_alpha(), (i[1] * 5, 45)))

        self.rect = pg.Rect(x, y, self.images[self.size].get_rect().width, self.images[self.size].get_rect().height)

    def update(self, sc, obstacle_group, cat):
        sc.blit(self.images[self.size], self.rect)
        if self.rect.x < -1000:
            pg.sprite.Sprite.kill(self)
            del self


class Button(pg.Rect):
    def __init__(self, x, y, text, font):
        self.text = font.render(text, False, (0, 0, 0))
        self.textHover = font.render(text, False, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
        self.rect = pg.Rect(self.textRect.x - 26, self.textRect.y - 10, self.textRect.width + 50, self.textRect.height + 20)

    def draw(self, sc, hover):
        if hover:
            pg.draw.rect(sc, (0, 0, 0), self.rect)
            pg.draw.rect(sc, (255, 255, 255), self.rect, 5)
            sc.blit(self.textHover, self.textRect)
        else:
            pg.draw.rect(sc, (255, 255, 255), self.rect)
            pg.draw.rect(sc, (0, 0, 0), self.rect, 5)
            sc.blit(self.text, self.textRect)