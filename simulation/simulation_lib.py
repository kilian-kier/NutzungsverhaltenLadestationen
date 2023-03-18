import os
from pathlib import Path

from scipy.stats import gennorm
import datetime
import pickle


class ArrivalTime:
    beta = 2.7426560592988083
    log = 48048.58035760029
    scale = 16130.745137265721

    def __init__(self):
        self.dist = gennorm(self.beta, self.log, self.scale)

    def sample(self, n=1):
        return self.dist.rvs(n)


def combine_time(time, delta):
    total_seconds = time.hour * 3600 + time.minute * 60 + time.second

    total_seconds += delta.total_seconds()

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    while hours >= 24:
        hours -= 24

    return datetime.time(int(hours), int(minutes), int(seconds))


def load_model(model_name):
    try:
        with open(model_name, 'rb') as f:
            arrival = pickle.load(f)
            return arrival
    except FileNotFoundError:
        print(f'Vine Copulas Pickel Datei "{model_name}" nicht gefunden. '
              f'Generiere eine neue Datei mit vine_copulas.py und benenne die Datei in vine_copulas.pickle um.')
        input('Drücke Enter um das Programm zu beenden.')


def random_generator(n, results, model_name='vine_copulas.pickle'):
    path = os.path.join(Path(os.path.realpath(__file__)).parent, 'vine_copulas.pickle')
    model = load_model(path)
    arrival = ArrivalTime()
    time_periods = []

    i = 0
    while i < n:
        tmp = model.sample(1).iloc[0].tolist()
        tmp.insert(0, arrival.sample())

        neg = False
        for t in tmp:
            if t < 0:
                neg = True
                break

        if neg:
            continue

        # int(...) to remove milliseconds
        arrival_delta = datetime.timedelta(seconds=int(tmp[0]))
        arrival_time = (datetime.datetime.min + arrival_delta).time()
        tmp[0] = arrival_time

        duration_delta = datetime.timedelta(minutes=int(tmp[1]))
        tmp[1] = duration_delta

        end_time = combine_time(arrival_time, duration_delta)

        overlaps = 0
        for period in time_periods:
            if (period[0] < arrival_time < period[1]) or (period[0] < end_time < period[1]):
                overlaps += 1

        if overlaps >= 2:
            continue

        time_periods.append([arrival_time, end_time])
        time_periods = sorted(time_periods, key=lambda x: x[0])

        if tmp[2] + tmp[3] > 1:
            tmp[3] = 1 - tmp[2]

        if tmp[4] <= 0:
            continue

        results.append(tmp)
        i += 1

    if len(results) != n:
        print(results)

    results.sort()


def print_values(values):
    print(f'{values[0]} - {combine_time(values[0], values[1])} ({int(values[1].total_seconds() / 60)} min)')
    print(f'{int(values[2] * 100)}% - {min(100, int((values[2] + values[3]) * 100))}% ({int(values[3] * 100)}%)')
    print(f'{int(values[4] / 1000)}kWh')
