from random import choice, randint
from pygame import *
import sys

init()
font.init()
font1 = font.SysFont("Impact", 100)
font2 = font.SysFont("Impact", 50)
game_over_text = font1.render("GAME OVER", True, (150, 0, 0))
mixer.init()
mixer.music.load('mus.mp3')
# mixer.music.play()
mixer.music.set_volume(0.2)
bullet_sound = mixer.Sound("blat.wav")
bullet_sound.set_volume(0.5)


screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
FPS = 90
clock = time.Clock()

bg = image.load('road_0.png')
bg = transform.scale(bg, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

player_img = image.load("car.png")
enemy_img = image.load("Audi.png")
bullet_img = image.load("taxi.png")
all_sprites = sprite.Group()


class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)


class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.score = 0
        self.speed = 2
        self.bg_speed = 2
        self.max_speed = 30

    

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w]:
            if self.rect.y > 300:
                self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.1
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            if self.bg_speed > 2:
                self.bg_speed -= 0.2

        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        enemy_collide = sprite.spritecollide(
            self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100


class Enemy(Sprite):
    def __init__(self, sprite_img, width, height):
        rand_x = randint(0, WIDTH-width)
        super().__init__(sprite_img, width, height, rand_x, -200)
        self.damage = 100
        self.speed = 4
        enemys.add(self)

    def update(self):
        self.rect.y += player.bg_speed + 2
        if self.rect.y > HEIGHT:
            self.kill()





player = Player(player_img, 100, 70, 300, 300)
enemys = sprite.Group()
enemy1 = Enemy(enemy_img, 80, 60)

score_text = font2.render(f"Score:{player.score}", True, (255, 255, 255))

start_time = time.get_ticks()
enemy_spawn_time = time.get_ticks()
spawn_interval = randint(500, 3500)
run = True
finish = False

start_screen = True
start_text = font2.render(f"PRESS ANY KEY TO START", True, (255, 255, 255))
restart_text = font2.render(f"PRESS R TO RESTART", True, (255, 255, 255))



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if start_screen:
                start_screen = False
            if e.key == K_ESCAPE:
                run = False
                sys.exit()

            
            if finish and e.key == K_r:
                finish = False
                for s in all_sprites:
                    s.kill()
                player = Player(player_img, 100, 70, 300, 300)
                score_text = font2.render(f"Score:{player.score}", True, (255, 255, 255))


    window.blit(bg, (0, bg_y1))
    window.blit(bg, (0, bg_y2))

    if start_screen:
        window.blit(start_text, (WIDTH/2 - start_text.get_width()/2,
                                 HEIGHT/2 - start_text.get_height()/2))
    else:

        bg_y1 += player.bg_speed
        bg_y2 += player.bg_speed

        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT

        if player.hp <= 0:
            finish = True

        now = time.get_ticks()  # отримуємо поточний час
        if now - enemy_spawn_time > spawn_interval:  # якщо від появи останнього ворога пройшло більше 1с
            rand_k = randint(1, 3)
            for i in range(rand_k):
                enemy1 = Enemy(enemy_img, 80, 60)  # створюємо нового ворога

            enemy_spawn_time = time.get_ticks()  # оновлюємо час появи ворога
            spawn_interval = randint(500, 3000)

      

        collide_list = sprite.spritecollide(
            player, enemys, True, sprite.collide_mask)
        if len(collide_list) > 0:
            finish = True

        all_sprites.draw(window)
        window.blit(score_text, (30, 30))

        if not finish:
            all_sprites.update()
        if finish:
            window.blit(game_over_text,
                        (WIDTH/2 - game_over_text.get_width()/2,
                         HEIGHT/2 - game_over_text.get_height()/2))

            window.blit(restart_text,
                        (WIDTH/2 - restart_text.get_width()/2,
                        HEIGHT/2 - restart_text.get_height()/2 + 100))
            
    display.update()
    clock.tick(FPS)
