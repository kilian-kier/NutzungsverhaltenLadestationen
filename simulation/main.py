import datetime
import threading
import pygame
from simulation.constants import *
import simulation.simulation_lib as lib
from simulation.start_screen import StartScreen
from simulation.loading_screen import LoadingScreen
from simulation.simulation_screen import SimulationScreen
from simulation.summary_screen import SummaryScreen
from simulation.car import Car


def main():
    pygame.init()

    # create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hypercharger Simulator')

    # create clock
    clock = pygame.time.Clock()

    start_screen = StartScreen(screen)
    amount = start_screen.draw()

    random_values = []
    generate_thread = threading.Thread(target=lib.random_generator, args=(amount, random_values))
    generate_thread.start()

    loading_screen = LoadingScreen(screen, generate_thread)
    loading_screen.draw()

    cars = list()
    random_times = list()
    generate_thread.join()

    for i, r in enumerate(random_values):
        print('Auto ', i + 1)
        lib.print_values(r)
        print()

    for i in range(amount):
        startZeit = random_values[i][0]
        fahrzeit = datetime.timedelta(minutes=18)  # delay dass Auto bei Ankunftszeit bei Zapfsäule
        startZeit_effektiv = (datetime.datetime.combine(datetime.date.today(), startZeit) - fahrzeit).time()

        dauer = random_values[i][1]  # Damit bei Ankuftzeit bereits bei Zapfsäule
        batteryStart = int(round(random_values[i][2], 2) * 100)
        batteryEnd = batteryStart + int(round(random_values[i][3], 2) * 100)
        kwh = round(random_values[i][4] / 1000)
        # neue_zeit = (datetime.datetime.combine(datetime.date.today(), zeit) + dauer).time()

        pos = i % 2
        cars.append(
            Car(0, spawntime=startZeit_effektiv, duration=dauer, batteryStart=batteryStart, batteryEnd=batteryEnd,
                power=kwh, pos=pos))

    simulation_screen = SimulationScreen(screen, cars)
    simulation_screen.draw()

    summary_screen = SummaryScreen(screen)
    summary_screen.draw()

    # quit pygame
    pygame.quit()
