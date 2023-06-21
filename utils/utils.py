import random
from time import sleep


def random_delay(endpoint):
    """Decorator for simulating 0.1s to 1s delay for the endpoints"""
    def delay(*args, **kwargs):
        sleep(random.uniform(0.1, 1))
        response = endpoint(*args, **kwargs)
        return response
    return delay


def get_order_statuses():
    """Available statuses"""
    return ["PENDING", "EXECUTED", "CANCELLED"]


def get_fake_statuses():
    return ["SOME", "FAKE", "STATUSES"]
