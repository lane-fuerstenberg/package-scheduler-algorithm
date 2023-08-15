from package import Package
import datetime


class ScheduledDelivery:
    def __init__(self, package: Package, scheduled_time: datetime.datetime):
        self.package = package
        self.scheduled_time = scheduled_time

