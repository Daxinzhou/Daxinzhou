import pygame
import sys
from game_screen import GameScreen
from menu import Menu
from end_screen import EndScreen
from utils import load_image,load_music

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Looking for Griffin kids")
        self.clock = pygame.time.Clock()  # 初始化 clock 属性
        self.current_screen = GameScreen(self)  # 传入 self 参数以便访问 clock
        # 加载资源
        self.background = load_image('background.jpg')
        # 加载背景音乐
        load_music('resources/sounds/background_music.ogg')
        pygame.mixer.music.play(-1)  # 循环播放背景音乐

        # 游戏状态
        self.state = 'menu'
        self.menu = Menu(self)
        self.game_screen = GameScreen(self)
        self.end_screen = EndScreen(self)
    
    def change_screen(self, screen_name):
        if screen_name == 'end_screen':
            self.current_screen = EndScreen(self)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == 'menu':
                    self.menu.handle_event(event)
                elif self.state == 'game':
                    self.game_screen.handle_event(event)
                elif self.state == 'end':
                    self.end_screen.handle_event(event)

            self.screen.fill((0, 0, 0))
            
            if self.state == 'menu':
                self.menu.update()
                self.menu.draw()
            elif self.state == 'game':
                self.game_screen.update()
                self.game_screen.draw()
                if self.game_screen.score > 100:
                    self.state = 'end'  # 当得分超过100分时切换到结束界面
            elif self.state == 'end':
                self.end_screen.update()
                self.end_screen.draw()

            pygame.display.flip()
            clock.tick(60)
