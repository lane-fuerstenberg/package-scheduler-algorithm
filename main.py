
import pandas as pd
from hash_table import HashTable
from package import Package


distance_data = pd.read_excel("Resources\\WGUPS Distance Table.xlsx")


def load_hash_table():
    package_data = pd.read_excel("Resources\\WGUPS Package File.xlsx")
    table = HashTable()

    for index, row in package_data.iterrows():
        if type(row[0]) != int:
            continue

        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        print(package.package_id)
        table.put(package.package_id, package)


def find_distance(row, column):
    return distance_data.iloc[row, column]


if __name__ == '__main__':
    load_hash_table()
    print("break")
    print(find_distance(10, 3))
