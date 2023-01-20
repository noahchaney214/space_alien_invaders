import sys
import pygame

from alien import alien
from ship import ship
from laser import laser


""" space_aliens.py
    This is the heart of the game, including the main class and the game loop. This class sets the screen
    size, background color, and controls all sounds and music throughout the game. The game events are 
    controlled by an if/elif structure and this class inherits from space_ship.py, laser_blast.py
    
    Dialogue:
    A group of hostile aliens will spawn upon starting the program and begin to make their way down towards 
    the player. The player's (your) job is to shoot all of the aliens before they reach you. At the end of 
    each game there is a scoreboard that shows up for 5 seconds to tell you your score and time. Due to damage
    to our equipment, you are limited to 5 lasers in the air at any given time. Good luck Cadet, 
    the world is counting on you.
    
    Written By: Noah Chaney
    Date: Jan 21, 2022
"""


class space_aliens:

    def __init__(self):
        pygame.init()

        self.width = 1200
        self.height = 800

        self.alive = True

        font = pygame.font.Font(None, 30)
        self.text = font.render('', True, (255, 255, 255))
        self.text_rect = self.text.get_rect()

        self.won = False

        self.clock = pygame.time.Clock()

        # get a Surface object for the screen
        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size)

        self.blasts = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.alien_count = 0
        self.num_aliens = 0

        self.counter = 0
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

        x = 0
        y = 0
        num_aliens = 15
        for a in range(num_aliens):
            a = alien(self, x, y)
            self.num_aliens += 1
            b = alien(self, x, y + 50)
            self.num_aliens += 1
            c = alien(self, x, y + 100)
            self.num_aliens += 1
            self.aliens.add(a)
            self.aliens.add(b)
            self.aliens.add(c)
            a.update()
            b.update()
            c.update()
            x += 50

        # set the caption for the screen
        pygame.display.set_caption("Space Aliens: CS 328 Assignment 2 Noah Chaney")

        # set the background color
        self.bg_color = (0, 0, 35)

        self.spaceship = ship(self)

        self.speed = 10

    def start(self):
        background = pygame.mixer.Sound('background.mp3')
        background.set_volume(0.75)
        background.play()
        while 1:  # event loop
            self.screen.fill(self.bg_color)
            self.clock.tick(60)
            if self.alive and not self.won:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.spaceship.left = True
                        if event.key == pygame.K_RIGHT:
                            self.spaceship.right = True
                        if len(self.blasts) < 5:
                            if event.key == pygame.K_SPACE:
                                laser_sound = pygame.mixer.Sound('8-bit-laser.wav')
                                laser_sound.set_volume(0.5)
                                laser_sound.play()
                                self.fire_laser_blast()

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.spaceship.left = False
                        if event.key == pygame.K_RIGHT:
                            self.spaceship.right = False

                    elif event.type == self.timer_event:
                        self.counter += 1
                        font = pygame.font.SysFont(None, 30)
                        self.text = font.render(str(self.counter), True, (0, 128, 0))
                        self.text_rect = self.text.get_rect()
                        self.text_rect.center = (30, self.height - 30)
                        if self.counter == 0:
                            pygame.time.set_timer(self.timer_event, 0)
                self.screen.blit(self.text, self.text_rect)

                for b in self.blasts.sprites():
                    b.draw_laser()
                    if pygame.sprite.groupcollide(self.blasts, self.aliens, True, True):
                        explode_sound = pygame.mixer.Sound('8-bit-explosion.wav')
                        explode_sound.set_volume(0.5)
                        explode_sound.play()
                        self.alien_count += 1
                        num_aliens = len(self.aliens)
                        if num_aliens == 0:
                            self.won = True
                            self.alien_count = self.num_aliens
                            background.stop()
                    if b.rect.top < 0:
                        self.blasts.remove(b)

                for a in self.aliens:
                    a.draw_alien()

                if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
                    background.stop()
                    self.alive = False
                    self.aliens.remove(self.aliens)
                    explode_sound = pygame.mixer.Sound('8-bit-explosion.wav')
                    explode_sound.set_volume(0.5)
                    explode_sound.play()

                self.blasts.update()

                # display the ship
                self.spaceship.update(self.speed)
                self.spaceship.blit()

                # updates the screen
                pygame.display.flip()

            elif self.won:
                game_over = pygame.mixer.Sound('win.wav')
                game_over.set_volume(0.5)
                game_over.play()
                x = 5
                while x > 0:
                    self.win()
                    font = pygame.font.SysFont(None, 15)
                    time = font.render('Exiting in: %d' % x, True, (0, 128, 0))
                    time_rect = time.get_rect()
                    time_rect.center = (50, 30)
                    self.screen.blit(time, time_rect)
                    x -= 1
                    pygame.display.flip()
                    pygame.time.delay(1000)
                break
            elif not self.alive:
                game_over = pygame.mixer.Sound('game-over.wav')
                game_over.set_volume(0.5)
                game_over.play()
                x = 5
                while x > 0:
                    self.lose()
                    font = pygame.font.SysFont(None, 15)
                    time = font.render('Exiting in: %d' % x, True, (0, 128, 0))
                    time_rect = time.get_rect()
                    time_rect.center = (50, 30)
                    self.screen.blit(time, time_rect)
                    x -= 1
                    pygame.display.flip()
                    pygame.time.delay(1000)
                break

    def fire_laser_blast(self):
        myBlast = laser(self)
        self.blasts.add(myBlast)

    def lose(self):
        self.screen.fill(self.bg_color)
        red = (150, 0, 0)
        font = pygame.font.Font(None, 70)
        lose = font.render('GAME OVER', True, red)
        loseRect = lose.get_rect()
        loseRect.center = (self.width // 2, self.height // 2)
        self.screen.blit(lose, loseRect)
        self.score_board()

    def win(self):
        self.screen.fill(self.bg_color)
        white = (255, 255, 255)
        font = pygame.font.Font(None, 50)
        win = font.render('You Win', True, white)
        winRect = win.get_rect()
        winRect.center = (self.width // 2, self.height // 2)
        self.screen.blit(win, winRect)
        self.score_board()

    def score_board(self):
        white = (255, 255, 255)
        table_font = pygame.font.Font(None, 30)
        table_1 = table_font.render('|-------ScoreBoard--------|', True, white)
        table_1_rect = table_1.get_rect()
        table_1_rect.center = (self.width // 2, self.height // 2 + 50)
        table_2 = table_font.render('Aliens Killed:           %d' % self.alien_count, True, white)
        table_2_rect = table_2.get_rect()
        table_2_rect.center = (self.width // 2, self.height // 2 + 75)
        table_3 = table_font.render('Time:                    %d' % self.counter, True, white)
        table_3_rect = table_3.get_rect()
        table_3_rect.center = (self.width // 2, self.height // 2 + 100)
        if not self.alive:
            score = ((2*self.alien_count - self.counter) * 15) / 6
        else:
            score = ((2*self.alien_count - self.counter) * 15) / 2
        table_4 = table_font.render('Score:                   %d' % score, True, white)
        table_4_rect = table_4.get_rect()
        table_4_rect.center = (self.width // 2, self.height // 2 + 125)

        self.screen.blit(table_1, table_1_rect)
        self.screen.blit(table_2, table_2_rect)
        self.screen.blit(table_3, table_3_rect)
        self.screen.blit(table_4, table_4_rect)


"""This section looks at a special python variable called __name__
This variable is set when the program is executed.
If the value of __name__ is set to "__main__", 
then we know the file is being run as the main method for the program.
So, since we are the main program we'll create an instance of our class
and then call the start() method."""
if __name__ == '__main__':
    myGame = space_aliens()
    myGame.start()
