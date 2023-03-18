import pygame
from simulation.constants import *


class StartScreen:
    running = True
    amount = 0

    cursor_timer = 0
    cursor_visible = True

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 25)
        self.title_text = self.font.render('Gib die Anzahl der zu generierenden Autos an und drück dann ENTER', True,
                                           (0, 0, 0))

    def draw(self):
        while self.running:
            dt = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.amount
                    elif event.key == pygame.K_BACKSPACE:
                        self.amount //= 10
                    elif event.unicode.isdigit():
                        self.amount *= 10
                        self.amount += int(event.unicode)

            self.screen.fill(BACKGROUND)

            amount_text = self.font.render(str(self.amount), True, (0, 0, 0))
            amount_rect = amount_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            if self.amount > 0:
                self.screen.blit(amount_text, amount_rect)

            title_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
            self.screen.blit(self.title_text, title_rect)

            self.cursor_timer += dt / 1000.0
            if self.cursor_timer >= 0.5:
                self.cursor_timer -= 0.5
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (amount_rect.right + 1, amount_rect.top + 6, 2, amount_rect.height - 10))

            pygame.display.flip()
