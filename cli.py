import sys
from turing import run, TuringError
from examples.registry import TASKS


def print_usage():
    print("Использование:")
    print("  python cli.py run <номер задачи>")
    print("Доступные задачи:", sorted(TASKS))


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "run":
        print_usage()
        return

    try:
        num = int(sys.argv[2])
    except ValueError:
        print(f"Номер задачи должен быть числом, а не {sys.argv[2]!r}")
        return

    if num not in TASKS:
        print(f"Задача {num} не найдена. Доступные: {sorted(TASKS)}")
        return

    machine = TASKS[num]
    word = input().strip()
    try:
        print(run(word, machine))
    except TuringError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()