import pygame

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Title')

colors = {
  'black': (0, 0, 0),
  'white': (255, 255, 255),
  'red': (255, 0, 0),
  'green': (0, 255, 0),
  'blue': (0, 0, 255)
}

def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

font40 = pygame.font.Font('ProximaNova/ProximaNova-Bold.ttf', 40)

run = True

class Screen:
    def run(self):
        pass

    def handle_event(self, event):
        pass


class MenuScreen(Screen):
    def __init__(self):
        self.bg_img = pygame.transform.scale(load_image('bg_menu.png', pygame.Color('white')), (width, height))
        self.texts = (
          font40.render('Start Game', 0, colors['white']),
          font40.render('How To Play', 0, colors['white']),
          font40.render('Exit', 0, colors['white'])
        )
        
        self.game_title_text = font40.render('Brother\'s destruction', 0, colors['white'])

        self.wc = width // 2
        self.w = 300
        self.h = 50
        self.x = self.wc - self.w // 2
        self.button_rects = (
          (self.x, 200, self.w, self.h),
          (self.x, 300, self.w, self.h),
          (self.x, 400, self.w, self.h),
        )
        
        self.text_rects = tuple(
          self.texts[i].get_rect(center=(self.wc, self.button_rects[i][1] + self.h // 2)) for i in range(3)
        )

    def run(self):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.game_title_text, self.game_title_text.get_rect(center=(self.wc, 20)))
        for i in range(3):
            pygame.draw.rect(screen, colors['blue'], self.button_rects[i])
            screen.blit(self.texts[i], self.text_rects[i])
        
    def handle_event(self, event):
        global run
        global screen_num
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            h = 50
            by = [b[1] for b in self.button_rects]
            if abs(x - self.wc) < self.w // 2:
                if by[0] <= y < by[0] + h: # start game
                    screen_num = 2
                elif by[1] <= y < by[1] + h: # how to play
                    screen_num = 1
                elif by[2] <= y < by[2] + h: # exit
                    run = False

class HowToPlayScreen(Screen):
    def __init__(self):
        self.bg_img = pygame.transform.scale(load_image('bg_menu.png', pygame.Color('white')), (width, height))

        texts1 = (
          'Player1:',
          'Move: A D',
          'Attack: R T',
          'Ult: F',
        )
        texts2 = (
          'Player2:',
          'Move: K ;',
          'Attack: I U',
          'Ult: J'
        )
        self.text1 = tuple(font40.render(s, 0, colors['white']) for s in texts1)
        self.text2 = tuple(font40.render(s, 0, colors['white']) for s in texts2)

        self.btn_texts = (
          font40.render('Start Game', 0, colors['white']),
          font40.render('Exit', 0, colors['white'])
        )
        self.wc = width // 2
        self.w = 300
        self.h = 50
        self.x = self.wc - self.w // 2
        self.button_rects = (
          (self.x, 550, self.w, self.h),
          (self.x, 650, self.w, self.h),
        )

        self.btn_text_rects = tuple(
          self.btn_texts[i].get_rect(center=(self.wc, self.button_rects[i][1] + self.h // 2)) for i in range(2)
        )

    def run(self):
        screen.blit(self.bg_img, (0, 0))
        y = 50
        for t in self.text1:
            screen.blit(t, (20, y))
            y += 100

        y = 50
        for t in self.text2:
            screen.blit(t, (self.wc + 20, y))
            y += 100

        for i in range(2):
            pygame.draw.rect(screen, colors['blue'], self.button_rects[i])
            screen.blit(self.btn_texts[i], self.btn_text_rects[i])

    def handle_event(self, event):
        global run
        global screen_num
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            h = 50
            by = [b[1] for b in self.button_rects]
            if abs(x - self.wc) < self.w // 2:
                if by[0] <= y < by[0] + h: # start game
                    screen_num = 2
                elif by[1] <= y < by[1] + h: # exit
                    run = False

class SelectPlayerScreen(Screen):
    def __init__(self):
        self.bg_img = pygame.transform.scale(load_image('bg_menu.png', pygame.Color('white')), (width, height))
        self.ava1 = pygame.transform.scale(load_image('chr1/avatar.png', pygame.Color('white')), (250, 250))
        self.ava2 = pygame.transform.scale(load_image('chr2/avatar.png', pygame.Color('white')), (250, 250))

    def run(self):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.ava1, (50, 50))
        screen.blit(self.ava2, (width - 300, 50))

    def handle_event(self, event):
        global screen_num
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 < y < 300:
                if 50 < x < 300:
                    screens[4].set_first_player(1)
                    screen_num = 3
                elif width - 300 < x < width - 50:
                    screens[4].set_first_player(2)
                    screen_num = 3

class SelectBgScreen(Screen):
    def __init__(self):
        self.bg_img = pygame.transform.scale(load_image('bg_menu.png', pygame.Color('white')), (width, height))
        self.bg_size = (256, 192)
        self.gap = 72
        self.bg_variants = (
            pygame.transform.scale(load_image('bg/Screenshot_3.png',  pygame.Color('white')), self.bg_size),
            pygame.transform.scale(load_image('bg/Screenshot_4.png',  pygame.Color('white')), self.bg_size),
            pygame.transform.scale(load_image('bg/Screenshot_5.png',  pygame.Color('white')), self.bg_size),
            pygame.transform.scale(load_image('bg/Screenshot_6.png',  pygame.Color('white')), self.bg_size),
            pygame.transform.scale(load_image('bg/Screenshot_7.png',  pygame.Color('white')), self.bg_size),
            pygame.transform.scale(load_image('bg/Screenshot_8.png',  pygame.Color('white')), self.bg_size)
        )
        

    def run(self):
        screen.blit(self.bg_img, (0, 0))
        x = 20
        y = 20
        for img in self.bg_variants:
            screen.blit(img, (x, y))
            x += self.bg_size[0] + self.gap
            if x >= (self.bg_size[0] + self.gap) * 3 + 20:
                x = 20
                y += self.bg_size[1] + self.gap


    def handle_event(self, event):
        global screen_num
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 20 < y < self.bg_size[1] + 20:
                screens[4].set_bg((x - 20) // (self.bg_size[0] + self.gap))
                screen_num = 4
            elif self.bg_size[1] + 20 + self.gap < y < self.bg_size[1] * 2 + 20 + self.gap:
                screens[4].set_bg(3 + (x - 20) // (self.bg_size[0] + self.gap))
                screen_num = 4

class BattleScreen(Screen):
    def __init__(self):
        self.player1 = None
        self.player2 = None

        self.imgs = (
          'bg/Screenshot_3.png',
          'bg/Screenshot_4.png',
          'bg/Screenshot_5.png',
          'bg/Screenshot_6.png',
          'bg/Screenshot_7.png',
          'bg/Screenshot_8.png',
        )
        self.bg_img = None

    def run(self):
        screen.blit(self.bg_img, (0, 0))
        self.player1.update()
        self.player2.update()
        self.player1.draw()
        self.player2.draw()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player1.set_moving_left()
            elif event.key == pygame.K_d:
                self.player1.set_moving_right()
            elif event.key == pygame.K_r:
                self.player1.attack1()
            elif event.key == pygame.K_t:
                self.player1.attack2()
            elif event.key == pygame.K_f:
                self.player1.ult()
            elif event.key == pygame.K_k:
                self.player2.set_moving_left()
            elif event.key == pygame.K_SEMICOLON:
                self.player2.set_moving_right()
            elif event.key == pygame.K_i:
                self.player2.attack1()
            elif event.key == pygame.K_u:
                self.player2.attack2()
            elif event.key == pygame.K_j:
                self.player2.ult()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                self.player1.set_idle()
            elif event.key in (pygame.K_k, pygame.K_COLON):
                self.player2.set_idle()

    def set_first_player(self, n):
        if n == 1:
            self.player1 = Player1(left=True)
            self.player2 = Player2(left=False)
        else:
            self.player1 = Player2(left=True)
            self.player2 = Player1(left=False)
        self.player1.set_enemy(self.player2)
        self.player2.set_enemy(self.player1)

    def set_bg(self, n):
        self.bg_img = pygame.transform.scale(load_image(self.imgs[n]), (width, height))


class Player:
    def __init__(self, left):
        self.is_first_player = left
        self.w = 120
        self.h = 250
        if left:
            self.x = 100
        else:
            self.x = width - 100 - self.w
        self.y = 400
        self.idle_left_img = None
        self.idle_right_img = None
        self.attack1_left_sprite = None
        self.attack1_right_sprite = None
        self.attack2_left_sprite = None
        self.attack2_right_sprite = None
        self.run_left_sprite = None
        self.run_right_sprite = None
        self.ult_left_sprite = None
        self.ult_right_sprite = None
        self.avatar_img = None
        self.state = 'idle'
        self.left = left
        self.moving_left = False
        self.moving_right = False
        self.max_hp = 100
        self.hp = 100
        self.max_ult = 100
        self.ult_points = 0
        self.attack_success = False
        self.speed = 15
        self.active_animation = None
        self.ulting_left = None

    def set_enemy(self, enemy):
        self.enemy = enemy

    def set_moving_left(self):
        if self.state == 'idle':
            self.state = 'run'
            if self.left:
                self.active_animation = self.run_left_sprite
            else:
                self.active_animation = self.run_right_sprite
            self.active_animation.start()
        self.moving_left = True

    def set_moving_right(self):
        if self.state == 'idle':
            self.state = 'run'
            if self.left:
                self.active_animation = self.run_left_sprite
            else:
                self.active_animation = self.run_right_sprite
            self.active_animation.start()
        self.moving_right = True

    def set_idle(self):
        if self.state == 'run':
            self.state = 'idle'
            self.active_animation.stop()
            self.active_animation = None
        self.moving_left = False
        self.moving_right = False

    def attack1(self):
        if self.state in ('idle', 'run'):
            self.state = 'attack1'
            self.attack_success = False
            if self.left:
                self.active_animation = self.attack1_left_sprite
            else:
                self.active_animation = self.attack1_right_sprite
            self.active_animation.start()

    def attack2(self):
        if self.state in ('idle', 'run'):
            self.state = 'attack2'
            self.attack_success = False
            if self.left:
                self.active_animation = self.attack2_left_sprite
            else:
                self.active_animation = self.attack2_right_sprite
            self.active_animation.start()

    def ult(self):
        if self.state in ('idle', 'run') and self.ult_points == self.max_ult:
            self.state = 'ult'
            self.attack_success = False
            self.ult_points = 0
            if self.left:
                self.active_animation = self.ult_left_sprite
            else:
                self.active_animation = self.ult_right_sprite
            self.active_animation.start()
            self.ulting_left = self.left

    def update(self):
        change_left = self.left != (self.enemy.x > self.x)
        if change_left:
            self.left = not self.left
            if self.active_animation:
                self.active_animation.stop()
        if self.state == 'run':
            if change_left:
                if self.left:
                    self.active_animation = self.run_left_sprite
                else:
                    self.active_animation = self.run_right_sprite
                self.active_animation.start()
            if self.moving_left:
                self.x = max(self.x - self.speed, 0)
            else:
                self.x = min(self.x + self.speed, width - self.w)
        elif self.state in ('attack1', 'attack2'):
            if self.active_animation.is_ended():
                self.state = 'idle'
            elif not self.attack_success:
                if self.enemy.x - self.w < self.x < self.enemy.x + self.enemy.w:
                    self.attack_success = True
                    self.enemy.hp = max(self.enemy.hp - 5, 0)
                    self.ult_points = min(self.ult_points + 10, self.max_ult)
        elif self.state == 'ult':
            if self.active_animation.is_ended():
                self.is_ulting = False
                self.state = 'idle'
            elif not self.attack_success:
                if self.enemy.x - self.w < self.x < self.enemy.x + self.enemy.w:
                    self.attack_success = True
                    self.enemy.hp = max(self.enemy.hp - 25, 0)
                    self.ulting()

    def draw(self):
        if self.is_first_player:
            xhp, yhp, whp, hhp = 20, 20, 200, 40
            xult, yult, wult, hult = 20, 65, 200, 40
        else:
            xhp, yhp, whp, hhp = width - 220, 20, 200, 40
            xult, yult, wult, hult = width - 220, 65, 200, 40
        pygame.draw.rect(screen, colors['white'], (xhp, yhp, whp, hhp))
        pygame.draw.rect(screen, colors['red'], (xhp + 2, yhp + 2, (whp - 4) * (self.hp / self.max_hp), hhp - 4))
        pygame.draw.rect(screen, colors['white'], (xult, yult, wult, hult))
        pygame.draw.rect(screen, colors['green'], (xult + 2, yult + 2, (wult - 4) * (self.ult_points / self.max_ult), hult - 4))

        if self.state == 'idle':
            if self.left:
                screen.blit(self.idle_left_img, (self.x, self.y))
            else:
                screen.blit(self.idle_right_img, (self.x, self.y))
        elif self.state == 'attack1':
            if self.left:
                screen.blit(self.attack1_left_sprite.img(), (self.x, self.y))
            else:
                screen.blit(self.attack1_right_sprite.img(), (self.x, self.y))
        elif self.state == 'attack2':
            if self.left:
                screen.blit(self.attack2_left_sprite.img(), (self.x, self.y))
            else:
                screen.blit(self.attack2_right_sprite.img(), (self.x, self.y))
        elif self.state == 'run':
            if self.left:
                screen.blit(self.run_left_sprite.img(), (self.x, self.y))
            else:
                screen.blit(self.run_right_sprite.img(), (self.x, self.y))
        elif self.state == 'ult':
            if self.left:
                screen.blit(self.ult_left_sprite.img(), (self.x, self.y))
            else:
                screen.blit(self.ult_right_sprite.img(), (self.x, self.y))


class Player1(Player):
    def __init__(self, left):
        super(Player1, self).__init__(left)
        self.idle_left_img = pygame.transform.scale(load_image('chr1/1.PNG',  pygame.Color('white')), (self.w, self.h))
        self.idle_right_img = pygame.transform.flip(self.idle_left_img, True, False)
        
        a1_frames=(
          pygame.transform.scale(load_image('chr1/atack1/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/atack1/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/atack1/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/atack1/4.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.attack1_left_sprite = AnimatedSprite(frames=a1_frames, duration=800, cyclic=False)
        a1_frames_r = tuple(pygame.transform.flip(img, True, False) for img in a1_frames)
        self.attack1_right_sprite = AnimatedSprite(frames=a1_frames_r, duration=800, cyclic=False)

        a2_frames=(
          pygame.transform.scale(load_image('chr1/atack2/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/atack2/2.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.attack2_left_sprite = AnimatedSprite(frames=a2_frames, duration=600, cyclic=False)
        a2_frames_r = tuple(pygame.transform.flip(img, True, False) for img in a2_frames)
        self.attack2_right_sprite = AnimatedSprite(frames=a2_frames_r, duration=600, cyclic=False)

        ult_frames=(
          pygame.transform.scale(load_image('chr1/ult.PNG',  pygame.Color('white')), (self.w, self.h)),
        )
        self.ult_left_sprite = AnimatedSprite(frames=ult_frames, duration=600, cyclic=False)
        ult_frames_r = tuple(pygame.transform.flip(img, True, False) for img in ult_frames)
        self.ult_right_sprite = AnimatedSprite(frames=ult_frames_r, duration=600, cyclic=False)
        
        run_frames=(
          pygame.transform.scale(load_image('chr1/run/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/run/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/run/4.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr1/run/5.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.run_left_sprite = AnimatedSprite(frames=run_frames, duration=800, cyclic=True)
        run_frames_r = tuple(pygame.transform.flip(img, True, False) for img in run_frames)
        self.run_right_sprite = AnimatedSprite(frames=run_frames_r, duration=800, cyclic=True)

        self.avatar_img = pygame.transform.scale(load_image('chr1/avatar.png',  pygame.Color('white')), (100, 100))
        
        self.ult_left = None

    def ulting(self):
        if self.ulting_left:
            self.x = min(self.x + 30, width - self.w)
        else:
            self.x = max(self.x - 30, 0)

class Player2(Player):
    def __init__(self, left):
        super(Player2, self).__init__(left)
        self.idle_right_img = pygame.transform.scale(load_image('chr2/1.PNG',  pygame.Color('white')), (self.w, self.h))
        self.idle_left_img = pygame.transform.flip(self.idle_right_img, True, False)
        
        a1_frames=(
          pygame.transform.scale(load_image('chr2/atack1/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/atack1/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/atack1/3.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.attack1_left_sprite = AnimatedSprite(frames=a1_frames, duration=800, cyclic=False)
        a1_frames_r = tuple(pygame.transform.flip(img, True, False) for img in a1_frames)
        self.attack1_right_sprite = AnimatedSprite(frames=a1_frames_r, duration=800, cyclic=False)

        a2_frames=(
          pygame.transform.scale(load_image('chr2/atack2/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/atack2/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/atack2/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/atack2/4.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.attack2_left_sprite = AnimatedSprite(frames=a2_frames, duration=1200, cyclic=False)
        a2_frames_r = tuple(pygame.transform.flip(img, True, False) for img in a2_frames)
        self.attack2_right_sprite = AnimatedSprite(frames=a2_frames_r, duration=1200, cyclic=False)
        
        ult_frames=(
          pygame.transform.scale(load_image('chr2/ult1/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult1/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult1/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult1/4.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult2/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult2/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult2/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/ult2/4.PNG',  pygame.Color('white')), (self.w, self.h)),
        )
        self.ult_left_sprite = AnimatedSprite(frames=ult_frames, duration=1600, cyclic=False)
        ult_frames_r = tuple(pygame.transform.flip(img, True, False) for img in ult_frames)
        self.ult_right_sprite = AnimatedSprite(frames=ult_frames_r, duration=1600, cyclic=False)
        
        run_frames=(
          pygame.transform.scale(load_image('chr2/run/1.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/run/2.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/run/3.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/run/4.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/run/5.PNG',  pygame.Color('white')), (self.w, self.h)),
          pygame.transform.scale(load_image('chr2/run/6.PNG',  pygame.Color('white')), (self.w, self.h))
        )
        self.run_left_sprite = AnimatedSprite(frames=run_frames, duration=1200, cyclic=True)
        run_frames_r = tuple(pygame.transform.flip(img, True, False) for img in run_frames)
        self.run_right_sprite = AnimatedSprite(frames=run_frames_r, duration=1200, cyclic=True)

        self.avatar_img = pygame.transform.scale(load_image('chr2/avatar.png',  pygame.Color('white')), (100, 100))

    def ulting(self):
        pass

class AnimatedSprite:
    def __init__(self, frames, duration, cyclic):
        self.frames = frames
        self.duration = duration / len(frames)
        self.start_time = None
        self.cyclic = cyclic
        self.ended = None

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.ended = False

    def stop(self):
        self.start_time = None
        self.ended = True

    def is_ended(self):
        return self.ended

    def img(self):
        dt = pygame.time.get_ticks() - self.start_time
        if not self.cyclic and dt > self.duration * len(self.frames):
            self.stop()
        return self.frames[int(dt / self.duration) % len(self.frames)]


screens = (
  MenuScreen(),
  HowToPlayScreen(),
  SelectPlayerScreen(),
  SelectBgScreen(),
  BattleScreen(),
)
screen_num = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            screens[screen_num].handle_event(event)

    screens[screen_num].run()

    pygame.time.delay(15)
    pygame.display.flip()

pygame.quit()