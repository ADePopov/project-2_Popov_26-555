import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def handle_db_errors(func: Callable[P, R]) -> Callable[P, R | str]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | str:
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError as e:
            return f"Ошибка {e}, введены некорректные данные"
        except ValueError as v:
            return f"Ошибка {v}, некорректный тип данных"
        except FileNotFoundError as f:
            return f"Ошибка {f}, файл не найден"
        except Exception as e:
            return f"Ошибка {e}"

    return wrapper


def confirm_action(
    action_name: str,
) -> Callable[[Callable[P, R]], Callable[P, R | str]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R | str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            answer = input(f"Вы уверены, что хотите выполнить {action_name}? [y/n]: ")
            if answer == "y":
                return func(*args, **kwargs)
            else:
                return "Действие отменено"

        return wrapper

    return decorator


def log_time(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        full_time = end_time - start_time
        print(f"Функция выполнилась за {full_time:.5f} секунд")
        return result

    return wrapper


def create_cacher():
    cache = {}

    def cache_result(key, value_func: Callable[[], R]) -> R:
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    def clear():
        cache.clear()

    cache_result.clear = clear
    return cache_result
