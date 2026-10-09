import time
import random

def random_sleep(base, bounds):
    """
    Generates a variable amount of time of the form:

    base + random value

    Arguments:
        base - floor amount of time
        bounds - tuple bounding the random value
    """
    time.sleep(base + random.randint(bounds[0], bounds[1]))