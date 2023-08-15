import datetime

import numpy as np
import pandas as pd
from hash_table import HashTable
from package import Package
from truck import Truck
from IPython.display import display
import datetime

import distance


def load_hash_table():
    package_data = pd.read_excel("Resources\\WGUPS Package File.xlsx")
    table = HashTable()

    for index, row in package_data.iterrows():
        if type(row[0]) != int:
            continue

        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        table.put(package.package_id, package)

    return table


hash_table = load_hash_table()


def load_trucks_algorithmically():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    trucks = [Truck(now.replace(hour=9)), Truck(now.replace(hour=10)), Truck(now.replace(hour=11))]

    # loop in order of deadline then create a time efficiency value for each truck

    for index, package in enumerate(hash_table):
        truck_to_use = -1
        least_modified_distance = -1
        efficient_index = -1

        for truck_index, truck in enumerate(trucks):
            if len(truck.scheduled_deliveries) == 0:
                truck_to_use = truck_index
                efficient_index = 0
                least_modified_distance = distance.assess_length_for_insertion(truck, package, efficient_index)
                break

            if len(truck.scheduled_deliveries) == 16:
                continue

            # determine time efficiency of adding to each list
            modified_distance, index_insert = distance.determine_most_efficient_insert_time(package, truck)

            if modified_distance < least_modified_distance or least_modified_distance == -1:
                least_modified_distance = modified_distance
                truck_to_use = truck_index
                efficient_index = index_insert

                if modified_distance == 0:
                    break

        trucks[truck_to_use].add_delivery(efficient_index, package, least_modified_distance)

    print("test")
    # distance.generate_truck_report(trucks[0])
    # distance.generate_truck_report(trucks[1])
    # distance.generate_truck_report(trucks[2])
    # distance.simulate_delivery(trucks)




def create_schedule(trucks):
    print("simulating delivery")
    current_time = trucks[0].time_leaving
    test = datetime.time(hour=9, minute=10)
    print(test)


if __name__ == '__main__':
    load_hash_table()
    # print(find_distance("Sugar House Park 1330 2100 S", "Holiday City Office 4580 S 2300 E"))
    load_trucks_algorithmically()
