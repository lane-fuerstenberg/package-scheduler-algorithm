import csv


def load_distance_table():
    array = []
    with open("Resources/distance.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            array.append(row)

    return array


distance_data = load_distance_table()


def miles_to_minutes(miles):
    return (miles / 18) * 60


def find_index(string):
    for index, columns in enumerate(distance_data[0]):
        if string == columns:
            return index


def find_distance(package1, package2):
    return get(string_format_package(package1), string_format_package(package2))


def get(row, column):
    row_index = find_index(row)
    column_index = find_index(column)
    return float(distance_data[row_index][column_index])


def string_format_package(package):
    if package is None or package == "HUB":
        return "HUB"

    return package.address + "(" + str(package.zip) + ")"
