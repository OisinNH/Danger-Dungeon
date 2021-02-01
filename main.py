"""
Show the proper way to organize a game using the a game class.

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Explanation video: http://youtu.be/O4Y5KrNgP_c
"""

import pygame
import shapely
import random
from shapely.geometry import LineString
import pygame.freetype
import math

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BEIGE = (191, 175, 126)
GREY = (128, 128, 128)
BULLET_TRAVEL = 5

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# --- Classes ---


class Enemy(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.health = 100
        self.ranged = False
    def shoot(self, target_x, target_y):
        self.enemy_bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
    def update(self)
        self.shoot(game)


class EnemyRanged(Enemy):
    def __init__(self):
        super().__init__()
        self.ranged = True


class EnemyMelee(Enemy):
    def __init__(self):
        super().__init__()


class Character(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.health = 100
        self.attack_modifier = 1
        self.strength_modifier = 1
        self.rect.x = 50
        self.rect.y = 50

    def shoot(self, target_x, target_y):
        self.bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)


    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Pointer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect(center=[x, y])

        self.image = pygame.image.load("pointer.png")
        self.rect.center = (self.rect.centerx, self.rect.centery)

    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


class Collectable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.rect.centery = y
        self.rect.centerx = x

        self.bullet_line = LineString([(x, y), (target_x, target_y)])
        self.bullet_target = self.bullet_line.interpolate(5)

        self.bullet_movement_x = self.bullet_target.x - x
        self.bullet_movement_y = self.bullet_target.y - y

    def update(self):
        self.rect.x += self.bullet_movement_x
        self.rect.y += self.bullet_movement_y

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.rect.centery = y
        self.rect.centerx = x

        self.bullet_line = LineString([(x, y), (target_x, target_y)])
        self.bullet_target = self.bullet_line.interpolate(5)

        self.bullet_movement_x = self.bullet_target.x - x
        self.bullet_movement_y = self.bullet_target.y - y

    def update(self):
        self.rect.x += self.bullet_movement_x
        self.rect.y += self.bullet_movement_y



class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.enemy_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(10):
            enemy = Enemy()

            enemy.rect.x = random.randrange(SCREEN_WIDTH)
            enemy.rect.y = random.randrange(-300, SCREEN_HEIGHT)

            self.enemy_list.add(enemy)
            self.all_sprites_list.add(enemy)

        # Create the playerwa
        self.character = Character()
        self.all_sprites_list.add(self.character)
        # Create Player Speed
        self.speed_x = 0
        self.speed_y = 0

        # Create Pointer
        self.pointer = Pointer(960, 540)
        self.all_sprites_list.add(self.pointer)

        #Create Walls

        for x in range (1881):
            if x % 40 == 0 :
                self.wall = Wall(x, 0)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)
                self.wall = Wall(x, 1040)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)
        for y in range (1041):
            if y % 40 == 0 :
                self.wall = Wall(0, y)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)
                self.wall = Wall(1880, y)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)



    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
                else:
                    self.character.shoot(self.pointer.rect.centerx, self.pointer.rect.centery)
                    self.bullet_list.add(self.character.bullet)
                    self.all_sprites_list.add(self.character.bullet)
            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.speed_x += 1
                if event.key == pygame.K_a:
                    self.speed_x -= 1
                if event.key == pygame.K_w:
                    self.speed_y -= 1
                if event.key == pygame.K_s:
                    self.speed_y += 1
            # Removing the movement when letting go
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.speed_x -= 1
                if event.key == pygame.K_a:
                    self.speed_x += 1
                if event.key == pygame.K_w:
                    self.speed_y += 1
                if event.key == pygame.K_s:
                    self.speed_y -= 1

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            # self.all_sprites_list.update()

            if self.bullet_list:
                # See if the player's bullet has collided with anything.
                enemies_hit_list = pygame.sprite.spritecollide(self.character.bullet, self.enemy_list, True)
                self.character.bullet.update()

                # Check the list of collisions.
                for enemy in enemies_hit_list:
                    self.score += 1
                    print(self.score)
                    # You can do something with "block" here.


            temp_character_x = self.character.rect.x
            temp_character_y = self.character.rect.y
            self.character.update(self.speed_x, self.speed_y)
            wall_hit_list = pygame.sprite.spritecollide(self.character, self.wall_list, False)
            player_enemy_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_list, False)
            if player_enemy_hit_list:
                self.character.health -= 5
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y
            if wall_hit_list:
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y

            if len(self.enemy_list) == 0:
                self.game_over = True


            self.pointer.update()

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BEIGE)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)
            pygame.draw.aaline(screen, GREEN, [self.character.rect.centerx, self.character.rect.centery],
                               [self.pointer.rect.x + 20, self.pointer.rect.y + 20], 5)
        if self.bullet_list:
            print(self.character.bullet.bullet_target.x, self.character.bullet.bullet_target.y, self.character.bullet.rect.center)

        health_text = pygame.freetype.SysFont("Arial", 30)
        health_display, _ = health_text.render("Health = " + str(self.character.health), BLACK)
        screen.blit(health_display, (50, 1050))

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(144)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
