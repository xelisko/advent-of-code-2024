import time
import uuid

from dataclasses import dataclass
from enum import Enum
import numpy as np


@dataclass
class Corner:
    x: int
    y: int


@dataclass
class Direction:
    x: int
    y: int


class Garden:
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.outline_corners = set()
        self.counted = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def showMap(self):
        for row in self.map:
            print(row)

    def showCounted(self):
        for row in self.counted:
            print(row)

    def get_plant_type_price_for_fence(self):
        price = 0
        price_two_starts = 0
        for i, row in enumerate(self.map):
            for j, plant in enumerate(row):
                # checks if already processed
                if self.counted[i][j] == 0:
                    self.outline_corners = set()
                    # start tracing the region - Task 1
                    a, n = self.find_all_tiles_in_region(i, j, plant)
                    # price += a * (4 * a - a * n)

                    number_of_straight_lines = self.calculate_no_of_straight_line(i, j)
                    price_two_starts += a * number_of_straight_lines
                    # print("new area = ", a, number_of_straight_lines)
        return price, price_two_starts

    def for_tile_return_corners(self, x: int, y: int, plant_type: str) -> list[Corner]:
        top_left = Corner(x, y)
        top_right = Corner(x + 1, y)
        bottom_left = Corner(x, y + 1)
        bottom_right = Corner(x + 1, y + 1)

        if self.is_an_edge(top_left, top_right, plant_type):
            self.outline_corners.add(tuple((top_left.x, top_left.y)))
            self.outline_corners.add(tuple((top_right.x, top_right.y)))
        if self.is_an_edge(top_right, bottom_right, plant_type):
            self.outline_corners.add(tuple((top_right.x, top_right.y)))
            self.outline_corners.add(tuple((bottom_right.x, bottom_right.y)))
        if self.is_an_edge(bottom_right, bottom_left, plant_type):
            self.outline_corners.add(tuple((bottom_right.x, bottom_right.y)))
            self.outline_corners.add(tuple((bottom_left.x, bottom_left.y)))
        if self.is_an_edge(bottom_left, top_left, plant_type):
            self.outline_corners.add(tuple((bottom_left.x, bottom_left.y)))
            self.outline_corners.add(tuple((top_left.x, top_left.y)))

    def is_next_in_the_same_region(
        self, row: int, col: int, direction: Direction, regions_plant_type: str
    ) -> bool:
        if not (
            col + direction.x < self.cols and row + direction.y < self.rows
        ) or not (col + direction.x >= 0 and row + direction.y >= 0):
            return False
        if self.map[row + direction.y][col + direction.x] == regions_plant_type:
            if self.counted[row + direction.y][col + direction.x] == 0:
                return True
        return False

    def find_all_tiles_in_region(self, row, col, plant):
        # colour the visited tile and get all its outline corners
        self.for_tile_return_corners(col, row, plant)
        self.counted[row][col] = 1
        area = 1
        nghbrs = 0
        # if: within bounds, match, uncounted
        if self.is_next_in_the_same_region(row, col, Direction(+1, 0), plant):
            nghbrs += 1
            a, n = self.find_all_tiles_in_region(row, col + 1, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(-1, 0), plant):
            nghbrs += 1
            a, n = self.find_all_tiles_in_region(row, col - 1, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(0, +1), plant):
            nghbrs += 1
            a, n = self.find_all_tiles_in_region(row + 1, col, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(0, -1), plant):
            nghbrs += 1
            a, n = self.find_all_tiles_in_region(row - 1, col, plant)
            area += a
            nghbrs += n
        return area, nghbrs

    def get_plant_type(self, x: int, y: int):
        if x < 0 or y < 0:
            return None
        if x >= self.cols or y >= self.rows:
            return None
        return self.map[y][x]

    def returns_if_belongs_to_region(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return True
        if x >= self.cols or y >= self.rows:
            return True
        return self.counted[y][x] == 1

    def is_an_edge(
        self, prevCorner: Corner, currCorner: Corner, plant_type: str
    ) -> bool:
        if prevCorner.x == currCorner.x:
            if prevCorner.y > currCorner.y:  # up
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y - 1)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y - 1)
                return (type0 != type1) and (
                    (type0 == plant_type) or (type1 == plant_type)
                )
            else:  # down
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y)
                return type0 != type1 and (
                    (type0 == plant_type) or (type1 == plant_type)
                )
        else:
            if prevCorner.x > currCorner.x:  # left
                type0 = self.get_plant_type(prevCorner.x - 1, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y - 1)
                return type0 != type1 and (
                    (type0 == plant_type) or (type1 == plant_type)
                )
            else:  # right
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x, prevCorner.y - 1)
                return type0 != type1 and (
                    (type0 == plant_type) or (type1 == plant_type)
                )

    def calculate_no_of_straight_line(self, row: int, col: int) -> int:
        plant_of_the_region = self.get_plant_type(col, row)
        no_of_straight_lines = 0
        # gather all the outline corners and directions
        while len(self.outline_corners) != 0:
            corners, directions = self.tracing_outline_of_region(
                Corner(col, row), [Corner(col, row)], plant_of_the_region, []
            )
            direction_first_last_corner = Direction(
                corners[0].x - corners[-1].x,
                corners[0].y - corners[-1].y,
            )
            directions.append(direction_first_last_corner)
            if len(self.outline_corners):
                col, row = self.outline_corners.pop()

            # calculate the number of stright lines
            n = self.numberOfDirectionChanges(directions)
            no_of_straight_lines += n
        # print("straight lines", no_of_straight_lines)
        return no_of_straight_lines

    def numberOfDirectionChanges(self, all_directions: list[Direction]) -> int:
        count = 0
        for i in range(len(all_directions) - 1):
            if all_directions[i] != all_directions[i + 1]:
                count += 1
        return count + 1

    def sameCorner(self, corner1: Corner, corner2: Corner) -> bool:
        return corner1.x == corner2.x and corner1.y == corner2.y

    def try_next_corner_to_X_direction(
        self,
        currCorner: Corner,
        direction: Direction,
        plant_of_the_region: str,
        all_corners: list[Corner],
    ) -> bool:
        nextCorner = Corner(currCorner.x + direction.x, currCorner.y + direction.y)
        # if next corner is not the previous corner and they create and edge
        return (
            self.sameCorner(currCorner, nextCorner) == False
            and self.is_an_edge(currCorner, nextCorner, plant_of_the_region)
            and tuple((nextCorner.x, nextCorner.y)) in self.outline_corners
            and nextCorner not in all_corners
        )

    def tracing_outline_of_region(
        self,
        currCorner: Corner,
        all_corners: list[Corner],
        plant_of_the_region: str,
        all_directions: list[Direction],
    ):
        # print(currCorner, plant_of_the_region)
        self.outline_corners.discard(tuple((currCorner.x, currCorner.y)))
        # try right
        if self.try_next_corner_to_X_direction(
            currCorner, Direction(x=+1, y=0), plant_of_the_region, all_corners
        ):
            nextCorner = Corner(currCorner.x + 1, currCorner.y + 0)
            all_corners.append(nextCorner)
            all_directions.append(Direction(+1, 0))
            self.tracing_outline_of_region(
                nextCorner, all_corners, plant_of_the_region, all_directions
            )
        # try down
        elif self.try_next_corner_to_X_direction(
            currCorner, Direction(x=0, y=+1), plant_of_the_region, all_corners
        ):
            nextCorner = Corner(currCorner.x + 0, currCorner.y + 1)
            all_corners.append(nextCorner)
            all_directions.append(Direction(0, 1))
            self.tracing_outline_of_region(
                nextCorner, all_corners, plant_of_the_region, all_directions
            )
        # try up
        if self.try_next_corner_to_X_direction(
            currCorner, Direction(x=0, y=-1), plant_of_the_region, all_corners
        ):
            nextCorner = Corner(currCorner.x + 0, currCorner.y - 1)
            all_corners.append(nextCorner)
            all_directions.append(Direction(0, -1))
            self.tracing_outline_of_region(
                nextCorner, all_corners, plant_of_the_region, all_directions
            )
        # try left
        elif self.try_next_corner_to_X_direction(
            currCorner, Direction(x=-1, y=0), plant_of_the_region, all_corners
        ):
            nextCorner = Corner(currCorner.x - 1, currCorner.y + 0)
            all_corners.append(nextCorner)
            all_directions.append(Direction(-1, 0))
            self.tracing_outline_of_region(
                nextCorner, all_corners, plant_of_the_region, all_directions
            )
        return [all_corners, all_directions]


def main():

    space = []
    with open("12_puzzle.txt") as f:
        for line in f:
            space.append(line.strip())

    garden = Garden(space)
    # garden.showMap()
    price1, price2 = garden.get_plant_type_price_for_fence()
    # print("price start one = ", price1)
    print("price start two = ", price2)


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
