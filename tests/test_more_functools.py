import more_functools as mft


def test_compose():
    assert mft.compose(lambda x: x ** 2, lambda x: x + 1)(4) == 25


def test_const():
    assert mft.const(1, 2, 3) == 1


def test_constantly():
    assert mft.constantly(1)(2, 3) == 1


def test_flip():
    assert mft.flip(lambda x, y: x - y)(3, 2) == -1


def test_foldl():
    assert mft.foldl(lambda x, y: x + y, 0, [1, 2, 3]) == 6


def test_foldl1():
    assert mft.foldl1(lambda x, y: x + y, [1, 2, 3]) == 6


def test_foldr():
    assert mft.foldr(lambda x, y: x - y, 0, [1, 2, 3]) == 2
