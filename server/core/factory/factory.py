from functools import partial

from fastapi import depends


class Factory:
    """
    This factory container will instantiate all the controllers and the
    repositories which can be accessed by the rest of the application.
    """
