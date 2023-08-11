import numpy as np
import pandas as pd
from hash_table import HashTable
from package import Package
from truck import Truck
from IPython.display import display

def load_hash_table():
    package_data = pd.read_excel("Resources\\WGUPS Package File.xlsx")
    table = HashTable()

    for index, row in package_data.iterrows():
        if type(row[0]) != int:
            continue

        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        print(package.package_id)
        table.put(package.package_id, package)

    return table


distance_data = pd.read_excel("Resources\\WGUPS Distance Table.xlsx")

hash_table = load_hash_table()


def find_distance(row, column):
    return distance_data.iloc[row, column]


def load_trucks_algorithmically():
    trucks = [Truck() for _ in range(3)]

    # loop in order of deadline then create a time efficiency value for each truck

    for index, package in enumerate(hash_table):
        for truck in trucks:
            if len(truck.packages) == 0:
                truck.packages.append(package)
                break

            # determine time efficiency of adding to each list
            length = assess_length_of_list(truck.packages)
            print("length is " + str(length))

            # attempt to load each package into a truck
            # original truck time = how long for a truck
            # new truck time = how long for truck now

        # compare old time / new time of truck to find the time efficiency then pick the lowest option
        print(trucks)


def assess_length_of_list(package_list):
    print("assess length")
    # find length of list journey
    return -1


def main():
    load_hash_table()
    test = np.tril(distance_data)
    display(test)
    print(find_distance(10, 3))
    load_trucks_algorithmically()


if __name__ == '__main__':
    main
