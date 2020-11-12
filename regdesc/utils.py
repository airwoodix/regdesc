import inspect
import re


def is_strict_subclass_pred(base):
    def pred(cls):
        return inspect.isclass(cls) and issubclass(cls, base) and cls is not base

    return pred


def camel_to_snake(name):
    # https://stackoverflow.com/a/1176023
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
