import pandas as pd
import datetime


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


def determine_most_efficient_insert_time(package, truck):
    modified_time = -1
    index_insert = -1

    for i in range(len(truck.scheduled_deliveries) + 1):
        original_time = assess_length_for_index(truck.scheduled_deliveries, i)
        insert_time = assess_length_for_insertion(truck, package, i) - original_time
        if modified_time == -1 or insert_time < modified_time:
            modified_time = insert_time
            index_insert = i

    return modified_time, index_insert


# todo: verify that this is not completely broken after refactor
def assess_length_for_insertion(truck, package, index):
    scheduled_deliveries = truck.scheduled_deliveries

    # find length of list journey
    distance = 0
    wgu = 'HUB'

    start = wgu
    middle = string_format_package(package)
    end = wgu

    if index != 0:
        start = string_format_package(scheduled_deliveries[index - 1].package)

    if index != len(scheduled_deliveries):
        end = string_format_package(scheduled_deliveries[index].package)

    distance += find_distance(start, middle)
    distance += find_distance(middle, end)
    return distance


def assess_length_for_index(scheduled_deliveries, index):
    # find length of list journey
    distance = 0
    wgu = 'HUB'

    start: str
    end: str

    if index == 0:
        start = wgu
        end = string_format_package(scheduled_deliveries[index].package)

    elif index == len(scheduled_deliveries):
        start = string_format_package(scheduled_deliveries[index - 1].package)
        end = wgu

    else:
        start = string_format_package(scheduled_deliveries[index - 1].package)
        end = string_format_package(scheduled_deliveries[index].package)

    distance += find_distance(start, end)
    # # todo:
    # if end != wgu:
    #     truck.schedule.insert(index)
    return distance


def assess_length_of_list(package_list):
    distance = 0

    wgu = 'HUB'
    distance += find_distance(wgu, string_format_package(package_list[0]))

    for i in range(1, len(package_list)):
        distance += find_distance(string_format_package(package_list[i - 1]), string_format_package(package_list[i]))

    distance += find_distance(string_format_package(package_list[-1]), wgu)
    return distance

#
# def generate_truck_report(truck: Truck):
#     # find time for each package to be delivered, status of the packages
#     # find the total time for all deliveries to be completed
#     # note which packages did NOT get delivered in time
#     print('\r\n')
#     print(truck)
#     current_time: datetime.datetime = truck.time_leaving
#     miles_per_hour = 18
#     minutes_in_hour = 60
#
#     for i in range(len(truck.packages) + 1):
#         if i == 0:
#             start = "HUB"
#             end = string_format_package(truck.packages[i])
#             status_update = "truck delivered package: " + str(truck.packages[i].package_id)\
#                             + " DEADLINE = " + str(truck.packages[i].delivery_deadline)
#         elif i == len(truck.packages):
#             start = string_format_package(truck.packages[i - 1])
#             end = "HUB"
#             status_update = "finished all deliveries"
#         else:
#             start = string_format_package(truck.packages[i - 1])
#             end = string_format_package(truck.packages[i])
#             status_update = "truck delivered package: " + str(truck.packages[i].package_id) \
#                             + " DEADLINE = " + str(truck.packages[i].delivery_deadline)
#
#         current_time += datetime.timedelta(minutes=(find_distance(start, end) / miles_per_hour) * minutes_in_hour)
#         print(str(current_time.time().strftime("%H:%M:%S")) + " - " + status_update)


def find_distance(row, column):
    return distance_data.at[row, column]


def string_format_package(package):
    return package.address + "(" + str(package.zip) + ")"
