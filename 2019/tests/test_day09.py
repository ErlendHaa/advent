import pytest

from aoc2019 import helpers

def test_copy_self():
    intcodes = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    comp = helpers.computer('test', list(intcodes), [])
    comp()
    assert comp.outputs == intcodes

def test_16digits():
    intcodes = [1102,34915192,34915192,7,4,7,99,0]
    comp = helpers.computer('test', list(intcodes), [])
    comp()

    assert len(comp.outputs) == 1
    assert len([x for x in str(comp.outputs[0])]) == 16

def test_largenumber():
    intcodes = [104,1125899906842624,99]
    comp = helpers.computer('test', list(intcodes), [])
    comp()

    assert comp.outputs[0] == 1125899906842624
