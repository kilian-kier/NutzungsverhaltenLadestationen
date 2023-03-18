import importlib


def run_simulation():
    main = importlib.import_module('simulation.main')
    main.main()


if __name__ == '__main__':
    run_simulation()
