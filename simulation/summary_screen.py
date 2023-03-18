import pygame
from simulation.global_variables import GlobalVariables
from simulation.constants import *


class SummaryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 30)
        self.font_titel = pygame.font.SysFont('Arial', 36, bold=True)
        self.titel = self.font_titel.render(f'Zusammenfassung', True, (0, 0, 0))
        self.gesAutos = self.font.render(f'Gesamt Autos: {GlobalVariables.ges_autos}', True, (0, 0, 0))
        self.gesDauer = self.font.render(f'Gesamt Aufladedauer: {GlobalVariables.ges_dauer} min', True, (0, 0, 0))
        self.gesKWH = self.font.render(f'Zählerstand: {GlobalVariables.ges_kWh} kWh', True, (0, 0, 0))

    def draw(self):
        # get text surfaces' rects
        titel_rect = self.titel.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        autos_rect = self.gesAutos.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        dauer_rect = self.gesDauer.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        kwh_rect = self.gesKWH.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        # draw text surfaces onto screen
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.titel, titel_rect)
        self.screen.blit(self.gesAutos, autos_rect)
        self.screen.blit(self.gesDauer, dauer_rect)
        self.screen.blit(self.gesKWH, kwh_rect)

        # update screen
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
