from functools import wraps
import inspect


class MFACInterface:
    def __init__(self):
        pass

    def run(self):
        pass

    @classmethod
    def initializer(self, func):
        """
        Automatically assigns the parameters.
        """
        names, varargs, keywords, defaults = inspect.getargspec(func)

        @wraps(func)
        def wrapper(self, *args, **kargs):
            for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
                setattr(self, name, arg)

            if defaults and names:
                for name, default in zip(reversed(names), reversed(defaults)):
                    if not hasattr(self, name):
                        setattr(self, name, default)

            func(self, *args, **kargs)

        return wrapper


class PlantInterface:
    def __init__(self):
        pass

    def reset(self):
        pass

    def step(self, u):
        pass

    def render(self, mode):
        pass

    def observe(self, window):
        pass

    @classmethod
    def initializer(self, func):
        """
        Automatically assigns the parameters.
        """
        names, varargs, keywords, defaults = inspect.getargspec(func)

        @wraps(func)
        def wrapper(self, *args, **kargs):
            for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
                setattr(self, name, arg)

            if defaults and names:
                for name, default in zip(reversed(names), reversed(defaults)):
                    if not hasattr(self, name):
                        setattr(self, name, default)

            func(self, *args, **kargs)

        return wrapper