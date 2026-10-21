from turing import Machine, run
from examples.num2 import ALPHABET, TRANSITIONS, CASES_OK


def test_ok():
    m = Machine("num2", ALPHABET, TRANSITIONS)
    for inp, expected in CASES_OK:
        got = run(inp, m)
        assert got == expected, f"вход={inp!r}: ждали {expected!r}, получили {got!r}"
