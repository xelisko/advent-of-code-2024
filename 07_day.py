import numpy as np
import time


def main():
    start = time.time()

    sum = 0
    with open("07_input.txt") as f:
        for line in f:
            # read and process the line
            values = line.strip().split(" ")
            result = int(values[0][:-1])
            values = list(map(int, values[1:]))

            # get all the combinations of operators
            all_equations = np.array(
                generate_operators_combinations("", len(values) - 1)
            )
            all_equations = all_equations.reshape((-1))
            # print(all_equations)
            # print(len(all_equations), len(values))

            # calculate all the values
            all_results = []
            for operators_in_equation in all_equations:
                intermediate = values[0]
                for i, operator in enumerate(operators_in_equation):
                    if operator == "+":
                        intermediate += values[i + 1]
                    elif operator == "*":
                        intermediate *= values[i + 1]
                    elif operator == "|":
                        intermediate = int(str(intermediate) + str(values[i + 1]))

                all_results.append(intermediate)

            if result in all_results:
                sum += result

    print("sum of the correct equations = ", sum)
    end = time.time()
    print("processing time = ", end - start)
    return 0


def generate_operators_combinations(curr_str: str, n: int) -> list[str]:
    if len(curr_str) == n:
        return str(curr_str)

    combinations = []
    combinations.append(generate_operators_combinations(curr_str + "*", n))
    combinations.append(generate_operators_combinations(curr_str + "+", n))
    combinations.append(generate_operators_combinations(curr_str + "|", n))

    return combinations


if __name__ == "__main__":
    main()
