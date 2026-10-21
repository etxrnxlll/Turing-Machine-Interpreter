"""
Универсальный интерпретатор машины Тьюринга.

Модель: машина работает на ленте, инициализируемой входным словом.
Переход: (состояние, читаемый_символ) -> (записываемый_символ, сдвиг, новое_состояние).
Пустой символ — 'λ'. Условие остановки — состояние 'STOP'.
Подробные конвенции и описание модели см. в README.md.
"""

from dataclasses import dataclass

from typing import TypeAlias

TransitionTable: TypeAlias = dict[tuple[str, str], tuple[str, str, str]]
Alphabet: TypeAlias = set[str]
DirectionsMap: TypeAlias = dict[str, int]


@dataclass
class Machine:
    name: str
    alphabet: Alphabet
    transitions: TransitionTable
    start_state: str = "q0"

class TuringError(Exception):
    pass
# направления головки
MOVES = {"R": 1, "L": -1, "N": 0}

MAX_STEPS = 10000


def _grow_left(tape: list, pos: int) -> int:
    tape.insert(0, "λ")
    return pos + 1


def _grow_right(tape: list, pos: int) -> int:
    tape.append("λ")
    return pos


def _validate_transitions(machine: Machine, moves: DirectionsMap) -> None:
    transitions = machine.transitions
    alphabet = machine.alphabet
    start_state = machine.start_state

    defined = {state for (state, _) in transitions}
    reachable = set()
    if start_state != "STOP" and start_state not in defined:
        raise TuringError(
            f"Стартовое состояние {start_state!r} отсутствует в таблице"
        )

    for (state, symbol), (write, move, new_state) in transitions.items():
        if state == "STOP":
            raise TuringError(
                f"Переход из STOP: (STOP, {symbol!r})"
            )

        if symbol not in alphabet and symbol != "λ":
            raise TuringError(
                f"Символ чтения {symbol!r} не в алфавите и не λ, "
                f"ключ (state={state!r})"
            )

        if move not in moves:
            raise TuringError(
                f"Неизвестный ход {move!r} в переходе "
                f"({state!r}, {symbol!r})"
            )

        if write not in alphabet and write != "λ":
            raise TuringError(
                f"Символ записи {write!r} не в алфавите и не λ, "
                f"переход ({state!r}, {symbol!r})"
            )

        if new_state != "STOP":
            reachable.add(new_state)

    # DFS: порядок обхода не важен, нам нужно только множество достижимых состояний
    if start_state == "STOP":
        visited = set(defined)
    else:
        visited = {start_state}
    stack = [start_state]
    while stack:
        current = stack.pop()
        for (state, _), (_, _, new_state) in transitions.items():
            if state != current:
                continue
            if new_state == "STOP":
                continue
            if new_state in visited:
                continue
            visited.add(new_state)
            stack.append(new_state)

    undefined = defined - visited
    if undefined:
        raise TuringError(
            f"Недостижимые состояния: {sorted(undefined)}"
        )

    dangling = reachable - defined
    if dangling:
        raise TuringError(
            f"Состояния без строк в таблице: {sorted(dangling)}"
        )


def _ensure_bounds(tape: list, pos: int) -> int:
    while pos < 0 or pos >= len(tape):
        if pos < 0:
            pos = _grow_left(tape, pos)
        else:
            pos = _grow_right(tape, pos)
    return pos


def run(word: str, machine: Machine, moves: DirectionsMap = MOVES) -> str:
    """Прогнать машину Тьюринга на слове и вернуть результат.

    Аргументы:
        word: входное слово, только символы из machine.alphabet.
        machine: спецификация машины — имя, алфавит, таблица переходов,
            стартовое состояние.
        moves: словарь направлений головки; по умолчанию MOVES.
            Ключи — имена ходов ("R", "L", "N"), значения — смещение по ленте.

    Возвращает:
        Слово с ленты после остановки машины, без λ по краям.

    Поднимает:
        TuringError: если таблица переходов битая (неизвестный ход,
            символ вне alphabet или λ, переход из STOP, недостижимое
            или отсутствующее состояние), если во входе есть символ
            вне alphabet, если для пары (состояние, символ) нет перехода
            или если машина не остановилась за MAX_STEPS шагов.

    Конвенция:
        Головка стартует на позиции 0 (начало слова). Пустой символ — λ.
        Позиция головки после остановки наружу не возвращается; конвенция
        конкретной машины (например, «вернуть головку в начало слова»)
        задаётся её таблицей переходов, а не интерпретатором.
        Таблица не обязана быть тотальной.
        Если для пары (состояние, символ) строки нет — это не ошибка валидации,
        а ошибка времени прогона. Проверка на тотальность не делается.
        Валидация таблицы выполняется при каждом вызове run, а не при создании Machine.
        Причина: валидация зависит от moves, который передаётся в run, а не хранится в спецификации.
    """
    transitions = machine.transitions
    alphabet = machine.alphabet
    state = machine.start_state

    _validate_transitions(machine, moves)

    for i, ch in enumerate(word):
        if ch not in alphabet:
            raise TuringError(
                f"Символ вне алфавита: {ch!r}, позиция={i}"
            )

    tape = list(word)
    pos = 0
    step = 0

    while state != "STOP":
        if step >= MAX_STEPS:
            raise TuringError(
                f'Машина не остановилась за {MAX_STEPS} шагов '
                f'(состояние={state}, позиция={pos})'
            )

        pos = _ensure_bounds(tape, pos)

        symbol = tape[pos]
        key = (state, symbol)

        if key not in transitions:
            raise TuringError(
                f"Нет перехода: состояние={state}, символ={symbol!r}, позиция={pos}"
            )

        write, move, new_state = transitions[key]
        tape[pos] = write

        pos += moves[move]
        state = new_state
        step += 1

    return "".join(tape).strip("λ")