import time


def is_possible(target: int, acc, xs: list[int]):
    if len(xs) == 0:
        return acc == target
    return (
        is_possible(target, xs[1:], acc=acc + xs[0])
        or is_possible(target, xs[1:], acc=acc * xs[0])
        or is_possible(target, xs[1:], acc=int(str(acc) + str(xs[0])))
    )


def main():
    total = 0
    with open("07_puzzle.txt") as f:
        for line in f:
            parts = line.split(" ")
            result = int(parts[0][:-1])
            values = list(map(int, parts[1:]))
            if is_possible(result, values[0], values[1:]):
                print(result, "is possible")
                total += result
    print(total)
    return 0


if __name__ == "__main__":
    main()
