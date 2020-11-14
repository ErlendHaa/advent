import pytest

from collections import deque

from aoc2019.day22 import deal2stack, deal2table, cut

def test_deal2stack():
    deck = deque(range(10))

    res = deal2stack(deck)
    assert res == deque([9,8,7,6,5,4,3,2,1,0])

def test_deal2table():
    deck = deque(range(10))

    res = deal2table(deck, 3)
    assert res == deque([0,7,4,1,8,5,2,9,6,3])

def test_cut():
    deck = deque(range(10))

    res = cut(deck, 3)
    assert res == deque([3,4,5,6,7,8,9,0,1,2])
