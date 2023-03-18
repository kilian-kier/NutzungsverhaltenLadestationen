import datetime
import pygame
from simulation.constants import *
from simulation.charger import Charger
from simulation.global_variables import GlobalVariables


class SimulationScreen:
    def __init__(self, screen, cars):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 20)
        self.cars = cars
        self.clock = pygame.time.Clock()

    def draw(self):
        running = True
        hour = 0
        minute = 0
        second = 0
        clock_speedup = 10  # how many times faster the clock runs
        while running:
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill self.screen.with white color
            self.screen.fill((0, 100, 0))

            # update clock
            second += clock_speedup
            if second >= 60:
                second -= 60
                minute += 1
            if minute >= 60:
                minute -= 60
                hour += 1
            if hour >= 24:
                hour = 0

            # draw titel
            font_titel = pygame.font.SysFont('Arial', 36, bold=True)
            titel = font_titel.render(f'Hypercharger Simulation', True, (0, 0, 0))
            titel_rect = titel.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
            self.screen.blit(titel, titel_rect)

            # draw clock
            time_str = f'Uhrzeit  {hour:02d}:{minute:02d}:{second:02d}'
            clock_text = self.font.render(time_str, True, WHITE)
            self.screen.blit(clock_text, (WIDTH - 150, 10))

            # draw road
            pygame.draw.rect(self.screen, BLACK,
                             (ROAD_X, ROAD_Y, ROAD_WIDTH, ROAD_HEIGHT))
            Charger(CHARGER_X, CHARGER_Y).draw(self.screen, self.font)

            # draw Ges Auto Counter
            counter_text = self.font.render(f'Gesamt Autos: {GlobalVariables.ges_autos}', True, (255, 255, 255))
            self.screen.blit(counter_text, (10, 10))

            # draw Ges KWH Counter
            counter_text = self.font.render(f'Geladene Energie: {GlobalVariables.ges_kWh} kWh', True, (255, 255, 255))
            counter_text_rect = counter_text.get_rect(center=(WIDTH // 2, 20))
            self.screen.blit(counter_text, counter_text_rect)

            # draw Ges Dauer Prozent
            counter_text = self.font.render(f'Gesamt Dauer: {GlobalVariables.ges_dauer} min', True, (255, 255, 255))
            self.screen.blit(counter_text, (10, 30))

            # update and draw cars
            for car in self.cars:
                car.move(hour, minute, second, self.cars, GlobalVariables.lock, self.screen)

                if datetime.time(hour, minute, second) >= datetime.time(23, 58, 0):
                    GlobalVariables.fertig = True
                # update display

                if not self.cars:
                    running = False
                break
            pygame.display.update()

            # tick clock
            self.clock.tick(60)
