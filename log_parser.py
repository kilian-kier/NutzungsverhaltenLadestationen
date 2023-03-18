import argparse
import xlsxwriter
import re
import csv
from datetime import datetime


class ChargerLog:
    headers_xlsx = ['Date', 'Time', 'Plug Type' 'Target voltage [V]', 'Target current [A]', 'max. current [A]',
                    'Actual voltage [V]', 'Actual current [A]', 'Actual power [W]', 'State of charge [%]',
                    'Energymeter reading [Wh]',
                    'Resistence [\u03A9]', 'Temperature 1 [°C]', 'Temperature 2 [°C]']

    headers_csv = ['Date', 'Time', 'Plug Type' 'Target voltage [V]', 'Target current [A]', 'max. current [A]',
                   'Actual voltage [V]', 'Actual current [A]', 'Actual power [W]', 'State of charge [%]',
                   'Energymeter reading [Wh]',
                   'Resistence [ogm]', 'Temperature 1 [C]', 'Temperature 2 [C]']

    date_time: datetime
    date: datetime
    time: datetime
    plug: str
    target_voltage: float
    target_current: float
    max_current: float
    actual_voltage: float
    actual_current: float
    actual_power: float
    charging_level: float
    energymeter_reading: float
    resistence: float
    temp_1: float
    temp_2: float

    def __init__(self, match):
        self.date = datetime.strptime(match.group(1), '%Y-%m-%d')
        self.time = datetime.strptime(match.group(2), '%H:%M:%S.%f')
        self.plug = match.group(3).split(']')[0]
        self.target_voltage = float(match.group(4))
        self.target_current = float(match.group(5))
        self.max_current = float(match.group(6))
        self.actual_voltage = float(match.group(7))
        self.actual_current = float(match.group(8))
        self.actual_power = float(match.group(9))
        self.charging_level = float(match.group(10)) / 100.0
        self.energymeter_reading = float(match.group(11))
        self.resistence = float(match.group(12))
        self.temp_1 = float(match.group(13))
        self.temp_2 = float(match.group(14))


def read_data(input_path):
    input_file = open(input_path, 'r')
    pattern = r'\[(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\.\d+)\]\s*\[(.*?)\]\s*' \
              r'target:\s*(.*?)\s*V,\s*(.*?)\s*A\s*\(HYC:\s*(.*?)\s*A\)\.\s*actual:' \
              r'\s*(.*?)\s*V,\s*(.*?)\s*A,\s*(.*?)\s*W,\s*(.*?)%,\s*(.*?)\s*Wh,\s*(.*?)\s*kOhm,' \
              r'\s*(.*?)\s*C,\s*(.*?)\s*C.'

    result = []

    temp = []
    n = 0
    for line in input_file:
        if line == '\n':
            result.append(temp.copy())
            temp.clear()
        match = re.search(pattern, line)
        if match:
            log_line = ChargerLog(match)
            temp.append(log_line)
        n += 1

    input_file.close()
    return n, result


def write_xlsx(data, workbook, worksheet):
    worksheet.write_row(0, 0, tuple(ChargerLog.headers_xlsx))

    date_format = workbook.add_format()
    date_format.set_num_format('dd/mm/yy')

    time_format = workbook.add_format()
    time_format.set_num_format('hh:MM:ss')

    percentage_format = workbook.add_format()
    percentage_format.set_num_format('0%')

    for j, line in enumerate(data):
        row = [
            line.plug,
            line.target_voltage,
            line.target_current,
            line.max_current,
            line.actual_voltage,
            line.actual_current,
            line.actual_power,
            line.charging_level,
            line.energymeter_reading,
            line.resistence,
            line.temp_1,
            line.temp_2
        ]
        worksheet.write(j + 1, 0, line.date, date_format)
        worksheet.write(j + 1, 1, line.time, time_format)
        worksheet.write_row(j + 1, 2, row)
        worksheet.write(j + 1, 8, line.charging_level, percentage_format)


def write_csv(data, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(ChargerLog.headers_csv)
        for line in data:
            writer.writerow([line.date.strftime('%d/%m/%y'),
                             line.time.strftime('%H:%M:%S'), line.plug, line.target_voltage, line.target_current,
                             line.max_current,
                             line.actual_voltage, line.actual_current, line.actual_power, line.charging_level,
                             line.energymeter_reading, line.resistence, line.temp_1, line.temp_2])


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('log_file', type=str, help='Path to the input Log file')
    arg_parser.add_argument('-f', '--output_format', type=str, required=False, default='excel', choices=['excel', 'csv'],
                            help='The format in which the output will be saved')
    arg_parser.add_argument('-o', '--output_path', type=str, required=False, default='output.xlsx',
                            help='Path where the output will be saved')
    args = arg_parser.parse_args()
    n, data = read_data(args.log_file)
    if args.output_format == 'excel':
        workbook = xlsxwriter.Workbook(args.output_path)
        for i, session in enumerate(data):
            worksheet = workbook.add_worksheet(f'{i + 1}')
            write_xlsx(session, workbook, worksheet)
        workbook.close()
    else:
        if args.output_path == 'output.xlsx':
            args.output_path = 'output.csv'

        args.output_path = args.output_path[:args.output_path.rfind('.')]

        for i, session in enumerate(data):
            write_csv(session, args.output_path + str(i + 1) + '.csv')

    print(f'Successfully wrote {n} lines')


if __name__ == '__main__':
    main()
