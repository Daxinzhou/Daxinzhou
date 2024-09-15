import pygame
import sys

class Menu:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0  # 0 是开始游戏，1 是退出游戏
        self.options = ['Start Game', 'Quit Game']
        self.font = pygame.font.SysFont(None, 48)
        self.button_color = (255, 255, 255)
        self.button_highlight_color = (255, 0, 0)
        self.button_border_color = (0, 0, 0)
        self.button_hover_color = (0, 255, 0)
        self.button_width = 190
        self.button_height = 120
        self.button_margin = 25

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    self.game.state = 'game'
                elif self.selected_option == 1:
                    pygame.quit()
                    sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for index, option in enumerate(self.options):
                button_rect = pygame.Rect(
                    self.button_margin,
                    self.button_margin + index * (self.button_height + self.button_margin),
                    self.button_width,
                    self.button_height
                )
                if button_rect.collidepoint(mouse_pos):
                    if index == 0:
                        self.game.state = 'game'
                    elif index == 1:
                        pygame.quit()
                        sys.exit()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            button_rect = pygame.Rect(
                self.button_margin,
                self.button_margin + index * (self.button_height + self.button_margin),
                self.button_width,
                self.button_height
            )
            if button_rect.collidepoint(mouse_pos):
                self.selected_option = index

    def draw(self):
        self.game.screen.blit(self.game.background, (0, 0))

        # 绘制选项
        for index, option in enumerate(self.options):
            button_rect = pygame.Rect(
                self.button_margin,
                self.button_margin + index * (self.button_height + self.button_margin),
                self.button_width,
                self.button_height
            )

            # 绘制按钮背景
            pygame.draw.rect(self.game.screen, self.button_highlight_color if index == self.selected_option else self.button_color, button_rect)

            # 绘制按钮边框
            pygame.draw.rect(self.game.screen, self.button_border_color, button_rect, 2)

            # 绘制按钮上的文本
            text = self.font.render(option, True, (0, 0, 0))  # 黑色文本
            text_rect = text.get_rect(center=button_rect.center)
            self.game.screen.blit(text, text_rect)  # 居中对齐

        pygame.display.flip()  # 更新屏幕显示
    


