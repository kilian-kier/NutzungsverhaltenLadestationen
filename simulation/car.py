import datetime
import random
import pygame
from simulation.global_variables import GlobalVariables
from simulation.constants import *


class Car:
    def __init__(self, x, spawntime, duration, batteryStart, batteryEnd, power, pos):
        self.x = x
        positions = [ROAD_Y + 10, ROAD_Y + 80]
        self.y = positions[pos]
        self.speed = 4
        self.batteryStart = batteryStart
        self.battery = self.batteryStart
        self.batteryEnd =  batteryEnd
        self.spawnTime = spawntime  # Ankunftszeit
        self.power = power  # KWH
        self.duration = duration.total_seconds()/60
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.is_charging = False

    def move(self, hour, minute, second, cars, lock, screen):
        if datetime.time(hour, minute, second) < self.spawnTime and not GlobalVariables.fertig:
            # wait until spawn time is reached
            return

        if self.x >= WIDTH - CAR_WIDTH:
            lock.acquire()
            try:
                cars.remove(self)
            finally:
                lock.release()

            return

        self.draw(screen)

        if not self.is_charging:

            self.x += self.speed
            if CHARGER_X + CHARGER_WIDTH / 2 - CAR_WIDTH / 2 <= self.x <= CHARGER_X + CHARGER_WIDTH / 2 + CAR_WIDTH / 2:
                self.is_charging = True
        else:
            if self.battery < self.batteryEnd:
                self.battery += 1
            else:
                self.is_charging = False

        if self.battery == self.batteryEnd:
            GlobalVariables.ges_autos += 1
            GlobalVariables.ges_kWh += self.power
            GlobalVariables.ges_dauer += self.duration
            self.batteryEnd = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))
        font = pygame.font.Font(None, 25)
        text = font.render(str(self.battery) + "%", True, WHITE)
        screen.blit(text, (self.x, self.y - 20))