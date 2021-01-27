import os
import random
import pygame
import time
import sqlite3
from collections import deque, namedtuple


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("archer_i_1.png").convert_alpha()
        self.image.set_colorkey([255,255,255])

        self.rect = self.image.get_rect()

class Vector():
    def __init__(self, Sprite):
        self.sprite = Sprite

    def move(self,dx,dy):
        if dx!=0:
            self.move_single_axis(dx,0)
        if dy!=0:
            self.move_single_axis(0,dy)

    def move_single_axis(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Uni game")
screen = pygame.display.set_mode((500,400))

clock = pygame.time.Clock()
player = Player()
vector_player = Vector(player)

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
    
    pygame.display.flip()

pygame.quit()
