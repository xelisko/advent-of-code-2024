import time

from dataclasses import dataclass
from enum import Enum


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
        self.visited_corners = []
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
                    print("started with", plant)
                    # start tracing the region - Task 1
                    a, n = self.find_all_tiles_in_region(i, j, plant)
                    price += a * (4 * a - n)
                    self.showCounted()

                    # start tracing outline for that region
                    number_of_straight_lines = self.calculate_no_of_straight_line(i, j)
                    price_two_starts += a * number_of_straight_lines
                    print("number of straight lines = ", number_of_straight_lines)
                    print("new area = ", a * number_of_straight_lines)
                    # return price
        return price, price_two_starts

    # def for_tile_return_corners(self, x, y) -> list[Corner]:
    #     corner = Corner(x, y)
    #     # for each corner, find out if the four cornering tiles are of different and at the same time same plant tzpe
    #     self.is_an_edge()
    #     self.try_next_corner_to_X_direction(
    #         corner, Direction(+1, 0), regions_plant_type
    #     )

    #     nextCorner = Corner(currCorner.x + direction.x, currCorner.y + direction.y)
    #     return self.is_an_edge(currCorner, nextCorner, plant_of_the_region)

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
        # colour the visited tile
        self.counted[row][col] = 1
        # find any corners of the tile that are on the outline
        # all_visited_corners.append(self.for_tile_return_corners())
        area = 1
        nghbrs = 0
        # if: within bounds, match, uncounted
        if self.is_next_in_the_same_region(row, col, Direction(+1, 0), plant):
            a, n = self.find_all_tiles_in_region(row, col + 1, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(-1, 0), plant):
            a, n = self.find_all_tiles_in_region(row, col - 1, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(0, +1), plant):
            a, n = self.find_all_tiles_in_region(row + 1, col, plant)
            area += a
            nghbrs += n
        if self.is_next_in_the_same_region(row, col, Direction(0, -1), plant):
            a, n = self.find_all_tiles_in_region(row - 1, col, plant)
            area += a
            nghbrs += n
        return area, nghbrs

    def get_plant_type(self, x, y):
        if x < 0 or y < 0:
            return None
        if x >= self.cols or y >= self.rows:
            return None
        return self.map[y][x]

    def returns_if_belongs_to_region(self, x, y):
        if x < 0 or y < 0:
            return True
        if x >= self.cols or y >= self.rows:
            return True
        return self.counted[y][x] == 1

    def is_an_edge(
        self, prevCorner: Corner, currCorner: Corner, plant_type: str
    ) -> bool:
        # can't be the same, but must be neightbouring
        assert (
            abs(prevCorner.x - currCorner.x) <= 1
            and abs(prevCorner.y - currCorner.y) <= 1
        )
        assert (prevCorner.x != currCorner.x) or (prevCorner.y != currCorner.y)
        assert prevCorner.x == currCorner.x or prevCorner.y == currCorner.y

        if prevCorner.x == currCorner.x:
            if prevCorner.y > currCorner.y:  # up
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y - 1)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y - 1)
                counted0 = self.returns_if_belongs_to_region(
                    prevCorner.x, prevCorner.y - 1
                )
                counted1 = self.returns_if_belongs_to_region(
                    prevCorner.x - 1, prevCorner.y - 1
                )
                return (type0 != type1) and (
                    (type0 == plant_type)
                    or (type1 == plant_type)
                    and (counted0 and counted1)
                )
            else:  # down
                # convert the edge between corners into tiles that have that edge
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y)
                counted0 = self.returns_if_belongs_to_region(prevCorner.x, prevCorner.y)
                counted1 = self.returns_if_belongs_to_region(
                    prevCorner.x - 1, prevCorner.y
                )
                return type0 != type1 and (
                    (type0 == plant_type)
                    or (type1 == plant_type)
                    and (counted0 and counted1)
                )
        else:
            if prevCorner.x > currCorner.x:  # left1
                type0 = self.get_plant_type(prevCorner.x - 1, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x - 1, prevCorner.y - 1)
                counted0 = self.returns_if_belongs_to_region(
                    prevCorner.x - 1, prevCorner.y
                )
                counted1 = self.returns_if_belongs_to_region(
                    prevCorner.x - 1, prevCorner.y - 1
                )
                return type0 != type1 and (
                    (type0 == plant_type)
                    or (type1 == plant_type)
                    and (counted0 and counted1)
                )
            else:  # right
                type0 = self.get_plant_type(prevCorner.x, prevCorner.y)
                type1 = self.get_plant_type(prevCorner.x, prevCorner.y - 1)
                counted0 = self.returns_if_belongs_to_region(prevCorner.x, prevCorner.y)
                counted1 = self.returns_if_belongs_to_region(
                    prevCorner.x, prevCorner.y - 1
                )
                return type0 != type1 and (
                    (type0 == plant_type)
                    or (type1 == plant_type)
                    and (counted0 and counted1)
                )

    def check_for_embedded_regions(
        self, all_corners: list[Corner], plant_type: str
    ) -> bool:
        # for corner in all_corners:
        #     if self.map[corner.y][corner.x] != plant_type:
        #         return self.map[corner.y][corner.x]
        return "nic"

    def calculate_no_of_straight_line(self, row: int, col: int) -> int:
        plant_of_the_region = self.get_plant_type(col, row)
        all_visited_corners, all_directions = self.tracing_outline_of_region(
            Corner(col, row), [Corner(col, row)], plant_of_the_region, []
        )

        direction_first_last_corner = Direction(
            all_visited_corners[0].x - all_visited_corners[-1].x,
            all_visited_corners[0].y - all_visited_corners[-1].y,
        )
        all_directions.append(direction_first_last_corner)
        no_of_straight_lines = self.numberOfDirectionChanges(all_directions)
        print(self.check_for_embedded_regions(all_visited_corners, plant_of_the_region))
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
            and nextCorner not in all_corners
        )

    def tracing_outline_of_region(
        self,
        currCorner: Corner,
        all_corners: list[Corner],
        plant_of_the_region: str,
        all_directions: list[Direction],
    ):
        print(currCorner, plant_of_the_region)
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
    with open("12_input.txt") as f:
        for line in f:
            space.append(line.strip())

    garden = Garden(space)
    garden.showMap()
    price1, price2 = garden.get_plant_type_price_for_fence()
    print("price start one = ", price1)
    print("price start two = ", price2)


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
