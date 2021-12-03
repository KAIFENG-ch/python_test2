from functools import wraps
import time


def log1(func):
    @wraps(func)
    def wrapper(*args, **kw):
        print('[hello]')
        return func(*args, **kw)

    return wrapper


def log2(func):
    @wraps(func)
    def wrapper(*args, **kw):
        t = time.time() * 1000
        print(func.__name__)
        func(*args, **kw)
        print(time.time() * 1000 - t)

    return wrapper


@log1
@log2
def func1():
    time.sleep(2)
    print("hello python")


func1()
