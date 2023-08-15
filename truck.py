import datetime
import distance

from scheduled_delivery import ScheduledDelivery


class Truck:
    def __init__(self, time_leaving):
        self.scheduled_deliveries: ScheduledDelivery = []
        self.time_leaving = time_leaving

    def add_delivery(self, index, package, distance_added):
        start_time: datetime.datetime
        end_location = distance.string_format_package(package)
        if len(self.scheduled_deliveries) == 0 or index == 0:
            start_time = self.time_leaving
            start_location = "HUB"
        elif len(self.scheduled_deliveries) == index:
            start: ScheduledDelivery = self.scheduled_deliveries[index - 1]
            start_time = start.scheduled_time
            start_location = distance.string_format_package(start.package)
        else:
            start: ScheduledDelivery = self.scheduled_deliveries[index]
            start_time = start.scheduled_time
            start_location = distance.string_format_package(start.package)

        distance_to_package = distance.find_distance(start_location, end_location)
        delivery_time = start_time + datetime.timedelta(minutes=(distance_to_package / 18) * 60)
        delivery: ScheduledDelivery = ScheduledDelivery(package, delivery_time)
        self.scheduled_deliveries.insert(index, delivery)

        self.delay_future_scheduled_packages(index, distance_added)
        # adjust time_modified for each element past index

    def delay_future_scheduled_packages(self, index, distance_added):
        for i in range(index + 1, len(self.scheduled_deliveries)):
            self.scheduled_deliveries[i].scheduled_time += datetime.timedelta(minutes=(distance_added / 18) * 60)

