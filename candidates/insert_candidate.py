import math


class InsertCandidate:
    def __init__(self, modified_distance, index, truck, package):
        self.modified_distance = modified_distance
        self.index = index
        self.truck = truck
        self.package = package

    def get_weighted_value(self):
        capacity_value = (self.truck.capacity - len(self.truck.scheduled_deliveries)) / self.truck.capacity
        distance_value = math.pow(1.3, -self.modified_distance)
        weighted_value = (capacity_value + distance_value) / 2
        return weighted_value

