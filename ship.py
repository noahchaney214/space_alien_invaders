import pygame

""" ship.py
    This class creates a the player object ship. It can only move side to side and fire a laser when 
    the space bar is pressed (implementation in space_aliens.py). The methods in this class are __init__
    to initialize the attributes of the object, blit to blit the object to the screen, move to correctly
    move the object side to side by a constant number of pixels, and update to check collisions with the 
    sides of the screen and stopping the ship from continuing in that direction.
    
    Written By: Noah Chaney
    Date: Jan 21, 2022
"""


class ship:

    def __init__(self, sa_game):

        self.screen = sa_game.screen
        self.screen_rect = sa_game.screen.get_rect()

        # load the space ship image
        self.image = pygame.image.load("ship.png")

        # set the image to an appropriate size
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # set the midbottom value of the ship to be the same as the
        # midbottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        self.left = False
        self.right = False

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def move(self, direction):
        self.rect.x = self.rect.x + direction

    def update(self, direction):
        if self.right:
            self.rect.x += direction
        if self.left:
            self.rect.x -= direction
        if self.rect.right < self.screen_rect.right:
            self.rect.x += direction
        if self.rect.left > self.screen_rect.left:
            self.rect.x -= direction
