
class SwapCandidate:
    def __init__(self, modified_distance, index, truck, package):
        self.modified_distance = modified_distance
        self.index = index
        self.truck = truck
        self.package = package

    def get_weighted_value(self):
        return self.modified_distance

