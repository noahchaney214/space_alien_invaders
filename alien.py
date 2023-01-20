import pygame
from pygame.sprite import Sprite

""" alien.py
    This class inherits from Sprite for more efficient collision detection and grouping. This class
    contains its __init__ method to initialize its attributes and create the object, blit method to blit 
    the alien to the screen, move method to keep the aliens moving, and update method to make sure they
    change direction and move down a unit when they hit a side of the screen.
    
    Written By: Noah Chaney
    Date: Jan 21, 2022
"""


class alien(Sprite):

    def __init__(self, sa_game, init_x, init_y):
        super().__init__()

        self.left = True
        self.right = False

        self.dir = 10

        self.y = init_y
        self.screen = sa_game.screen
        self.screen_rect = sa_game.screen.get_rect()

        # load the space ship image
        self.image = pygame.image.load("alien.png")

        self.width = 50
        self.height = 50
        # set the image to an appropriate size
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # set the topleft value of the ship to be the same as the
        # topleft of the screen
        self.rect.topleft = (init_x, init_y)

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def move(self, direction):
        self.rect.x = self.rect.x + direction
        self.rect.y = self.y

    def update(self):
        if self.rect.right > self.screen_rect.width or self.rect.left < 0:
            self.dir = -self.dir
            self.y += self.height

        self.move(self.dir)

        self.screen.blit(self.image, self.rect)

    def draw_alien(self):
        self.update()
