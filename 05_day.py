def main():
    file = open("05_puzzle.txt", "r")
    line = file.readline().strip()

    rule_dict = dict()

    # read all the rules and save to dictionary
    while line != "":
        line1 = line.split("|")
        x, y = int(line1[0]), int(line1[1])

        if rule_dict.get(x) != None:
            existing = rule_dict.get(x)
            if isinstance(existing, int):
                rule_dict[x] = [existing, y]
            else:
                rule_dict[x] = existing + [y]
        else:
            rule_dict[x] = y

        line = file.readline().strip()

    # check the existing orders
    line = file.readline().strip()
    sum = 0
    incorrect_orders = []
    while line:
        tokens = list(map(int, line.split(",")))

        valid = checkValidity(tokens, rule_dict)

        # add up the middle value
        if valid:
            middle_index = len(tokens) // 2
            middle_value = tokens[middle_index]
            sum += middle_value
        else:
            incorrect_orders.append(tokens)

        line = file.readline().strip()

    print("sum part 1 =", sum)

    sum1 = 0
    for order in incorrect_orders:
        correct = correctOrder(order, rule_dict)
        sum1 += correct[len(correct) // 2]

    print("sum part 2 =", sum1)
    return 0


def checkValidity(tokens, rules_dict):
    prev_tokens = []

    for token in tokens:
        if not prev_tokens:
            prev_tokens.append(token)
            continue

        cannot_be_before = rules_dict.get(token)

        if not cannot_be_before:
            prev_tokens.append(token)
            continue

        if isinstance(cannot_be_before, int):
            if cannot_be_before in prev_tokens:
                return False
            prev_tokens.append(token)
            continue

        for page in prev_tokens:
            if page in cannot_be_before:
                return False

        prev_tokens.append(token)
    return True


def correctOrder(order, rules_dict):
    prev_ids = []

    # let's swap the ones that are in an incorrect order
    for id in order:
        prev_ids.append(id)

        # get the dictionary entry
        no_go_ids = rules_dict.get(id)

        if len(prev_ids) == 0:
            continue

        # if no rules
        if no_go_ids == None:
            continue

        # if only 1 rule -> convert int to list
        if isinstance(no_go_ids, int):
            no_go_ids = [no_go_ids]

        # loop through
        j = 0
        # reverse the array, so the checking happens from the end
        prev_ids = prev_ids[::-1]

        for i, prev in enumerate(prev_ids):
            if prev in no_go_ids:
                prev_ids[i], prev_ids[j] = prev_ids[j], prev_ids[i]
                j = i
        # reverse back
        prev_ids = prev_ids[::-1]

    return prev_ids


if __name__ == "__main__":
    main()
