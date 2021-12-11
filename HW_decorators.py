import sys
from datetime import datetime
from typing import Callable

# Задача 1
original_write = sys.stdout.write


def my_write(string_text: str):
    if string_text != '\n':
        return original_write(f'[{datetime.now()}]: {string_text}')
    else:
        return original_write(string_text)


sys.stdout.write = my_write
print('1, 2, 3')
sys.stdout.write = original_write


# Задача 2
def timed_output(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f'[{datetime.now()}]:')
        function(*args, **kwargs)

    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


print_greeting("Nikita")


# Задача 3
def redirect_output(filepath: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            output = open(filepath, 'w')

            def my_write(string_text: str):
                output.write(string_text)

            original_write = sys.stdout.write
            sys.stdout.write = my_write
            func(*args, **kwargs)
            output.close()
            sys.stdout.write = original_write

        return wrapper

    return decorator


@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


calculate()
