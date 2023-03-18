import pygame
from simulation.constants import *


class Charger:
    def __init__(self, x, y, size=(100, 40), color=(0, 0, 255)):
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        charger_text = font.render(f'Ladesäule', True, (255, 255, 255))
        charger_text_rect = charger_text.get_rect(
            center=(CHARGER_X + CHARGER_WIDTH / 2, CHARGER_Y + CHARGER_HEIGHT * 2))
        screen.blit(charger_text, charger_text_rect)
