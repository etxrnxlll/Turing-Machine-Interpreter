from turing import Machine, run, TuringError


# тестовый алфавит ядра, не связанный с примерами
ALPHABET = {"a", "b"}


BAD_TABLE_BAD_MOVE = {
    ("q0", "a"): ("a", "S", "STOP"),
}


BAD_TABLE_BAD_WRITE = {
    ("q0", "a"): ("c", "R", "STOP"),
}


BAD_TABLE_FROM_STOP = {
    ("q0", "a"): ("a", "R", "STOP"),
    ("STOP", "a"): ("a", "R", "STOP"),
}


BAD_TABLE_DANGLING = {
    ("q0", "a"): ("a", "R", "q9"),
}


BAD_TABLE_NO_START = {
    ("q1", "a"): ("a", "R", "STOP"),
}


BAD_TABLE_BAD_WRITE_LAMBDA = {
    ("q0", "λ"): ("c", "R", "STOP"),
}


BAD_TABLE_BAD_READ = {
    ("q0", "c"): ("a", "R", "STOP"),
}


BAD_TABLE_UNREACHABLE = {
    ("q0", "a"): ("a", "R", "STOP"),
    ("q7", "a"): ("a", "R", "STOP"),   # q7 есть в ключах, но в него никто не ведёт
}


HOLE_TABLE = {
    ("q0", "a"): ("a", "R", "q1"),
    ("q1", "a"): ("a", "R", "STOP"),
}


BAD_TABLES = [
    BAD_TABLE_BAD_MOVE,
    BAD_TABLE_BAD_WRITE,
    BAD_TABLE_FROM_STOP,
    BAD_TABLE_DANGLING,
    BAD_TABLE_NO_START,
    BAD_TABLE_BAD_WRITE_LAMBDA,
    BAD_TABLE_BAD_READ,
    BAD_TABLE_UNREACHABLE,
]


MOVE_N_TABLE = {
    ("q0", "a"): ("b", "N", "q0"),   # увидели a — стали b и остались на месте
    ("q0", "b"): ("b", "R", "q0"),   # увидели b — поехали вправо
    ("q0", "λ"): ("λ", "N", "STOP"), # упёрлись в край — стоим и стоп
}


CASES_OK_MOVE_N = [
    ("", ""),
    ("a", "b"),
    ("aa", "bb"),
    ("aab", "bbb"),
]


def test_bad_tables():
    for tbl in BAD_TABLES:
        bad = Machine("bad", ALPHABET, tbl)
        try:
            run("a", bad)
        except TuringError:
            pass
        else:
            assert False, f"ждали ошибку на битой таблице {tbl!r}"


def test_runtime_hole():
    bad = Machine("hole", ALPHABET, HOLE_TABLE)
    try:
        run("b", bad)
    except TuringError:
        pass
    else:
        assert False, "ждали ошибку 'нет перехода' на дырке в легальной таблице"


def test_move_n():
    machine_n = Machine("move_n", ALPHABET, MOVE_N_TABLE)
    for inp, expected in CASES_OK_MOVE_N:
        got = run(inp, machine_n)
        assert got == expected, f"вход={inp!r}: ждали {expected!r}, получили {got!r}"


def test_start_at_stop():
    """Машина, которая стартует сразу в STOP, ничего не делает и не падает на валидации."""
    m = Machine(
        "noop",
        ALPHABET,
        {("q0", "a"): ("a", "R", "STOP")},
        start_state="STOP",
    )
    assert run("a", m) == "a"


def test_empty_word():
    """Пустой вход на легальной машине не должен ломаться."""
    m = Machine(
        "empty",
        ALPHABET,
        {
            ("q0", "a"): ("a", "R", "q0"),
            ("q0", "λ"): ("λ", "N", "STOP"),
        },
    )
    assert run("", m) == ""


def test_max_steps():
    """Машина, которая крутится на месте, должна поднять TuringError про MAX_STEPS."""
    loop = Machine(
        "loop",
        ALPHABET,
        {("q0", "a"): ("a", "N", "q0")},
    )
    try:
        run("a", loop)
    except TuringError as e:
        assert "не остановилась" in str(e), \
            f"ждали ошибку про MAX_STEPS, получили: {e}"
    else:
        assert False, "ждали ошибку про MAX_STEPS, а run вернул результат"