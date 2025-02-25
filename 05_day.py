def main():
    page_order_rules_dict = dict()
    sum = 0
    sum_star_2 = 0
    incorrectly_ordered_pages = []
    part_A = True

    with open("05_puzzle.txt") as file:
        for line in file:
            if line == "\n":
                part_A = False
                continue

            # read all the rules and save to dictionary
            if part_A:
                page_before_Y, Y = list(map(int, line.strip().split("|")))

                if page_before_Y not in page_order_rules_dict.keys():
                    page_order_rules_dict[page_before_Y] = [Y]
                else:
                    existing = page_order_rules_dict.get(page_before_Y)
                    existing.append(Y)
                    page_order_rules_dict[page_before_Y] = existing

            else:
                # check the existing orders
                pages = list(map(int, line.strip().split(",")))

                valid = checkValidity(pages, page_order_rules_dict)

                if valid:
                    sum += pages[len(pages) // 2]
                else:
                    incorrectly_ordered_pages.append(pages)

        print("sum part 1 =", sum)

        for update in incorrectly_ordered_pages:
            correctly_ordered_update = correctOrder(update, page_order_rules_dict)
            sum_star_2 += correctly_ordered_update[len(correctly_ordered_update) // 2]

        print("sum part 2 =", sum_star_2)
    return 0


def checkValidity(
    pages: list[int], page_order_rules_dict: dict[int, list[int]]
) -> bool:
    prev_pages = []

    for curr_page in pages:
        prev_pages.append(curr_page)
        if (prev_pages) == 1:
            continue

        if curr_page not in page_order_rules_dict.keys():
            continue

        pages_after_curr_page = page_order_rules_dict.get(curr_page)

        for prev_page in prev_pages:
            if prev_page in pages_after_curr_page:
                return False

    return True


def correctOrder(
    update: list[int], page_order_rules_dict: dict[int, list[int]]
) -> list[int]:
    prev_pages = []

    # let's swap the ones that are in an incorrect order
    for curr_page in update:
        prev_pages.append(curr_page)

        if len(prev_pages) == 1 or curr_page not in page_order_rules_dict.keys():
            continue
        must_be_after_curr_page = page_order_rules_dict.get(curr_page)

        # reverse the array, so the checking happens from the end
        prev_pages = prev_pages[::-1]
        j = 0
        for i, prev_page in enumerate(prev_pages):
            if prev_page in must_be_after_curr_page:
                prev_pages[i], prev_pages[j] = prev_pages[j], prev_pages[i]
                j = i
        # reverse back
        prev_pages = prev_pages[::-1]

    return prev_pages


if __name__ == "__main__":
    main()
