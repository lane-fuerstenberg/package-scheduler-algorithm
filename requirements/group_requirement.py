
class GroupRequirement:

    def __init__(self, group_with):
        self.group_with = group_with
        self.truck_id = None

    def set_group_truck(self, truck_id):
        self.truck_id = truck_id
