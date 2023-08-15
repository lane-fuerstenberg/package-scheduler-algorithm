from enum import Enum


class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.package_status = Status.AT_HUB

    def assign_status(self, status):
        self.package_status = status


class Status(Enum):
    AT_HUB = "at_hub"
    EN_ROUTE = "en_route"
    DELIVERED = "delivered"
