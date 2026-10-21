from turing import Machine
from examples.num1 import ALPHABET as ALPHABET_num1, TRANSITIONS as TRANSITIONS_num1
from examples.num2 import ALPHABET as ALPHABET_num2, TRANSITIONS as TRANSITIONS_num2
from examples.num3 import ALPHABET as ALPHABET_num3, TRANSITIONS as TRANSITIONS_num3


TASKS = {
    1: Machine("num1", ALPHABET_num1, TRANSITIONS_num1),
    2: Machine("num2", ALPHABET_num2, TRANSITIONS_num2),
    3: Machine("num3", ALPHABET_num3, TRANSITIONS_num3),
}