from turing import Machine
from examples.num1 import ALPHABET as ALPHABET_num1, TRANSITIONS as TRANSITIONS_num1
from examples.num2 import ALPHABET as ALPHABET_num2, TRANSITIONS as TRANSITIONS_num2
from examples.num3 import ALPHABET as ALPHABET_num3, TRANSITIONS as TRANSITIONS_num3
from examples.num4 import ALPHABET as ALPHABET_num4, TRANSITIONS as TRANSITIONS_num4
from examples.num5 import ALPHABET as ALPHABET_num5, TRANSITIONS as TRANSITIONS_num5
from examples.num6 import ALPHABET as ALPHABET_num6, TRANSITIONS as TRANSITIONS_num6
from examples.num7 import ALPHABET as ALPHABET_num7, TRANSITIONS as TRANSITIONS_num7
from examples.num8 import ALPHABET as ALPHABET_num8, TRANSITIONS as TRANSITIONS_num8
from examples.num9 import ALPHABET as ALPHABET_num9, TRANSITIONS as TRANSITIONS_num9
from examples.num10 import ALPHABET as ALPHABET_num10, TRANSITIONS as TRANSITIONS_num10
from examples.num11 import ALPHABET as ALPHABET_num11, TRANSITIONS as TRANSITIONS_num11
from examples.num13 import ALPHABET as ALPHABET_num13, TRANSITIONS as TRANSITIONS_num13
from examples.num14 import ALPHABET as ALPHABET_num14, TRANSITIONS as TRANSITIONS_num14
from examples.num15 import ALPHABET as ALPHABET_num15, TRANSITIONS as TRANSITIONS_num15


TASKS = {
    1: Machine("num1", ALPHABET_num1, TRANSITIONS_num1),
    2: Machine("num2", ALPHABET_num2, TRANSITIONS_num2),
    3: Machine("num3", ALPHABET_num3, TRANSITIONS_num3),
    4: Machine("num4", ALPHABET_num4, TRANSITIONS_num4),
    5: Machine("num5", ALPHABET_num5, TRANSITIONS_num5),
    6: Machine("num6", ALPHABET_num6, TRANSITIONS_num6),
    7: Machine("num7", ALPHABET_num7, TRANSITIONS_num7),
    8: Machine("num8", ALPHABET_num8, TRANSITIONS_num8),
    9: Machine("num9", ALPHABET_num9, TRANSITIONS_num9),
    10: Machine("num10", ALPHABET_num10, TRANSITIONS_num10),
    11: Machine("num11", ALPHABET_num11, TRANSITIONS_num11),
    13: Machine("num13", ALPHABET_num13, TRANSITIONS_num13),
    14: Machine("num14", ALPHABET_num14, TRANSITIONS_num14),
    15: Machine("num15", ALPHABET_num15, TRANSITIONS_num15)
}