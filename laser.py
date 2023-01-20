import pygame
from pygame.sprite import Sprite

""" laser.py
    This class inherits from Sprite to make lasers that shoot and can collide with aliens. It includes
    its __init__ method to initialize all of its attributes, update method to keep the laser moving, 
    and draw_laser method which draws the laser on the screen.

    Written By: Noah Chaney
    Date: Jan 21, 2022
"""


class laser(Sprite):
    speed = 10.0

    def __init__(self, sa_game):
        super().__init__()

        self.screen = sa_game.screen
        self.color = (60, 60, 60)

        # our laser blasts aren't going to be based on an image
        # so we build a rect object for them
        self.rect = pygame.Rect(0, 0, 3, 15)

        # set the laser blast to be initially located at the top of the ship
        self.rect.midtop = sa_game.spaceship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_laser(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
