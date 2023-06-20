import pygame as py
import random
from pygame import mixer
from movements import player_walk_right, player_walk_left, enemy_walk_right, enemy_walk_left

py.init()
mixer.music.load('sounds/teddy.mp3')
mixer.music.play(-1)

# Game related constants (**EDIT ON OWN RISK**).
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 480
RED = (0xFF, 0, 0)
GREEN = (0, 0x7F, 0)
BLUE = (0, 0, 0xFF)
BLACK = (0, 0, 0)
WHITE = (0xFF, 0xFF, 0xFF)
PLAYER_FRAME_LIMIT = 27
ENEMY_FRAME_LIMIT = 33
BULLETS_LIMIT = 3
enemy_bullets_limit = 1
BULLETS_COLOR = BLACK
JUMP_LIMIT = 8
ENEMY_HEALTH = 10
PLAYER_HEALTH = 30
PLAYER_SPEED = 5
ENEMY_SPEED = 3
SPRITE_SIZE = 64
LIFE_TIMER = 600
GAME_FONT = 'optimattc'

# Game related variables.
score = 0
hiscore = 0
lives = 5
level = 1
speed = 3
player_dead = False
life_visible = True
life_x = 150
life_y = 280
life_wait_timer = 1
life_hitbox = (life_x + 2, life_y + 2, 24, 24)
player_life_hitbox = (life_x + 2, life_y + 2, 24, 24)
life_taken = False
pause = False

# Initialize game section.
game_screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("ድንበርህን አስከብር")
clock = py.time.Clock()

background_platform = py.image.load('images/monut.jpg')
player_life = py.image.load('images/shield1.jpg')
sword_image = py.image.load("./images/javelin.png")


# Player class with all attributes related to player.
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = PLAYER_SPEED
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_limit = JUMP_LIMIT
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = PLAYER_HEALTH

    def draw(self, game_screen):
        if self.walk_count + 1 >= PLAYER_FRAME_LIMIT:
            self.walk_count = 0
        if not (self.standing):
            if self.left:
                game_screen.blit(player_walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                game_screen.blit(player_walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                game_screen.blit(player_walk_right[0], (self.x, self.y))
            else:
                game_screen.blit(player_walk_left[0], (self.x, self.y))

        py.draw.rect(game_screen, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        py.draw.rect(game_screen, GREEN, (
        self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / PLAYER_HEALTH) * (PLAYER_HEALTH - self.health)), 10))
        # self.hitbox = (self.x+17,self.y+2,31,57)  
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)


    def hit(self):
        self.is_jump = False
        self.walk_count = 0
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


# Enemy class with all attributes related to enemy.
class Enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walk_count = 0
        self.path = [self.x, self.end]
        self.speed = ENEMY_SPEED
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = ENEMY_HEALTH
        self.visible = True

    def draw(self, game_screen):
        if self.visible:
            self.move()
            if self.walk_count + 1 >= ENEMY_FRAME_LIMIT:
                self.walk_count = 0

            if self.speed > 0:
                game_screen.blit(enemy_walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                game_screen.blit(enemy_walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1

            py.draw.rect(game_screen, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            py.draw.rect(game_screen, GREEN, (
            self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / ENEMY_HEALTH) * (ENEMY_HEALTH - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.speed > 0:
            facing = 1
            projectile = Projectile((enemy_1.x + enemy_1.width // 2), round(enemy_1.y + enemy_1.height // 2), 6,
                                    BULLETS_COLOR, facing)
            if len(enemy_bullets) < enemy_bullets_limit:
                enemy_bullets.append(projectile)
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walk_count = 0
        else:
            facing = -1
            projectile = Projectile((enemy_1.x + enemy_1.width // 2), round(enemy_1.y + enemy_1.height // 2), 6,
                                    BULLETS_COLOR, facing)
            if len(enemy_bullets) < enemy_bullets_limit:
                enemy_bullets.append(projectile)
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walk_count = 0

    def hit(self, level):
        if self.health > 0:
            self.health -= 1 if level < 5 else 2
        else:
            self.visible = False


# Projectile class for bullets.
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self, game_screen):
        py.draw.circle(game_screen, self.color, (self.x, self.y), self.radius)


class Projectile2(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self, game_screen):
        game_screen.blit(sword_image, (self.x - 30 // 2, self.y - 50))

    # Method to render sprites.


def renderSprites():
    global life_wait_timer, life_taken, life_x, life_y, life_hitbox, life_visible

    game_screen.blit(background_platform, (0, 0))

    # logo_font = py.font.SysFont(GAME_FONT,30,True,True)

    font = py.font.SysFont(GAME_FONT, 20, True, True)

    score_text = font.render('Score ' + str(score), 1, BLUE)
    game_screen.blit(score_text, (340, 0))

    # Draw player/enemies/bullets on every frame.
    player.draw(game_screen)

    if level < 5:
        enemy_1.draw(game_screen)
    elif level >= 5 and level < 10:
        enemies = [enemy_1, enemy_2]
        for enemy in enemies:
            enemy.draw(game_screen)
    elif level >= 10:
        enemies = [enemy_1, enemy_2, enemy_3]
        for enemy in enemies:
            enemy.draw(game_screen)

    for bullet in bullets:
        bullet.draw(game_screen)

    for bullet in enemy_bullets:
        # time.sleep(1)
        bullet.draw(game_screen)

    # Get new positon for life if taken.
    if life_taken:
        life_x = random.randint(0, SCREEN_WIDTH - 50)
        life_y = random.randint(280, SCREEN_HEIGHT - 70)
        life_taken = False
        life_visible = False
    else:
        life_wait_timer += 1

        # Wait till life wait timer loop ends after draw new life.
    if not life_taken and life_wait_timer % LIFE_TIMER == 0:
        life_visible = True

    if life_visible:
        game_screen.blit(player_life, (life_x, life_y))

    life_hitbox = (life_x + 2, life_y + 2, 24, 24)
    py.display.update()


# Method to detect collision between enemy/player/bullet/life.
def collisionDetection(enemy, bullets):
    global score, lives, level, life_taken
    # Player and life collision detection.
    if player.hitbox[1] < life_hitbox[1] + life_hitbox[3] and player.hitbox[1] + player.hitbox[3] > life_hitbox[1]:
        if player.hitbox[0] + player.hitbox[2] > life_hitbox[0] and player.hitbox[0] < life_hitbox[0] + life_hitbox[2]:
            if life_visible:
                player.health = PLAYER_HEALTH
                lives += 1
                life_taken = True
                life_up = mixer.Sound('sounds/life_up.wav')
                life_up.play()

                # Enemy and bullet collision detection.
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[
                2]:
                if enemy.visible:
                    enemy_hit = mixer.Sound('sounds/enemy_bullet_hit.mp3')
                    enemy_hit.play()
                    enemy.hit(level)
                    score += 1
                    bullets.remove(bullet)

        # Remove bullets from screen.           
        if bullet.x < SCREEN_WIDTH and bullet.x > 0:
            bullet.x += bullet.speed

        else:
            bullets.remove(bullet)
    # Player and enemy bullets collision detection
    for bullet in enemy_bullets:
        if bullet.y - bullet.radius < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.radius > player.hitbox[
            1]:
            if bullet.x + bullet.radius > player.hitbox[0] and bullet.x - bullet.radius < player.hitbox[0] + \
                    player.hitbox[2]:
                # if enemy.visible:
                enemy_hit = mixer.Sound('sounds/enemy_bullet_hit.mp3')
                enemy_hit.play()
                player.hit()
                score += 1
                enemy_bullets.remove(bullet)

        if bullet.x < SCREEN_WIDTH and bullet.x > 0:
            bullet.x += bullet.speed

        else:
            enemy_bullets.remove(bullet)


# Method to respawn enemies.
def respawnEnemy(enemy):
    enemy_collided = False
    py.time.delay(1000)
    enemy.health = ENEMY_HEALTH
    enemy.visible = True
    enemy.x = random.randint(0, SCREEN_WIDTH - 50)


# Main method for game.
if __name__ == '__main__':

    # Creating player and enemies instances.
    player = Player(300, 370, SPRITE_SIZE, SPRITE_SIZE)
    enemy_1 = Enemy(0, 380, SPRITE_SIZE, SPRITE_SIZE, SCREEN_WIDTH - 50)
    enemy_2 = Enemy(100, 380, SPRITE_SIZE, SPRITE_SIZE, SCREEN_WIDTH - 50)
    enemy_3 = Enemy(200, 380, SPRITE_SIZE, SPRITE_SIZE, SCREEN_WIDTH - 50)
    bullets = []
    enemy_bullets = []
    shoot_loop = 0
    reset_speed = True
    running = True
    pause_freq = 0

    # Main game loop.
    while running:
        clock.tick(PLAYER_FRAME_LIMIT)

        # Game over section - reset all variables and constants.
        if player.health <= 0:
            # Reset variables.
            hiscore = (score + 5) if score > hiscore else hiscore
            lives = 5
            score = 0
            level = 1
            speed = 3
            BULLETS_LIMIT = 5
            LIFE_TIMER = 600
            player.health = PLAYER_HEALTH
            enemy_1.health = ENEMY_HEALTH
            enemy_1.speed = ENEMY_SPEED
            player.speed = PLAYER_SPEED
            enemy_1.visible = True

            # Print game over text and load music.
            game_end = py.image.load('images/teshenfehal.png')
            next_game = py.image.load('images/enter.png')

            game_over_font = py.font.SysFont('arial', 40, True, True)
            game_over_text = game_over_font.render('Game Over (Press ENTER Key)', 1, RED)
            game_screen.blit(game_end, (250, 150))
            game_screen.blit(next_game, (200, 190))
            game_over = mixer.Sound('sounds/game_over.mp3')
            game_over.play()

            # Remove bullets from screen.
            for bullet in bullets:
                bullets.remove(bullet)

            for bullet in enemy_bullets:
                enemy_bullets.remove(bullet)

            # Update display and delay.
            py.display.update()
            pause = True

            # Application quit event.
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        # Shooting limit range.
        if shoot_loop > 0:
            shoot_loop += 1
        if shoot_loop > 3:
            shoot_loop = 0

            # Respawn new enemy and check collision.
        if level < 5:
            if not enemy_1.visible and enemy_1.health == 0:
                respawnEnemy(enemy_1)
                enemy_1.speed = abs(enemy_1.speed) + 1
                level += 1
                speed = abs(enemy_1.speed)
            collisionDetection(enemy_1, bullets)
        elif level >= 5 and level < 10:
            enemies = [enemy_1, enemy_2]
            if level == 5 and reset_speed:
                enemy_1.speed = enemy_2.speed = speed = ENEMY_SPEED
                BULLETS_LIMIT = 7
                LIFE_TIMER = 400
                player.speed += 2
                reset_speed = False
            if level == 9:
                reset_speed = True

            if not enemy_1.visible and not enemy_2.visible and enemy_1.health == 0 and enemy_2.health == 0:
                for enemy in enemies:
                    respawnEnemy(enemy)
                    enemy.speed = abs(enemy.speed) + 1
                    speed = abs(enemy.speed)
                level += 1

            for enemy in enemies:
                collisionDetection(enemy, bullets)

            # Bug fix for life taken because of multiple detection.
            # PERMANENT-FIX-TO-DO : Move Player-Life Detection code here.
            if life_taken:
                lives -= 1

        elif level >= 10:
            enemies = [enemy_1, enemy_2, enemy_3]
            if level == 10 and reset_speed:
                enemy_1.speed = enemy_2.speed = enemy_3.speed = speed = ENEMY_SPEED
                player.speed += 3
                BULLETS_LIMIT = 10
                LIFE_TIMER = 200
                reset_speed = False
            if not enemy_1.visible and not enemy_2.visible and not enemy_3.visible and enemy_1.health == 0 and enemy_2.health == 0 and enemy_3.health == 0:

                for enemy in enemies:
                    respawnEnemy(enemy)
                    enemy.speed = abs(enemy.speed) + 1
                    speed = abs(enemy.speed)
                level += 1

            for enemy in enemies:
                collisionDetection(enemy, bullets)

            if life_taken:
                lives -= 2

                # Get the key pressed
        keys = py.key.get_pressed()

        # Bullet spawn section.
        if keys[py.K_SPACE] and shoot_loop == 0:
            # bullet = mixer.Sound('sounds/bullet.mp3')
            # bullet.play()
            facing = -1 if player.left else 1
            projectile = Projectile2((player.x + player.width // 2), round(player.y + player.height // 1.15), 6,BULLETS_COLOR, facing)

            if len(bullets) < BULLETS_LIMIT:
                bullets.append(projectile)
            shoot_loop = 1

        if keys[py.K_RETURN]:
            pause = not pause
            pause_on = mixer.Sound('sounds/pause_on.mp3')
            pause_on.play()
            pause_freq += 1

        if pause_freq % 2 == 0 and pause_freq > 0:
            pause_off = mixer.Sound('sounds/pause_off.mp3')
            pause_off.play(1)
            pause_freq = 1

        # Moving section of player.
        if keys[py.K_LEFT] and player.x > player.speed:
            player.x -= player.speed
            player.left = True
            player.right = False
            player.standing = False
        elif keys[py.K_RIGHT] and player.x < SCREEN_WIDTH - player.width - player.speed:
            player.x += player.speed
            player.right = True
            player.left = False
            player.standing = False

        else:
            player.standing = True
            player.walk_count = 0

        # Jump section of player.
        if not (player.is_jump):
            if keys[py.K_UP]:
                player_jump = mixer.Sound('sounds/zeraf.mp3')
                player_jump.play()
                player.is_jump = True
                player.right = False
                player.left = False
                player.walk_count = 0
        else:
            if player.jump_limit >= -JUMP_LIMIT:
                player.y -= (player.jump_limit * abs(player.jump_limit)) / 2
                player.jump_limit -= 1
            else:
                player.is_jump = False
                player.jump_limit = JUMP_LIMIT

        if not pause:
            # Render sprites on every frame.
            renderSprites()

    py.quit()
