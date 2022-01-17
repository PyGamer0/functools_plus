"""more_functools: A python library that extends functools."""
from functools import reduce, wraps
from itertools import accumulate

__version__ = "0.1.0"

__all__ = [
    "compose",
    "const",
    "constantly",
    "flip",
    "foldl",
    "foldl1",
    "foldr",
    "foldr1",
    "identity",
    "scanl",
    "scanl1",
    "scanr",
    "scanr1",
    "zipWith",
]


def append(value, iterable):
    for element in iterable:
        yield element
    yield value


def prepend(value, iterable):
    yield value
    for element in iterable:
        yield element


def flip(func):
    """flip: returns a function with reversed position arguments of func"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*reversed(*args), **kwargs)

    return wrapper


def identity(x):
    """identity: return the argument"""
    return x


def compose(*funcs, **kwargs):
    """compose: compose the funcs into a single function

    kwargs:
        unpack: if unpack is True, then unpack the result of each function before passing it to the next
    """
    unpack = kwargs.get("unpack", False)
    if not funcs:
        return identity
    outer, funcs = funcs[-1], reversed(funcs[:-1])
    if unpack:

        @wraps(outer)
        def wrapper(*args, **kwargs):
            ret = outer(*args, **kwargs)
            for func in funcs:
                ret = func(*ret)
            return ret

    else:

        @wraps(outer)
        def wrapper(*args, **kwargs):
            ret = outer(*args, **kwargs)
            for func in funcs:
                ret = func(ret)
            return ret

    return wrapper


def const(x, *args, **kwargs):
    """const: returns x ignoring other arguments"""
    return x


def constantly(x):
    """constantly: returns the function const(x)"""

    @wraps(const)
    def wrapper(*args, **kwargs):
        return x

    return wrapper


def foldl(func, start, iterable):
    """foldl: foldl is folding a function from left to right

    func: the function to reduce with
    start: the initial starting value
    iterable: the iterable to reduce over
    """
    return reduce(func, iterable, start)


def foldl1(func, iterable):
    """foldl1: foldl1 is folding a function from left to right without an initial value

    func: the function to reduce with
    iterable: the iterable to reduce over
    """
    return reduce(func, iterable)


def _foldr(func, start, iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return start
    return func(first, _foldr(func, start, iterable))


def foldr(func, start, iterable):
    """foldr: foldr is folding a function from right to left

    func: the function to reduce with
    start: the initial starting value
    iterable: the iterable to reduce over
    """
    return _foldr(func, start, iter(iterable))


def _foldr1(func, iterable):
    first = next(iterable)
    try:
        return func(first, _foldr1(func, iterable))
    except StopIteration:
        return first


def foldr1(func, iterable):
    """foldr1: foldr1 is folding a function from right to left without an initial value

    func: the function to reduce with
    iterable: the iterable to reduce over
    """
    try:
        return _foldr1(func, iter(iterable))
    except StopIteration:
        raise TypeError("foldr1() of empty sequence")


def scanl(func, start, iterable):
    """scanl: similar to foldl but also outputs intermediate values

    func: the function to scan with
    start: the initial starting value
    iterable: the iterable to scan over"""
    return accumulate(prepend(start, iterable), func)


def scanl1(func, iterable):
    """scanl: similar to foldl1 but also outputs intermediate values

    func: the function to scan with
    iterable: the iterable to scan over"""
    return accumulate(iterable, func)


def _scanr(func, start, iterable):
    try:
        first = next(iterable)
    except StopIteration:
        yield start
        raise StopIteration
    rest = _scanr(func, start, iterable)
    value = next(rest)
    yield func(first, value)
    yield value
    for value in rest:
        yield value


def scanr(func, start, iterable):
    """scanr: similar to foldr but also outputs intermediate values

    func: the function to scan with
    start: the initial starting value
    iterable: the iterable to scan over"""
    return _scanr(func, start, iter(iterable))


def _scanr1(func, iterable):
    first = next(iterable)
    try:
        rest = _scanr1(func, iterable)
        value = next(rest)
        yield func(first, value)
        yield value
        for value in rest:
            yield value
    except StopIteration:
        yield first


def scanr1(func, iterable):
    """scanr1: similar to foldr1 but also outputs intermediate values

    func: the function to scan with
    iterable: the iterable to scan over"""
    return _scanr1(func, iter(iterable))


def zipWith(func, *iterables):
    """zipWith: zip the iterables and apply func to each of them

    func: the function to apply
    *iterables: the iterables
    """
    return map(lambda args: func(*args), zip(*iterables))
