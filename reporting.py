import datetime

from utility import distance


def generate_truck_report(trucks):
    print('\r\nTotal Truck Distance: ')
    truck_distance = 0
    for truck in trucks:
        for i in range(len(truck.scheduled_deliveries) + 1):
            start = "HUB"
            end = "HUB"

            if i != 0:
                start = truck.scheduled_deliveries[i - 1].package
            if i != len(truck.scheduled_deliveries):
                end = truck.scheduled_deliveries[i].package

            truck_distance += distance.find_distance(start, end)

    print(truck_distance)


def print_unused(not_placed_packages):
    for package in not_placed_packages:
        print(f"{package.package_id} | {package.address} | {package.special_notes}")


def print_trucks(trucks):
    for truck in trucks:
        for scheduled_delivery in truck.scheduled_deliveries:
            print(f"{scheduled_delivery.scheduled_time} - truck {truck} delivered package: {scheduled_delivery.package.package_id}")


# todo: print status for all trucks given a time
def print_status_at_given_time(time: datetime.time, trucks):
    for truck in trucks:
        print("test status")


def print_package_deadlines_with_scheduled_times(trucks):
    for i, truck in enumerate(trucks):
        print(f'\r\nSTART OF TRUCK: {truck.truck_id} size of truck {len(truck.scheduled_deliveries)}')
        for j, middle in enumerate(truck.scheduled_deliveries):
            start = 'HUB'
            end = 'HUB'
            if j != 0:
                start = truck.scheduled_deliveries[j - 1].package
            if j != len(truck.scheduled_deliveries) - 1:
                end = truck.scheduled_deliveries[j + 1].package

            added = distance.find_distance(start, middle.package)
            added += distance.find_distance(middle.package, end)
            added -= distance.find_distance(start, end)
            print(f"{middle.scheduled_time.time()} - ID {middle.package.package_id} - {middle.package.address} | DEADLINE: {middle.package.delivery_deadline} SPECIAL: {middle.package.special_notes}")