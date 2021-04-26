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
import pygame.mixer

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


class EnemyRanged(Enemy):
    def __init__(self):
        super().__init__()
        self.ranged = True

    def shoot(self, target_x, target_y):
        self.enemy_bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)

    def update(self):
        self.rect.x += 0
        # self.shoot(game)


class EnemyMelee(Enemy):
    def __init__(self):
        super().__init__()
    def hit(self):
        self.enemy_melee_hit = EnemyMelee_Hit(self.rect.centerx, self.rect.centery)


class EnemyMelee_Hit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 60])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class TextBox_Title(TextBox):
    def __init__(self, x, y):
            super().__init__(x, y)
            self.image = pygame.Surface([1250, 160])
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

class TextBox_Options(TextBox):
    def __init__(self, x, y):
            super().__init__(x, y)
            self.image = pygame.Surface([250, 160])
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

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

class PointerTitle(Pointer):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.image = pygame.image.load("pointer2.png")



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

        self.x_difference = target_x - x
        self.y_difference = target_y - y

        self.target_angle = math.atan2(self.y_difference, self.x_difference);
        self.x_change = math.cos(self.target_angle) * BULLET_TRAVEL
        self.y_change = math.sin(self.target_angle) * BULLET_TRAVEL
        self.x = self.rect.x
        self.y = self.rect.y

        # self.distance = math.dist(x, y, target_x, target_y)
        # self.distance_division = self.distance / 5

    # self.bullet_line = LineString([(x, y), (target_x, target_y)])
    # self.bullet_target = self.bullet_line.interpolate(5)

    # self.bullet_movement_x = self.bullet_target.x - x
    # self.bullet_movement_y = self.bullet_target.y - y

    def update(self):
        # self.rect.x += self.bullet_movement_x
        # self.rect.y += self.bullet_movement_y

        self.x += self.x_change
        self.y += self.y_change

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


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
        self.enemy_ranged_list = pygame.sprite.Group()
        self.enemy_melee_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.collectable_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.enemy_melee_hit_list = pygame.sprite.Group()

        # map file read
        with open('lvl1.txt', 'r') as file:
        # written to a list
            self.lvlmap = file.readlines()

        self.test = 1
        for x in range(1881):
            if x % 40 == 0:
                self.wall = Wall(x, 0)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)
                self.wall = Wall(x, 1040)
                self.wall_list.add(self.wall)
                self.all_sprites_list.add(self.wall)

                wall_x = x / 20
                wall_y = 0
                
                self.map_replace(wall_x, wall_y, "O")
                self.map_replace(wall_x+1, wall_y, "O")
                self.map_replace(wall_x, wall_y+1, "O")
                self.map_replace(wall_x+1, wall_y+1, "O")

                wall_x = x / 20
                wall_y = 52

                self.map_replace(wall_x, wall_y, "O")
                self.map_replace(wall_x+1, wall_y, "O")
                self.map_replace(wall_x, wall_y+1, "O")
                self.map_replace(wall_x+1, wall_y+1, "O")

                #self.lvlmap[x//20] = "O"
               # self.lvlmap[(x // 20 )+ 1] = "O"
                #self.lvlmap[(x // 20) + 96] = "O"
               # self.lvlmap[(x // 20) + 1 + 96] = "O"

               # self.lvlmap[x//20 + 96*52] = "O"
                #self.lvlmap[(x // 20 + 96 * 52) + 96] = "O"
               # self.lvlmap[(x // 20 + 96 * 52)+ 1] = "O"
                #self.lvlmap[(x // 20 + 96 * 52) + 1 + 96] = "O"
        for y in range(1041):
            if y % 40 == 0:

                wall_x = 0
                wall_y = y / 20

                if self.map_checker(wall_x, wall_y, "/"):

                    self.wall = Wall(0, y)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y,"O")
                    self.map_replace(wall_x+1, wall_y, "O")
                    self.map_replace(wall_x, wall_y+1, "O")
                    self.map_replace(wall_x+1, wall_y+1, "O")

                wall_x = 95

                if self.map_checker(wall_x, wall_y, "/"):

                    self.wall = Wall(1880, y)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y,"O")
                    self.map_replace(wall_x+1, wall_y, "O")
                    self.map_replace(wall_x, wall_y+1, "O")
                    self.map_replace(wall_x+1, wall_y+1, "O")

                #if self.lvlmap[(y//20)*96] == "_":
                                    #self.lvlmap[(y//20)*96] = "O"
                    #self.lvlmap[((y // 20) * 96) + 1] = "O"
                    #self.lvlmap[((y // 20) * 96) + 96] = "O"
                    #self.lvlmap[((y // 20) * 96) + 1 + 96] = "O"

                    #self.lvlmap[95 + (y//20) * 96] = "O"
                    #self.lvlmap[(95 + (y // 20) * 96) + 1] = "O"
                    #self.lvlmap[(95 + (y // 20) * 96) + 96] = "O"
                    #self.lvlmap[(95 + (y // 20) * 96) + 1 + 96] = "O"
        #for x in range(1881):
           # if x % 40 == 0:
              #  r = random.randint(20)
                   # if r == 0


        # Create the block sprites
        # Creating Ranged Enemies
        for i in range(5):


            x = random.randrange(40,1861)
            y = random.randrange(40,1021)

            er_x = x // 20
            er_y = y //20

            # checking the entity map
            if not self.map_checker(er_x, er_y, "/"):
            #if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                enemy_ranged = EnemyRanged()
                enemy_ranged.rect.x = x
                enemy_ranged.rect.y = y

                self.enemy_list.add(enemy_ranged)
                self.all_sprites_list.add(enemy_ranged)
                self.enemy_ranged_list.add(enemy_ranged)

                self.map_replace(er_x, er_y, "r")
                self.map_replace(er_x+1, er_y, "r")
                self.map_replace(er_x, er_y+1, "r")
                self.map_replace(er_x+1, er_y+1, "r")
                # self.lvlmap[(x//20) + (y//20 * 96)] = "er"



        #creating meelee enemies
        for i in range(5):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            em_x = x // 20
            em_y = y // 20

            # checking the entity map
            if not self.map_checker(em_x, em_y, "/"):
            #if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                enemy_melee = EnemyMelee()

                enemy_melee.rect.x = x
                enemy_melee.rect.y = y

                self.enemy_list.add(enemy_melee)
                self.all_sprites_list.add(enemy_melee)
                self.enemy_melee_list.add(enemy_melee)

                self.map_replace(em_x, em_y, "m")
                self.map_replace(em_x + 1, em_y, "m")
                self.map_replace(em_x, em_y + 1, "m")
                self.map_replace(em_x + 1, em_y + 1, "m")
                #self.lvlmap[(x//20) + (y//20 * 96)] = "em"


        #Creating Collectables
        for i in range(4):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            pu_x = x // 20
            pu_y = y // 20

            #checking the entity map
            if not self.map_checker(pu_x, pu_y, "/"):
            #if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                #self.lvlmap[(x//20) + (y//20 * 96)] = "pu"
                self.collectable = Collectable()

                self.collectable.rect.x = x
                self.collectable.rect.y = y

                self.collectable_list.add(self.collectable)
                self.all_sprites_list.add(self.collectable)

                self.map_replace(pu_x, pu_y, "c")
                self.map_replace(pu_x + 1, pu_y, "c")
                self.map_replace(pu_x, pu_y + 1, "c")
                self.map_replace(pu_x + 1, pu_y + 1, "c")

        # Create the playerwa
        self.character = Character()
        self.all_sprites_list.add(self.character)
        # Create Player Speed
        self.speed_x = 0
        self.speed_y = 0

        # Create Pointer
        self.pointer = Pointer(960, 540)
        self.all_sprites_list.add(self.pointer)

        # Create Walls




        self.enemy_timer = 0  # Temporary thing for enemies shooting - should remove soon

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
            self.enemy_melee_timer = 0
            if self.bullet_list:
                # See if the player's bullet has collided with anything.
                enemies_hit_list = pygame.sprite.spritecollide(self.character.bullet, self.enemy_list, True)
                for self.bullet in self.bullet_list:
                    self.bullet.update()
            if self.enemy_melee_timer == 0:
                for i in self.enemy_melee_hit_list:
                    i.kill


                # Check the list of collisions.
                for enemy_ranged in self.enemy_melee_hit_list:
                    self.score += 1
                    print(self.score)
                    # You can do something with "block" here.

            temp_character_x = self.character.rect.x
            temp_character_y = self.character.rect.y
            self.character.update(self.speed_x, self.speed_y)

            wall_hit_list = pygame.sprite.spritecollide(self.character, self.wall_list, False)
            player_enemy_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_list, False)
            player_collectable_hit_list = pygame.sprite.spritecollide(self.character, self.collectable_list, False)
            enemy_melee_hit_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_melee_hit_list, False)
            enemy_bullet_hit_list = (pygame.sprite.spritecollide(self.character, self.enemy_bullet_list, False))

            if player_enemy_hit_list:
                self.character.health -= 5
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y
            if wall_hit_list:
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y
            if player_collectable_hit_list:
                player_collectable_hit_list[0].kill()
                self.score += 10
            if enemy_melee_hit_hit_list:
                    self.character.health -= 5
                    enemy_melee_hit_hit_list[0].kill()
            if enemy_bullet_hit_list:
                    self.character.health -= 5
                    enemy_bullet_hit_list[0].kill()

            if len(self.enemy_list) == 0:
                self.game_over = True

            if self.enemy_timer == 0:
                for self.enemy_ranged in self.enemy_ranged_list:
                    self.enemy_ranged.shoot(self.character.rect.centerx, self.character.rect.centery)
                    self.enemy_bullet_list.add(self.enemy_ranged.enemy_bullet)
                    self.all_sprites_list.add(self.enemy_ranged.enemy_bullet)
                    self.enemy_timer = 433

            if self.enemy_timer == 0:
                for self.enemy_melee in self.enemy_melee_list:
                    self.enemy_melee.hit()
                    self.enemy_melee_hit_list.add(self.enemy_melee.enemy_melee_hit)
                    self.all_sprites_list.add(self.enemy_melee.enemy_melee_hit)
                    self.enemy_melee_timer = 50

            for self.enemy_bullet in self.enemy_bullet_list:
                self.enemy_bullet.update()

            #self.invincibility_timer -=1
            self.enemy_timer -= 1
            self.enemy_melee_timer -= 1

            self.pointer.update()

            #22.02.2021 - adding game over for health
            if self.character.health <= 0:
                self.game_over = True

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
        # if self.bullet_list:
        # print(self.character.bullet.bullet_target.x, self.character.bullet.bullet_target.y, self.character.bullet.rect.center)

        health_text = pygame.freetype.SysFont("Arial", 30)
        health_display, _ = health_text.render("Health = " + str(self.character.health), BLACK)
        screen.blit(health_display, (50, 1050))

        score_text = pygame.freetype.SysFont("Arial", 30)
        score_display, _ = score_text.render("Score = " + str(self.score), BLACK)
        screen.blit(score_display, (300, 1050))

        if self.test == 1:
            print(self.lvlmap)
            self.test = 0

        pygame.display.flip()

    def map_replace(self, x, y, target):
        self.lvlmap_replace = self.lvlmap[int(y)]
        self.lvlmap_replace_list = list(self.lvlmap_replace)

        self.lvlmap_replace_list[int(x)] = target
        self.lvlmap_replace = "".join(self.lvlmap_replace_list)
        self.lvlmap[int(y)] = self.lvlmap_replace

    def map_checker(self,x,y,target):
        self.lvlmap_replace = self.lvlmap[int(y)]
        self.lvlmap_replace_list = list(self.lvlmap_replace)

        if self.lvlmap_replace_list[int(x)] == target:
            return True
        else:
            return False

class Title(object):

    def __init__(self, screen):
        screen.fill(BEIGE)
        # font = pygame.font.Font("Serif", 25)
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Danger Dungeon - Click to Start", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 4)
        screen.blit(text, [center_x, center_y])

        # Options
        font = pygame.font.SysFont("Calibri", 50)
        text = font.render("Options", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 - ((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        #Creating Sprite Lists
        self.all_sprites_list = pygame.sprite.Group()
        self.textbox_title_list = pygame.sprite.Group()
        self.textbox_options_list = pygame.sprite.Group()

        #Creating Title Box
        self.textbox_title = TextBox_Title(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        #Below is commented out so text box is invisible
        #self.all_sprites_list.add(self.textbox_title)
        self.textbox_title_list.add(self.textbox_title)

        #Creating Options Box
        self.textbox_options = TextBox_Options(SCREEN_WIDTH // 2, (1080 - SCREEN_HEIGHT // 4))
        # Below is commented out so text box is invisible
        self.all_sprites_list.add(self.textbox_options)
        self.textbox_options_list.add(self.textbox_options)

        #Creating Pointer
        self.pointertitle = PointerTitle(960, 540)
        self.all_sprites_list.add(self.pointertitle)

        #Music
        pygame.mixer.init()
        pygame.mixer.music.load("Title.mp3")
        pygame.mixer.music.play(-1)


        pygame.display.flip()



    def process_events(self, screen):

        screen.fill(BEIGE)
        # Title
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Danger Dungeon - Click to Start", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 4)
        screen.blit(text, [center_x, center_y])

        #Options
        font = pygame.font.SysFont("Calibri", 50)
        text = font.render("Options", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 -((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        self.pointertitle.update()
        self.all_sprites_list.draw(screen)
        pygame.display.flip()

        title_click_list = pygame.sprite.spritecollide(self.pointertitle, self.textbox_title_list, False)
        options_click_list = pygame.sprite.spritecollide(self.pointertitle, self.textbox_options_list, False)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if title_click_list:
                    return True
                elif options_click_list:
                    Title.options(screen)
                else:
                    return False
                
    def options(self, screen):
        screen.fill(BEIGE)
        # Title
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Danger Dungeon - Click to Start", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 4)
        screen.blit(text, [center_x, center_y])

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

    #Title Screen
    title = Title(screen)
    start = False
    while not start:
        start = title.process_events(screen)


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
