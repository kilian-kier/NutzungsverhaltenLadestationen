import argparse
import pandas as pd
import pickle
from copulas.multivariate import VineCopula


def store_model(model, name):
    with open(f'{name}.pickle', 'wb') as f:
        pickle.dump(model, f)


def generate_vine_copulas(dataset, output_name, sample_number):
    nparray = dataset.dropna().sample(sample_number)

    regular = VineCopula('regular')
    center = VineCopula('center')
    direct = VineCopula('direct')

    print('Fitting regular vine copula...')
    regular.fit(nparray)
    print('Fitting center vine copula...')
    center.fit(nparray)
    print('Fitting direct vine copula...')
    direct.fit(nparray)

    store_model(regular, f'{output_name}_regular')
    store_model(center, f'{output_name}_center')
    store_model(direct, f'{output_name}_direct')


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('dataset', type=str, help='Path to the input file')
    arg_parser.add_argument('-f', '--input_format', type=str, choices=['excel', 'csv'], default='excel', required=False,
                            help='Format of the input file')
    arg_parser.add_argument('-o', '--output_name', type=str, default='output', required=False,
                            help='Name of the output model')
    arg_parser.add_argument('-n', '--sample_number', type=int, default=20000, required=False,
                            help='How many samples to use from the dataset')
    args = arg_parser.parse_args()

    dataset: pd.DataFrame
    if args.input_format == 'excel':
        dataset = pd.read_excel(args.dataset)
    else:
        dataset = pd.read_csv(args.dataset)

    print(f'Successfully read {len(dataset)} lines and using {args.sample_number} samples of it')

    generate_vine_copulas(dataset, args.output_name, args.sample_number)


if __name__ == '__main__':
    main()
