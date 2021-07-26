import os
import csv


def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    result = []
    for line in reader:
        result.append(f"{line.get('Title')} {line.get('Price')}")
    return result


def get_csv_file():  # функцию можно заменить на выбор файла в ui
    path = os.getcwd()
    file_list = os.listdir(path)
    for file in file_list:
        if os.path.splitext(file)[-1] == '.csv':
            return file


def get_data_from_csv(file=None):
    if file is None:
        file = get_csv_file()
    with open(file) as f_obj:
        return csv_dict_reader(f_obj)
