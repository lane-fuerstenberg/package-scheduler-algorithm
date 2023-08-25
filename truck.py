import datetime
from utility import distance

from scheduled_delivery import ScheduledDelivery


class Truck:
    def __init__(self, truck_id, time_leaving):
        self.scheduled_deliveries: ScheduledDelivery = []
        self.time_leaving = time_leaving
        self.capacity = 16
        self.truck_id = truck_id

    def add_scheduled_delivery(self, index, scheduled_delivery: ScheduledDelivery):
        self.scheduled_deliveries.insert(index, scheduled_delivery)

    def add_delivery(self, insert_candidate):
        start_location = "HUB"
        end_location = insert_candidate.package
        start_time = self.time_leaving

        if insert_candidate.index != 0:
            scheduled_delivery = self.scheduled_deliveries[insert_candidate.index - 1]
            start_location = scheduled_delivery.package
            start_time = scheduled_delivery.scheduled_time

        distance_to_package = distance.find_distance(start_location, end_location)
        minutes = distance.miles_to_minutes(distance_to_package)
        delivery_time = start_time + datetime.timedelta(minutes=minutes)
        delivery: ScheduledDelivery = ScheduledDelivery(insert_candidate.package, delivery_time)
        self.scheduled_deliveries.insert(insert_candidate.index, delivery)

        self.delay_future_scheduled_deliveries(insert_candidate.index, insert_candidate.modified_distance)

    def delay_future_scheduled_deliveries(self, index, modified_distance):
        if modified_distance == 0:
            return

        for i in range(index + 1, len(self.scheduled_deliveries)):
            minutes = distance.miles_to_minutes(modified_distance)
            future_scheduled_delivery = self.scheduled_deliveries[i]
            future_scheduled_delivery.scheduled_time += datetime.timedelta(minutes=minutes)
