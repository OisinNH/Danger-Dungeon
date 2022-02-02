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
BG = (145, 176, 154)
GREY = (128, 128, 128)
PURPLE = (139, 0, 139)
BULLET_TRAVEL = 5
PLAYER_CHARACTER_1 = pygame.image.load("Player_Character_1.png")
PLAYER_CHARACTER_2= pygame.image.load("Player_Character_2.png")
PLAYER_CHARACTER_3 = pygame.image.load("Player_Character_3.png")
AMMO_SPRITE = pygame.image.load("ammo.png")
COLLECTABLE_SPRITE = pygame.image.load("collectable.png")
ENEMY_MELEE_SPRITE = pygame.image.load("melee.png")
ENEMY_RANGED_SPRITE = pygame.image.load("ranged.png")
ENEMY_BOSS_SPRITE = pygame.image.load("boss.png")
VOLUME_DOWN = pygame.image.load("volumedown.png")
VOLUME_UP = pygame.image.load("volumeup.png")

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
    def __init__(self, game):
        super().__init__()
        self.image = ENEMY_RANGED_SPRITE
        self.game = game
        self.ranged = True

    def shoot(self, target_x, target_y):
        if not self.game.cannot_see(self.game.wall_list, self.rect.centerx, self.rect.centery, self.game.character.rect.x, self.game.character.rect.y):
            self.enemy_bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            return True
        else:
            return False

    def update(self):
        pass
        # self.rect.x += 0
        # self.shoot(game)


    def move(self):
        if not self.game.cannot_see(self.game.wall_list, self.rect.centerx, self.rect.centery, self.game.character.rect.x, self.game.character.rect.y):
            if self.rect.x > self.game.character.rect.x:
                self.rect.x -= 0.5
            else:
                self.rect.x += 1
            if self.rect.y > self.game.character.rect.y:
                self.rect.y -= 0.5
            else:
                self.rect.y += 1


class EnemyMelee(Enemy):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_MELEE_SPRITE

    def hit(self):
        self.enemy_melee_hit = EnemyMelee_Hit(self.rect.centerx, self.rect.centery)


class EnemyBoss(EnemyRanged): #Create Boss class and tutorial screen
    def __init__(self, game):
        super().__init__(game)
        self.image = ENEMY_BOSS_SPRITE
        self.rect = self.image.get_rect()
        self.health = 1000


class EnemyMelee_Hit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([0, 0])
        #self.image.fill(RED)
        self.rect = pygame.Rect(0, 0, 60, 60)
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


class TextBox_Back(TextBox):
    def __init__(self,x ,y):
        super().__init__(x, y)
        self.image = pygame.Surface([250, 160])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class VolumeDown(TextBox):
    def __init__(self,x ,y):
        super().__init__(x, y)
        self.image = VOLUME_DOWN
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class VolumeUp(TextBox):
    def __init__(self,x ,y):
        super().__init__(x, y)
        self.image = VOLUME_UP
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
        self.ammo = 20

    def shoot(self, target_x, target_y):
        if self.ammo > 0:
            self.bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            self.ammo -= 1

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Character_1(Character):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_CHARACTER_1
        self.health = 200
        self.attack_modifier = 0.8


class Character_2(Character):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_CHARACTER_2
        self.health = 70
        self.attack_modifier = 1.2


class Character_3(Character):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_CHARACTER_3
        self.health = 300
        self.attack_modifier = 0.1


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
        self.image = COLLECTABLE_SPRITE
        self.rect = self.image.get_rect()


class Collectable_Ammo(Collectable):
    def  __init__(self):
        super().__init__()
        self.image = AMMO_SPRITE


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(PURPLE)
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


class character_select_image(pygame.sprite.Sprite):
    def __init__(self, x, y, character):
        super().__init__()
        self.image = pygame.image.load(character)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.top = y

        print(character)


class Game:
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self, screen, room, level, character):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.room = room
        self.level = level
        self.character_number = character
        self.new_level_timer =  0
        self.all_sprites_list = pygame.sprite.Group()
        self.start(self.room, self.level, character)

    def start(self, room, level, character_start):
        if self.all_sprites_list:
            for i in self.all_sprites_list:
                i.kill()
        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.enemy_list = pygame.sprite.Group()
        self.enemy_ranged_list = pygame.sprite.Group()
        self.enemy_melee_list = pygame.sprite.Group()
        self.enemy_boss_list =pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.collectable_list = pygame.sprite.Group()
        self.collectable_ammo_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.enemy_melee_hit_list = pygame.sprite.Group()
        self.portal_list = pygame.sprite.Group()

        self.level_file = "lvl"
        self.level_file = self.level_file + str(level) + str(room) + ".txt"
        print(self.level_file)

        # map file read
        with open(self.level_file, 'r') as file:
            # written to a list
            self.lvlmap = file.readlines()

        # Making Outside walls
        self.test = 1
        for x in range(1881):
            if x % 40 == 0:

                wall_x = x / 20
                wall_y = 0

                if self.map_checker(wall_x, wall_y, "/"):
                    self.wall = Wall(x, 0)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y, "w")
                    self.map_replace(wall_x + 1, wall_y, "w")
                    self.map_replace(wall_x, wall_y + 1, "w")
                    self.map_replace(wall_x + 1, wall_y + 1, "w")

                wall_y = 52

                if self.map_checker(wall_x, wall_y, "/"):
                    self.wall = Wall(x, 1040)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y, "w")
                    self.map_replace(wall_x + 1, wall_y, "w")
                    self.map_replace(wall_x, wall_y + 1, "w")
                    self.map_replace(wall_x + 1, wall_y + 1, "w")

                # self.lvlmap[x//20] = "O"
                # self.lvlmap[(x // 20 )+ 1] = "O"
                # self.lvlmap[(x // 20) + 96] = "O"
                # self.lvlmap[(x // 20) + 1 + 96] = "O"

                # self.lvlmap[x//20 + 96*52] = "O"
                # self.lvlmap[(x // 20 + 96 * 52) + 96] = "O"
                # self.lvlmap[(x // 20 + 96 * 52)+ 1] = "O"
                # self.lvlmap[(x // 20 + 96 * 52) + 1 + 96] = "O"

        for y in range(1041):
            if y % 40 == 0:

                wall_x = 0
                wall_y = y / 20

                if self.map_checker(wall_x, wall_y, "/"):
                    self.wall = Wall(0, y)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y, "w")
                    self.map_replace(wall_x + 1, wall_y, "w")
                    self.map_replace(wall_x, wall_y + 1, "w")
                    self.map_replace(wall_x + 1, wall_y + 1, "w")

                wall_x = 95

                if self.map_checker(wall_x, wall_y, "/"):
                    self.wall = Wall(1880, y)
                    self.wall_list.add(self.wall)
                    self.all_sprites_list.add(self.wall)

                    self.map_replace(wall_x, wall_y, "O")
                    self.map_replace(wall_x + 1, wall_y, "O")
                    self.map_replace(wall_x, wall_y + 1, "O")
                    self.map_replace(wall_x + 1, wall_y + 1, "O")

                # if self.lvlmap[(y//20)*96] == "_":
                # self.lvlmap[(y//20)*96] = "O"
                # self.lvlmap[((y // 20) * 96) + 1] = "O"
                # self.lvlmap[((y // 20) * 96) + 96] = "O"
                # self.lvlmap[((y // 20) * 96) + 1 + 96] = "O"

                # self.lvlmap[95 + (y//20) * 96] = "O"
                # self.lvlmap[(95 + (y // 20) * 96) + 1] = "O"
                # self.lvlmap[(95 + (y // 20) * 96) + 96] = "O"
                # self.lvlmap[(95 + (y // 20) * 96) + 1 + 96] = "O"
        # for x in range(1881):
        # if x % 40 == 0:
        #  r = random.randint(20)
        # if r == 0

        # Create the block sprites
        # Creating Ranged Enemies

        #Creating Ranged Enemies

        # Create Walls
        for x in range(1881):
            for y in range(1041):
                if x % 40 == 0:
                    if y % 40 == 0:
                        pu_x = x // 20
                        pu_y = y // 20

                        # checking the entity map
                        if self.map_checker(pu_x, pu_y, "w"):
                            # if self.lvlmap[(x//20) + (y//20*96)] != "_":
                            self.wall = Wall(x, y)
                            self.wall_list.add(self.wall)
                            self.all_sprites_list.add(self.wall);

        #adding boss
        if self.room == 2:
            self.enemy_boss = EnemyBoss(self)
            self.enemy_list.add(self.enemy_boss)
            self.enemy_boss_list.add(self.enemy_boss)
            self.all_sprites_list.add(self.enemy_boss)
            self.enemy_boss.rect.x = 820
            self.enemy_boss.rect.y = 95

            eb_x = 820 // 20
            eb_y = 95 // 20

            for i in range(15):
                for x in range (10):
                    self.map_replace(eb_x + i, eb_y + x, "B")

        # creating ranged enemies
        for i in range(5):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            er_x = x // 20
            er_y = y // 20

            # checking the entity map
            if not self.map_checker(er_x, er_y, "/"):
                # if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                enemy_ranged = EnemyRanged(self)
                enemy_ranged.rect.x = x
                enemy_ranged.rect.y = y

                self.enemy_list.add(enemy_ranged)
                self.all_sprites_list.add(enemy_ranged)
                self.enemy_ranged_list.add(enemy_ranged)

                self.map_replace(er_x, er_y, "r")
                self.map_replace(er_x + 1, er_y, "r")
                self.map_replace(er_x, er_y + 1, "r")
                self.map_replace(er_x + 1, er_y + 1, "r")
                # self.lvlmap[(x//20) + (y//20 * 96)] = "er"

        # creating meelee enemies
        for i in range(5):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            em_x = x // 20
            em_y = y // 20

            # checking the entity map
            if not self.map_checker(em_x, em_y, "/") and not self.map_checker(em_x + 1, em_y, "/") and not self.map_checker(em_x, em_y + 1, "/") and not self.map_checker(em_x + 1, em_y + 1, "/") :
                # if self.lvlmap[(x//20) + (y//20*96)] != "_":
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
                # self.lvlmap[(x//20) + (y//20 * 96)] = "em"

        # Creating Collectables
        for i in range(3):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            pu_x = x // 20
            pu_y = y // 20

            # checking the entity map
            if not self.map_checker(pu_x, pu_y, "/") and not self.map_checker(pu_x + 1, pu_y, "/") and not self.map_checker(pu_x, pu_y + 1, "/") and not self.map_checker(pu_x + 1, pu_y + 1, "/"):
                # if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                # self.lvlmap[(x//20) + (y//20 * 96)] = "pu"
                self.collectable = Collectable()

                self.collectable.rect.x = x
                self.collectable.rect.y = y

                self.collectable_list.add(self.collectable)
                self.all_sprites_list.add(self.collectable)

                self.map_replace(pu_x, pu_y, "c")
                self.map_replace(pu_x + 1, pu_y, "c")
                self.map_replace(pu_x, pu_y + 1, "c")
                self.map_replace(pu_x + 1, pu_y + 1, "c")

        #Creating Ammo Collectables
        for i in range(3):

            x = random.randrange(40, 1861)
            y = random.randrange(40, 1021)

            pu_x = x // 20
            pu_y = y // 20

            # checking the entity map
            if not self.map_checker(pu_x, pu_y, "/") and not self.map_checker(pu_x + 1, pu_y, "/") and not self.map_checker(pu_x, pu_y + 1, "/") and not self.map_checker(pu_x + 1, pu_y + 1, "/"):
                # if self.lvlmap[(x//20) + (y//20*96)] != "_":
                i -= 1
            else:
                # self.lvlmap[(x//20) + (y//20 * 96)] = "pu"
                self.collectable_ammo = Collectable_Ammo()

                self.collectable_ammo.rect.x = x
                self.collectable_ammo.rect.y = y

                self.collectable_list.add(self.collectable_ammo)
                self.collectable_ammo_list.add(self.collectable_ammo)
                self.all_sprites_list.add(self.collectable_ammo)

                self.map_replace(pu_x, pu_y, "a")
                self.map_replace(pu_x + 1, pu_y, "a")
                self.map_replace(pu_x, pu_y + 1, "a")
                self.map_replace(pu_x + 1, pu_y + 1, "a")

        # Creating Portal
        for x in range(1881):
            if x % 40 == 0:
                for y in range(1041):
                    if y % 40 == 0:
                        po_x = x / 20
                        po_y = y / 20
                        # checking the entity map
                        if self.map_checker(po_x, po_y, "p"):
                            self.portal = Portal(x, y)
                            self.portal_list.add(self.portal)
                            self.all_sprites_list.add(self.portal)

        # Create the player
        # Choosing the subclass
        if character_start == 1:
            self.character = Character_1()
        elif character_start == 2:
            self.character = Character_2()
        elif character_start == 3:
            self.character = Character_3()


        self.all_sprites_list.add(self.character)
        # Create Player Speed
        self.speed_x = 0
        self.speed_y = 0

        # Create Pointer
        self.pointer = Pointer(960, 540)
        self.all_sprites_list.add(self.pointer)



        self.enemy_timer = 0  # Temporary thing for enemies shooting - should remove soon
        self.enemy_melee_timer = 0 #timer for the melee enmies hitting the player

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.start(1, 1, self.character_number)
                else:
                    self.character.shoot(self.pointer.rect.centerx, self.pointer.rect.centery)
                    self.bullet_list.add(self.character.bullet)
                    self.all_sprites_list.add(self.character.bullet)
            # Player movement
            if event.type == pygame.KEYDOWN and self.new_level_timer == 0:
                if event.key == pygame.K_d:
                    self.speed_x += 5
                if event.key == pygame.K_a:
                    self.speed_x -= 5
                if event.key == pygame.K_w:
                    self.speed_y -= 5
                if event.key == pygame.K_s:
                    self.speed_y += 5
            # Removing the movement when letting go
            if event.type == pygame.KEYUP and self.new_level_timer == 0:
                if event.key == pygame.K_d:
                    self.speed_x -= 5
                if event.key == pygame.K_a:
                    self.speed_x += 5
                if event.key == pygame.K_w:
                    self.speed_y += 5
                if event.key == pygame.K_s:
                    self.speed_y -= 5

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            # self.all_sprites_list.update()
            # self.enemy_melee_timer = 0
            if self.enemy_bullet_list:
                for self.wall in self.wall_list:
                    #Kill any bullets if they come into contact with a wall
                    pygame.sprite.spritecollide(self.wall, self.enemy_bullet_list, True)
            if self.bullet_list:
                for self.wall in self.wall_list:
                    #Kill any bullets if they come into contact with a wall
                    pygame.sprite.spritecollide(self.wall, self.bullet_list, True)
                # See if the player's bullet has collided with anything.
                pygame.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True)
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
            portal_hit_list = pygame.sprite.spritecollide(self.character, self.portal_list, False)
            player_enemy_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_list, False)
            player_collectable_hit_list = pygame.sprite.spritecollide(self.character, self.collectable_list, False)
            player_collectable_ammo_hit_list = pygame.sprite.spritecollide(self.character, self.collectable_ammo_list, False)
            enemy_melee_hit_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_melee_hit_list, False)
            enemy_bullet_hit_list = pygame.sprite.spritecollide(self.character, self.enemy_bullet_list, False)

            if player_enemy_hit_list:
                self.character.health -= 5
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y
            if wall_hit_list:
                self.character.rect.x = temp_character_x
                self.character.rect.y = temp_character_y
            "ranged enemy movement"
            for self.ranged_enemy in self.enemy_ranged_list:
                "notes current enemy coords"
                self.temp_enemy_ranged_x =self.ranged_enemy.rect.x
                self.temp_enemy_ranged_y = self.ranged_enemy.rect.y

                "move the enemy"
                self.ranged_enemy.move()

                "checking if the enemy collides with a wall"
                if pygame.sprite.spritecollide(self.ranged_enemy, self.wall_list, False):
                    self.ranged_enemy.rect.x = self.temp_enemy_ranged_x
                    self.ranged_enemy.rect.y = self.temp_enemy_ranged_y

            #boss movement
            for enemy_boss in self.enemy_boss_list:
                "notes current enemy coords"
                self.temp_enemy_boss_x = enemy_boss.rect.x
                self.temp_enemy_boss_y = enemy_boss.rect.y

                "move the enemy"
                enemy_boss.move()

                "checking if the enemy collides with a wall"
                if pygame.sprite.spritecollide(enemy_boss, self.wall_list, False):
                    self.ranged_enemy.rect.x = self.temp_enemy_boss_x
                    self.ranged_enemy.rect.y = self.temp_enemy_boss_y

            if player_collectable_ammo_hit_list:
                self.character.ammo += 10
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
                # self.game_over = True
                # add animation for the door opening
                if portal_hit_list:
                    # add amimation for loading new room
                    for i in self.all_sprites_list:
                        i.kill()
                    if self.room < 6:
                        self.room += 1
                        self.start(self.room, self.level, self.character_number)
                        self.new_level_timer = 432
                    elif self.room == 6:
                        if self.level < 4:
                            self.level = 1
                            self.start(self.room, self.level)
                        elif self.level == 4:
                            self.game_over = True

            if self.enemy_timer == 0:
                for enemy_ranged in self.enemy_ranged_list:
                    if enemy_ranged.shoot(self.character.rect.centerx, self.character.rect.centery):
                        self.enemy_bullet_list.add(enemy_ranged.enemy_bullet)
                        self.all_sprites_list.add(enemy_ranged.enemy_bullet)
                self.enemy_timer = 433
            if self.enemy_timer == 433 or self.enemy_timer == 300 or self.enemy_timer == 200 or self.enemy_timer == 100 or self.enemy_timer == 70:
                for enemy_boss in self.enemy_boss_list:
                    if enemy_boss.shoot(self.character.rect.centerx, self.character.rect.centery):
                        self.enemy_bullet_list.add(enemy_boss.enemy_bullet)
                        self.all_sprites_list.add(enemy_boss.enemy_bullet)

            if self.enemy_melee_timer == 0:
                if self.enemy_melee_hit_list:
                    for enemy_melee in self.enemy_melee_list:
                        enemy_melee.enemy_melee_hit.kill()
                self.enemy_melee_timer = 144

            if self.enemy_melee_timer == 144:
                for enemy_melee in self.enemy_melee_list:
                    enemy_melee.hit()
                    self.enemy_melee_hit_list.add(enemy_melee.enemy_melee_hit)
                    self.all_sprites_list.add(enemy_melee.enemy_melee_hit)

            for enemy_bullet in self.enemy_bullet_list:
                enemy_bullet.update()

            # self.invincibility_timer -=1
            self.enemy_timer -= 1
            self.enemy_melee_timer -= 1

            self.pointer.update()



            # 22.02.2021 - adding game over for health
            if self.character.health <= 0:
                self.game_over = True

            #timer to ensure that controls aren't registered for 3 seconds after a new level so that the  character can move
            if self.new_level_timer > 0:
                self.new_level_timer -= 1

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BG)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)
            #pygame.draw.aaline(screen, GREEN, [self.character.rect.centerx, self.character.rect.centery],
                               #[self.pointer.rect.x + 20, self.pointer.rect.y + 20], 5)
            # if self.bullet_list:
            # print(self.character.bullet.bullet_target.x, self.character.bullet.bullet_target.y, self.character.bullet.rect.center)

            health_text = pygame.freetype.SysFont("Arial", 30)
            health_display, _ = health_text.render("Health = " + str(self.character.health), BLACK)
            screen.blit(health_display, (50, 1050))

            score_text = pygame.freetype.SysFont("Arial", 30)
            score_display, _ = score_text.render("Score = " + str(self.score), BLACK)
            screen.blit(score_display, (300, 1050))

            ammo_text = pygame.freetype.SysFont("Arial", 30)
            ammo_display, _ = ammo_text.render("Ammo = " + str(self.character.ammo), BLACK)
            screen.blit(ammo_display, (550, 1050))

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

    def map_checker(self, x, y, target):
        self.lvlmap_replace = self.lvlmap[int(y)]
        self.lvlmap_replace_list = list(self.lvlmap_replace)

        if self.lvlmap_replace_list[int(x)] == target:
            return True
        else:
            return False

    def cannot_see(self, checked_list, x1, y1, x2, y2):
        for checked in checked_list:
            if checked.rect.clipline(x1,y1,x2,y2):
                return True
        return False


class Title(object):

    def __init__(self, screen):

        # Adding Title background
        self.image = pygame.image.load("Title.jpg")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        # font = pygame.font.Font("Serif", 25)
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Danger Dungeon - Click to Start", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 4)
        screen.blit(text, [center_x, center_y])

        # Options
        font = pygame.font.SysFont("Calibri", 50)
        text = font.render("Options", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 - ((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        # Creating Sprite Lists
        self.all_sprites_list = pygame.sprite.Group()
        self.textbox_title_list = pygame.sprite.Group()
        self.textbox_options_list = pygame.sprite.Group()

        # Creating Title Box
        self.textbox_title = TextBox_Title(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        # Below is commented out so text box is invisible
        # self.all_sprites_list.add(self.textbox_title)
        self.textbox_title_list.add(self.textbox_title)

        # Creating Options Box
        self.textbox_options = TextBox_Options(SCREEN_WIDTH // 2, (1080 - SCREEN_HEIGHT // 4))
        # Below is commented out so text box is invisible
        # self.all_sprites_list.add(self.textbox_options)
        self.textbox_options_list.add(self.textbox_options)

        # Creating Pointer
        self.pointertitle = PointerTitle(960, 540)
        self.all_sprites_list.add(self.pointertitle)

        # Music
        pygame.mixer.init()
        pygame.mixer.music.load("Title.mp3")
        pygame.mixer.music.play(-1)

        pygame.display.flip()

    def process_events(self, screen):

        #clear the sprites list
        screen.blit(self.image, self.rect)

        # Title
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Danger Dungeon - Click to Start", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 4)
        screen.blit(text, [center_x, center_y])

        # Options
        font = pygame.font.SysFont("Calibri", 50)
        text = font.render("Options", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 - ((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        self.pointertitle.update()
        self.all_sprites_list.draw(screen)
        pygame.display.flip()

        self.title_click_list = pygame.sprite.spritecollide(self.pointertitle, self.textbox_title_list, False)
        self.options_click_list = pygame.sprite.spritecollide(self.pointertitle, self.textbox_options_list, False)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.title_click_list:
                    return 1
                elif self.options_click_list:
                    return 2
                else:
                    return 0
        return 0

    def options(self, screen):

        # Adding Title background
        self.image = pygame.image.load("Title.jpg")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        # Back button
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Back", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 - ((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        # Creating Sprite Lists
        self.textbox_back_list = pygame.sprite.Group()
        self.volume_down_list = pygame.sprite.Group()
        self.volume_up_list = pygame.sprite.Group()

        # Creating Title Box
        self.textbox_back = TextBox_Back(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        # Below is commented out so text box is invisible
        # self.all_sprites_list.add(self.textbox_back)
        self.textbox_back_list.add(self.textbox_back)

        #Creating volume down
        self.volume_down = VolumeDown(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4)
        self.all_sprites_list.add(self.volume_down)
        self.volume_down_list.add(self.volume_down)

        #Creating volume up
        self.volume_up = VolumeUp(SCREEN_WIDTH- (SCREEN_WIDTH // 3), SCREEN_HEIGHT // 4 )
        self.all_sprites_list.add(self.volume_up)
        self.volume_up_list.add(self.volume_up)

        # Creating Pointer
        #self.pointertitle = PointerTitle(960, 540)
        #self.all_sprites_list.add(self.pointertitle)

        pygame.display.flip()

    def process_events_options(self, screen):

        screen.blit(self.image, self.rect)

        # Back button
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Back", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = 1080 - ((SCREEN_HEIGHT // 4) - (text.get_height() // 4))
        screen.blit(text, [center_x, center_y])

        self.pointertitle.update()
        self.all_sprites_list.draw(screen)
        pygame.display.flip()

        self.back_click_list = pygame.sprite.spritecollide(self.pointertitle, self.textbox_back_list, False)
        self.volume_down_click_list = pygame.sprite.spritecollide(self.pointertitle, self.volume_down_list, False)
        self.volume_up_click_list = pygame.sprite.spritecollide(self.pointertitle, self.volume_up_list, False)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_click_list:
                    return False
                elif self.volume_down_click_list:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
                elif self.volume_up_click_list:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                else:
                    return True
        return False

    def character_select(self, screen):
        # Adding Title background
        self.image = pygame.image.load("Title.jpg")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        # Creating Sprite Lists
        self.all_sprites_list = pygame.sprite.Group()
        self.character_1_title_list = pygame.sprite.Group()
        self.character_2_title_list = pygame.sprite.Group()
        self.character_3_title_list = pygame.sprite.Group()

        # Character 1 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("C1", True, BLACK)
        center_x = (SCREEN_WIDTH // 3) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        # Character 1 Photo
        character_1 = character_select_image(center_x, center_y + 200, "C1.png")
        self.character_1_title_list.add(character_1)
        self.all_sprites_list.add(character_1)

        # Character 2 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("C2", True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        # Character 2 Photo
        character_2 = character_select_image(center_x, center_y + 200, "C2.png")
        self.character_2_title_list.add(character_2)
        self.all_sprites_list.add(character_2)

        # Character 3 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("C3", True, BLACK)
        center_x = SCREEN_WIDTH - ((SCREEN_WIDTH // 3) + (text.get_width() // 2))
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        # Character 3 Photo
        character_3 = character_select_image(center_x, center_y + 200, "C3.png")
        self.character_3_title_list.add(character_3)
        self.all_sprites_list.add(character_3)

        # Creating Pointer
        self.pointertitle = PointerTitle(960, 540)
        self.all_sprites_list.add(self.pointertitle)

    def character_select_processes(self, screen):
        screen.blit(self.image, self.rect)

        # Character 1 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Jerry", True, BLACK)
        center_x = (SCREEN_WIDTH // 3) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        #Character 2 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Tom", True, BLACK)
        center_x = (SCREEN_WIDTH //2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        #Character 3 Name
        font = pygame.font.SysFont("Calibri", 100)
        text = font.render("Clive", True, BLACK)
        center_x = SCREEN_WIDTH -((SCREEN_WIDTH // 3) + (text.get_width() // 2))
        center_y = (SCREEN_HEIGHT // 4) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

        self.pointertitle.update()
        self.all_sprites_list.draw(screen)
        pygame.display.flip()

        self.character_1_click_list = pygame.sprite.spritecollide(self.pointertitle, self.character_1_title_list, False)
        self.character_2_click_list = pygame.sprite.spritecollide(self.pointertitle, self.character_2_title_list, False)
        self.character_3_click_list = pygame.sprite.spritecollide(self.pointertitle, self.character_3_title_list, False)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.character_1_click_list:
                    return 1
                elif self.character_2_click_list:
                    return 2
                elif self.character_3_click_list:
                    return 3
                else:
                    return 0
        return 0


def title_Loader(screen):
    # Title Screen
    title = Title(screen)
    title_screen_page = 0
    while title_screen_page == 0:
        title_screen_page = title.process_events(screen)
        if title_screen_page == 2:
            title.options(screen)
            options_exit = False
            while options_exit == False:
                options_exit = title.process_events_options(screen)
            title.volume_down.kill()
            title.volume_up.kill()
            title_screen_page = 0

    #Choose character
    title.character_select(screen)
    character_selection = 0
    while character_selection == 0:
        character_selection = title.character_select_processes(screen)
    return character_selection


def tutorial_loader(screen):
    tutorial = Tutorial(screen)
    return tutorial.process_events()

class Tutorial(object):

    def __init__(self, screen):

        # Adding Title background
        self.image = pygame.image.load("tutorial.png")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        pygame.display.flip()

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            else:
                return False
        return False


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

    #Loading for Title Screen and Options
    character = title_Loader(screen)

    #showing tutorial screen
    tutorial_done = False
    while tutorial_done == False:
        tutorial_done = tutorial_loader(screen)

    # Create an instance of the Game class
    room = 1
    level = 1
    game = Game(screen, room, level, character)

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