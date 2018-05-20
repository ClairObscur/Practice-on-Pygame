import sys
import pygame
import pyganim

width = 1300
height = 800
move_speed = 1
gravity = 0.3
jump_power = 10
limit_speed = 20
anim_delay = 1
anim_stay = [('Mario/5.png', 1)]
anim_jump = [('Mario/7.png', 1)]
anim_right = [('Mario/2.png', 1)]
anim_left = [('Mario/9.png', 1)]
anim_jump_right = [('Mario/6.png', 1)]
anim_jump_left = [('Mario/8.png', 1)]

#Игровой экран
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('SuperMario')
screen = pygame.Surface((width, height))
background_image = pygame.image.load('Bricks/1.jpg')

from pygame.sprite import Sprite, collide_rect
from pygame import Surface

#Марио
class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = Surface((75, 95))
        self.xvel = 0
        self.yvel= 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.onGround = False

        # Анимация героя
        self.image.set_colorkey((0, 0, 0))
        self.AnimStay = pyganim.PygAnimation(anim_stay)
        self.AnimStay.play()
        self.AnimStay.blit(self.image, (0, 0))
        self.AnimRight = pyganim.PygAnimation(anim_right)
        self.AnimRight.play()
        self.AnimLeft = pyganim.PygAnimation(anim_left)
        self.AnimLeft.play()
        self.AnimJumpRight = pyganim.PygAnimation(anim_jump_right)
        self.AnimJumpRight.play()
        self.AnimJumpLeft = pyganim.PygAnimation(anim_jump_left)
        self.AnimJumpLeft.play()
        self.AnimJump = pyganim.PygAnimation(anim_jump)
        self.AnimJump.play()

    #Обновление героя
    def update(self, left, right, up, bricks):
        if left:
            self.xvel += -move_speed
            if abs(self.xvel) > limit_speed:
                self.xvel += move_speed

            self.image.fill((0, 0, 0))
            if up:
                self.AnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.AnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel += move_speed
            if abs(self.xvel) > limit_speed:
                self.xvel -= move_speed

            self.image.fill((0, 0, 0))
            if up:
                self.AnimJumpRight.blit(self.image, (0, 0))
            else:
                self.AnimRight.blit(self.image, (0, 0))

        if (left or right) == False:
            self.xvel = 0
            if not up:
                self.image.fill((0, 0, 0))
                self.AnimStay.blit(self.image, (0, 0))
        if up:
            if self.onGround:
                self.yvel = -jump_power
                self.image.fill((0, 0, 0))
                self.AnimJump.blit(self.image, (0, 0))

        self.yvel += gravity
        self.onGround = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, bricks)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, bricks)

    #Взаимодействие между объектами
    def collide(self, xvel, yvel, bricks):
         for brick in bricks:
             if collide_rect(self, brick):
                 if xvel > 0:
                     self.rect.right = brick.rect.left
                 if xvel < 0:
                     self.rect.left = brick.rect.right
                 if yvel > 0:
                     self.rect.bottom = brick.rect.top
                     self.onGround = True
                     self.yvel = 0
                 if yvel < 0:
                     self.rect.top = brick.rect.bottom
                     self.yvel = 0


from pygame.image import load

#Платформы
class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('Bricks/3.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Границы игрового поля
class Floor(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('Bricks/4.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

Mario = Player(100, 700)
left = right = up = False

sprite_group = pygame.sprite.Group()
sprite_group.add(Mario)
bricks =[]

#Макет уровня
level = [
       "**************************",
       "*         -------        *",
       "*                        *",
       "*                        *",
       "*   -                    *",
       "*                        *",
       "*                        *",
       "*               ------   *",
       "*                        *",
       "*                        *",
       "*   ----                 *",
       "*                        *",
       "*              ----      *",
       "*        --------        *",
       "*                        *",
       "**************************"]

x = 0
y = 0
for row in level:
    for col in row:
        if col == '-':
            platform = Platform(x, y)
            sprite_group.add(platform)
            bricks.append(platform)
        elif col == '*':
            floor = Floor(x, y)
            sprite_group.add(floor)
            bricks.append(floor)
        x += 50
    y += 50
    x = 0

timer = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame. K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False

    screen.blit(background_image, (0, 0))
    Mario.update(left, right, up, bricks)
    sprite_group.draw(screen)
    window.blit(screen, (0, 0))
    pygame.display.flip()
    pygame.display.update()
    timer.tick(60)
