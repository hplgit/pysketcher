import logging
from inspect import getfullargspec
from typing import get_type_hints

from hypothesis import given, infer
from hypothesis.errors import InvalidArgument


def given_inferred(func):

    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(
        func
    )
    logging.debug(f"{func.__name__} has been annotated with given_inferred.")

    def valid(self=None):
        nonlocal func, args, kwonlyargs
        logging.debug(f"{func.__name__} has been annotated with given_inferred.")
        # infer can only be applied to keywords, so convert the positionals to kws
        newargs = {arg: infer for arg in args if arg != "self"}
        kwargs = {kw: infer for kw in kwonlyargs}
        args = {**newargs, **kwargs}
        logging.debug(f"{func.__name__} args are {args}.")
        logging.debug(f"{func.__name__} type hints are {get_type_hints(func)}")
        if self:
            return given(**args)(func)(self)
        else:
            return given(**args)(func)()

    def invalid(message):
        def wrapped_test(*arguments, **kwargs):
            raise InvalidArgument(message)

        wrapped_test.is_hypothesis_test = True
        return wrapped_test

    if varargs:
        return invalid(
            f"Cannot apply @given_inferred to a function with arbitrary positional arguments."
        )
    if varkw:
        return invalid(
            f"Cannot apply @given_inferred to a function with arbitrary keyword arguments"
        )
    if defaults or kwonlydefaults:
        return invalid(f"Cannot apply @given_inferred to a function with defaults.")
    valid.is_hypothesis_test = True
    return valid
