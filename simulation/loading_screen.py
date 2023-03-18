import pygame
from simulation.constants import *


class LoadingScreen:
    def __init__(self, screen, thread):
        self.screen = screen
        self.thread = thread

    def draw(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if not self.thread.is_alive():
                running = False

            self.screen.fill(BACKGROUND)
            text = 'Daten werden generiert ...'
            font = pygame.font.Font(None, 30)
            loading_text = font.render(text, True, (0, 0, 0))
            loading_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(loading_text, loading_rect)
            pygame.display.update()
