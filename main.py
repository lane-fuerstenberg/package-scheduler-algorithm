# NHP3 — NHP3 TASK 2: WGUPS ROUTING PROGRAM IMPLEMENTATION
# DATA STRUCTURES AND ALGORITHMS II — C950
# Student: Richard Lane Fuerstenberg 010663034

import pandas as pd
import reporting
from utility.hash_table import HashTable
from candidates.insert_candidate import InsertCandidate
from package import Package, Status
from requirements.group_requirement import GroupRequirement
from requirements.time_requirement import TimeRequirement
from requirements.truck_requirement import TruckRequirement
from truck import Truck
import datetime
from utility import distance


# loading self adjusting hash table for package records
def load_hash_table():
    package_data = pd.read_excel("Resources\\WGUPS Package File.xlsx")
    table = HashTable()

    # inserting all the packages into the hashmap
    for index, row in package_data.iterrows():
        if type(row[0]) != int:
            continue

        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        table.put(package.package_id, package)

    return table


hash_table = load_hash_table()


# This is where the bulk of the algorithm takes place
def load_trucks_algorithmically():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    trucks = [Truck(1, now.replace(hour=8)), Truck(2, now.replace(hour=9, minute=5)),
              Truck(3, now.replace(hour=10, minute=20))]

    not_placed_packages = []
    insert_requirements = establish_requirements()
    # for every package in the hash table
    for index, package in enumerate(hash_table):
        best_insert_candidate: InsertCandidate = None

        # then we iterate through the trucks to search for the best position to place the package
        for truck_index, truck in enumerate(trucks):
            # check the package against the truck and insert requirements to see if this truck will be a valid insert
            if not passes_all_requirements(truck, package, insert_requirements):
                continue

            # once we assure the insert can be valid we iterate across the entire truck at every insert point to
            # calculate the most efficient insert for the package based on the distance added to the trucks overall
            # mileage for each insert point. Then select the lowest addition of mileage out of these choices and
            # return as an insert_candidate object storing all relevant information
            insert_candidate = find_greedy_insert(package, truck)
            # verify that a choice in the truck was made before proceeding
            if insert_candidate is None or insert_candidate.index == -1:
                continue

            # add the current insert_candidate as best_insert_candidate if there's no current best_insert_candidate
            # or compare them against each other to see if the current is better, then replace based on that.
            if (best_insert_candidate is None
                    or (insert_candidate.get_weighted_value() > best_insert_candidate.get_weighted_value())):
                best_insert_candidate = insert_candidate

        # if no insert_candidate was found add it to list of not placed packages
        if best_insert_candidate is None:
            not_placed_packages.append(package)
        # otherwise, add it to the truck
        else:
            add_insert_candidate_to_truck(best_insert_candidate, insert_requirements)

    return trucks


# used to create a list of insert requirements ahead of time
def establish_requirements():
    insert_requirements = []
    grp_arr = []
    # searches through all packages and adds to list of insert requirements
    for index, package in enumerate(hash_table):
        notes = package.special_notes
        if notes is None or not isinstance(notes, str):
            continue

        if notes == 'Can only be on truck 2':
            insert_requirements.append(TruckRequirement(package.package_id, 2))
        elif notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
            insert_requirements.append(TimeRequirement(package.package_id, datetime.time(hour=9, minute=5)))
        elif notes == 'Wrong address listed':
            package.address = '410 S State St'
            package.zip = '84111'
            insert_requirements.append(TimeRequirement(package.package_id, datetime.time(hour=10, minute=20)))
        elif notes.find("Must be delivered with") != -1:
            substring = notes.strip("Must be delivered with").replace(' ', '')
            if package.package_id not in grp_arr:
                grp_arr.append(package.package_id)
            for s in substring.split(','):
                i = int(s)
                if i not in grp_arr:
                    grp_arr.append(i)

    insert_requirements.append(GroupRequirement(grp_arr))
    return insert_requirements


# verify a package passes all requirements
def passes_all_requirements(truck, package, insert_requirements):
    if len(truck.scheduled_deliveries) == truck.capacity:
        return False

    for requirement in insert_requirements:
        if isinstance(requirement, TimeRequirement):
            if package.package_id == requirement.package_id and truck.time_leaving.time() < requirement.time:
                return False

        elif isinstance(requirement, GroupRequirement):
            if package.package_id in requirement.group_with:
                if requirement.truck_id is not None and requirement.truck_id != truck.truck_id:
                    return False

        elif isinstance(requirement, TruckRequirement):
            if package.package_id == requirement.package_id and truck.truck_id != requirement.truck_id:
                return False

    return True


# adds insert candidate to the truck
def add_insert_candidate_to_truck(ic, insert_requirements):
    for requirement in insert_requirements:
        if isinstance(requirement, GroupRequirement):
            if ic.package.package_id in requirement.group_with:
                requirement.truck_id = ic.truck.truck_id

    ic.truck.add_delivery(ic)


def is_truck_full(truck):
    return len(truck.scheduled_deliveries) >= truck.capacity


# looks for insert point into truck that adds the least amount of mileage
def find_greedy_insert(package, truck):
    modified_time = None
    index_insert = -1

    for i in range(len(truck.scheduled_deliveries) + 1):

        original_distance = assess_distance_index(truck.scheduled_deliveries, i)
        new_distance = assess_distance_insertion(truck, package, i)

        insert_time = new_distance - original_distance

        package_on_time = is_package_on_time(package, truck, i)
        future_packages_on_time = are_future_packages_on_time(truck, i, insert_time)

        if ((package_on_time and future_packages_on_time)
                and (modified_time is None or insert_time < modified_time)):
            modified_time = insert_time
            index_insert = i

    return InsertCandidate(modified_time, index_insert, truck, package)


# determines if an insert will make a trucks scheduled packages late
def are_future_packages_on_time(truck, i, offset_miles):
    for sd in truck.scheduled_deliveries[i:]:
        new_time = sd.scheduled_time + datetime.timedelta(minutes=distance.miles_to_minutes(offset_miles))
        deadline = sd.package.delivery_deadline
        if deadline != 'EOD' and new_time.time() > sd.package.delivery_deadline:
            return False

    return True


# determines that the package inserted at index i will arrive to its destination on time
def is_package_on_time(package, truck, i):
    if package.delivery_deadline != "EOD":
        start = "HUB"
        start_time = truck.time_leaving
        if i != 0:
            scheduled_delivery = truck.scheduled_deliveries[i - 1]
            start = scheduled_delivery.package
            start_time = scheduled_delivery.scheduled_time

        distance_added = distance.find_distance(start, package)
        new_scheduled_time = start_time + datetime.timedelta(minutes=distance.miles_to_minutes(distance_added))

        if new_scheduled_time.time() >= package.delivery_deadline:
            return False

    return True


# determine distance added to a truck by inserting at a given poiint
def assess_distance_insertion(truck, package, index):
    scheduled_deliveries = truck.scheduled_deliveries
    wgu = 'HUB'
    start = wgu
    end = wgu

    if index != 0:
        start = scheduled_deliveries[index - 1].package

    if index != len(scheduled_deliveries):
        end = scheduled_deliveries[index].package

    distance_added = distance.find_distance(start, package)
    distance_added += distance.find_distance(package, end)
    return distance_added


# determine the distance an index adds to the deliveries as a whole
def assess_distance_index(scheduled_deliveries, index):
    wgu = 'HUB'
    start = wgu
    end = wgu

    if index != 0:
        start = scheduled_deliveries[index - 1].package

    if index != len(scheduled_deliveries):
        end = scheduled_deliveries[index].package

    return distance.find_distance(start, end)


def assign_status_at_time(time, trucks):
    for truck in trucks:
        for scheduled_delivery in truck.scheduled_deliveries:
            if time > truck.time_leaving:
                if time > scheduled_delivery.scheduled_time:
                    scheduled_delivery.package.assign_status(Status.DELIVERED)
                elif time < scheduled_delivery.scheduled_time:
                    scheduled_delivery.package.assign_status(Status.EN_ROUTE)
            else:
                scheduled_delivery.package.assign_status(Status.AT_HUB)


def print_all_packages(trucks):
    for truck in trucks:
        for scheduled_delivery in truck.scheduled_deliveries:
            print(f"{scheduled_delivery.package.package_id} - scheduled delivery: {scheduled_delivery.scheduled_time.time()} - {scheduled_delivery.package.package_status.value}")


# main method
if __name__ == '__main__':
    load_hash_table()
    trucks_list = load_trucks_algorithmically()

    while 1:
        command = input("""
    Input command from:
    1) View status at given time and truck
    2) Total mileage travelled by trucks
    3) Print all packages with scheduled times
    4) Quit\r\n""")
        if command == '1':
            time_hour = int(input('What hour? (24 hour clock)\r\n'))
            time_minute = int(input('What minute?\r\n'))
            if time_minute > 59 or time_hour > 23 or time_minute < 0 or time_hour < 0:
                print('invalid time')
                continue
            assign_status_at_time(datetime.datetime.now().replace(hour=time_hour, minute=time_minute), trucks_list)
            print('Current time ' + datetime.datetime.now().replace(hour=time_hour, minute=time_minute).__str__())
            print_all_packages(trucks_list)

        elif command == '2':
            reporting.generate_truck_report(trucks_list)

        elif command == '3':
            reporting.print_package_deadlines_with_scheduled_times(trucks_list)

        elif command == '4':
            break

        else:
            print('\r\nInvalid command, try again.\r\n')
