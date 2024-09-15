import pygame
import sys

class EndScreen:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.state = 'game'
            self.game.game_screen.reset()

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        congrat_text = font.render("Congratulation!", True, (255, 255, 255))
        self.game.screen.blit(congrat_text, (self.game.screen.get_width() / 2 - congrat_text.get_width() / 2, self.game.screen.get_height() / 2 - congrat_text.get_height() / 2 - 40))
        
        end_text = font.render("Game Over, Hit enter to start over.", True, (255, 255, 255))
        self.game.screen.blit(end_text, (self.game.screen.get_width() / 2 - end_text.get_width() / 2, self.game.screen.get_height() / 2 - end_text.get_height() / 2))
