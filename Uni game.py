import os
import random
import pygame
import time
import sqlite3
from collections import deque, namedtuple

wall_sprites = pygame.sprite.Group()
walls = []
width = 500
height = 500

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("archer_i_1.png").convert_alpha()
        self.image.set_colorkey([255,255,255])
        self.rect = self.image.get_rect()
        
class Vector:
    def __init__(self, sprite):
        self.sprite = sprite

    def move(self,dx,dy):
        if dx!=0:
            self.move_single_axis(dx,0)
        if dy!=0:
            self.move_single_axis(0,dy)

    def move_single_axis(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy
        for wall in walls:
            if self.sprite.rect.colliderect(wall.rect):
                if dx > 0:
                    self.sprite.rect.right = wall.rect.left
                if dx < 0:
                    self.sprite.rect.left = wall.rect.right
                if dy > 0:
                    self.sprite.rect.bottom = wall.rect.top
                if dy < 0:
                    self.sprite.rect.top = wall.rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, wx, wy):
        super().__init__()
        walls.append(self)
        self.image = pygame.image.load("tree.png").convert_alpha()
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (width//14, height//9))
        self.rect = self.image.get_rect(center=(width//2,height//2))

    def rect(self):
        rect = self.rect
        return rect
                    


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Uni game")
screen = pygame.display.set_mode((500,500))

clock = pygame.time.Clock()
player = Player()
wall = Wall(width//2,height//2)
wall_sprites.add(wall)
vector_player = Vector(player)
player.rect.x= 100
player.rect.y = 100

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_UP]:
        vector_player.move(0,-2)

    if user_input[pygame.K_DOWN]:
        vector_player.move(0,2)

    if user_input[pygame.K_LEFT]:
        vector_player.move(-2,0)

    if user_input[pygame.K_RIGHT]:
        vector_player.move(2,0)

    screen.fill((0,0,0))
    all_sprites_list = pygame.sprite.Group()

    all_sprites_list.add(player)

    all_sprites_list.draw(screen)
    wall_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
