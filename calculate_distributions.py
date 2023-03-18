import argparse
import numpy as np
import pandas as pd
from fitter import Fitter, get_distributions
import matplotlib.pyplot as plt
import scipy.stats as st


def calculate(dataset, column):
    data = dataset[column].values
    fitter = Fitter(data, distributions=get_distributions())
    fitter.fit()

    best_dist = fitter.get_best()
    name = list(best_dist.keys())[0]
    params = list(best_dist.values())[0]

    dist = getattr(st, name)

    x = np.linspace(min(0, min(fitter.x)), max(fitter.x), 10000)
    y = dist.pdf(x, *params.values())
    plt.hist(data, bins='auto', density=True)
    plt.xlim(min(0, min(fitter.x)), max(fitter.x))
    plt.plot(x, y)
    plt.title(name)
    print('Beste Verteilung: ', name, ': ', params)
    plt.show()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('excel_dataset', type=str, help='Path to the Excel input file')
    arg_parser.add_argument('column', type=str, help='Column name for which the distribution should be calculated')
    args = arg_parser.parse_args()

    print('Reading data ...')
    dataset = pd.read_excel(args.excel_dataset)
    if args.column not in dataset.keys():
        print(f'{args.column} is not a column in {args.excel_dataset}')

    print(f'Successfully read {dataset.size}')

    print("Searching for the best distribution")

    calculate(dataset, args.column)


if __name__ == '__main__':
    main()
