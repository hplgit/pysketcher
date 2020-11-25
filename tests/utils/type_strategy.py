import logging
from typing import Callable, get_args, get_origin, get_type_hints, Type, TypeVar

from hypothesis.strategies import register_type_strategy, SearchStrategy

RT = TypeVar("RT")


class TypeStrategy:
    _func: Callable[[], SearchStrategy]

    def __init__(self, typ: Type = None) -> None:
        self._type = typ

    def __call__(self, func: Callable[[], SearchStrategy[RT]]) -> SearchStrategy[RT]:
        self._func = func

        def wrapper(*args, **kwargs):
            logging.debug(f"Calling {self._func.__name__}.")
            return self._func(*args, **kwargs)

        if not self._type:
            hints = get_type_hints(func)
            logging.debug(hints)
            if "return" not in hints:
                msg = (
                    f"Cannot register {self._func.__name__}, "
                    "as does not have a return type hint."
                )
                logging.error(msg)
                raise ValueError(msg)
            else:
                hint = hints["return"]
                origin = get_origin(hint)
                if origin != SearchStrategy:
                    msg = (
                        f"Cannot register {self._func.__name__}, "
                        "as does it returns {origin} not a SearchStrategy"
                    )
                    logging.error(msg)
                    raise ValueError(msg)
                else:
                    self._type = get_args(hint)[0]
        logging.debug(f"Registering {self._func.__name__} to {self._type}.")
        register_type_strategy(self._type, func)
        return wrapper
