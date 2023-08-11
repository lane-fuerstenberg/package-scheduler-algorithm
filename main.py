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
        table.put(package.package_id, package)

    return table


def load_distance_table():
    df = pd.read_excel("Resources\\WGUPS Distance Table Fixed.xlsx")
    df = df.rename(index=df['Unnamed: 1'])
    df = df.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    df = df.rename(columns=df.iloc[6])
    df = df.drop(df[:7].index)

    df.columns = df.columns.str.replace('\n', '')
    df.index = df.index.str.replace('\n', '')
    df.columns = df.columns.str.strip()
    df.index = df.index.str.strip()

    df = df.fillna(0)
    df = df.add(df.T)

    return df


distance_data = load_distance_table()

hash_table = load_hash_table()


def find_distance(row, column):
    return distance_data.at[row, column]


def load_trucks_algorithmically():
    trucks = [Truck() for _ in range(3)]

    # loop in order of deadline then create a time efficiency value for each truck

    for index, package in enumerate(hash_table):
        truck_to_use = -1
        most_efficient_ratio = -1
        index_insert = -1
        for truck_index, truck in enumerate(trucks):
            if len(truck.packages) == 0:
                truck_to_use = truck_index
                index_insert = 0
                break

            # determine time efficiency of adding to each list
            original_time = assess_length_of_list(truck.packages)
            modified_time, index_insert = determine_most_efficient_insert_time(package, truck)

            time_ratio = original_time / (modified_time + original_time)
            if time_ratio > most_efficient_ratio:
                most_efficient_ratio = time_ratio
                truck_to_use = truck_index

        add_to_truck(trucks[truck_to_use], package, index_insert)


# todo: add package to truck at insertion index
def add_to_truck(truck, package, index_insert):
    truck.packages.insert(index_insert, package)


def determine_most_efficient_insert_time(package, truck):
    modified_time = -1
    index_insert = -1
    for i in range(len(truck.packages) + 1):
        insert_time = assess_length_for_insertion(truck.packages, package, i)
        if modified_time == -1 or insert_time < modified_time:
            modified_time = insert_time
            index_insert = i

    return modified_time, index_insert


# todo: fix this method
def assess_length_for_insertion(package_list, package, index):
    # find length of list journey
    time = 0
    wgu = 'HUB'

    start: str
    middle = string_format_package(package)
    end: str

    print("\r\nASSESSING")
    print(package.address + " " + package_list.__str__())
    if index == 0:
        print('start')
        start = wgu
        end = string_format_package(package_list[index])

    # something is not correct here
    elif index == len(package_list):
        print('end')
        start = string_format_package(package_list[index - 1])
        end = wgu
    else:
        print('else')
        start = string_format_package(package_list[index - 1])
        end = string_format_package(package_list[index])

    time += find_distance(start, middle)
    time += find_distance(middle, end)

    print(time)
    return time


def assess_length_of_list(package_list):
    time = 0

    wgu = 'HUB'
    time += find_distance(wgu, string_format_package(package_list[0]))

    for i in range(1, len(package_list)):
        time += find_distance(string_format_package(package_list[i - 1]), string_format_package(package_list[i]))

    time += find_distance(string_format_package(package_list[-1]), wgu)
    print(time)
    return time


def string_format_package(package):
    return package.address + "(" + str(package.zip) + ")"


if __name__ == '__main__':
    load_hash_table()
    display(distance_data)
    # print(find_distance("Sugar House Park 1330 2100 S", "Holiday City Office 4580 S 2300 E"))
    load_trucks_algorithmically()
