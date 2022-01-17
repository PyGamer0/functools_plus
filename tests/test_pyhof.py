import pyhof as hof


def test_compose():
    assert hof.compose(lambda x: x ** 2, lambda x: x + 1)(4) == 25


def test_const():
    assert hof.const(1, 2, 3) == 1


def test_constantly():
    assert hof.constantly(1)(2, 3) == 1


def test_flip():
    assert hof.flip(lambda x, y: x - y)(3, 2) == -1


def test_foldl():
    assert hof.foldl(lambda x, y: x + y, 0, [1, 2, 3]) == 6


def test_foldl1():
    assert hof.foldl1(lambda x, y: x + y, [1, 2, 3]) == 6


def test_foldr():
    assert hof.foldr(lambda x, y: x - y, 0, [1, 2, 3]) == 2


def test_foldr1():
    assert hof.foldr1(lambda x, y: x - y, [1, 2, 3]) == 2
