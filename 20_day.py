import time
from dataclasses import dataclass
from queue import SimpleQueue


@dataclass
class Node:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Shortcut:
    start: Node
    end: Node

    def __hash__(self):
        return hash((self.start, self.end))


@dataclass
class Graf:
    grid: list[list[bool]]
    start: Node
    end: Node

    def __init__(self, grid: list[str]):
        self.grid = []
        for j, row in enumerate(grid):
            self.grid.append([])
            for i, char in enumerate(row):
                if char == "S":
                    self.start = Node(i, j)
                elif char == "E":
                    self.end = Node(i, j)
                if char == "#":
                    self.grid[j].append(False)
                elif char in ["S", "E", "."]:
                    self.grid[j].append(True)
                else:
                    assert False

    def neighbours(self, node: Node) -> list[Node]:
        # interval, set
        neighbours = []
        x = node.x
        y = node.y
        if x + 1 < len(self.grid[y]) and self.grid[y][x + 1]:
            neighbours.append(Node(x + 1, y))
        if x - 1 >= 0 and self.grid[y][x - 1]:
            neighbours.append(Node(x - 1, y))
        if y + 1 < len(self.grid) and self.grid[y + 1][x]:
            neighbours.append(Node(x, y + 1))
        if y - 1 >= 0 and self.grid[y - 1][x]:
            neighbours.append(Node(x, y - 1))
        return neighbours

    def get_distances_from(self, first: Node) -> dict[Node, int]:
        distances = dict()
        queue = SimpleQueue()  # of Nodes
        queue.put(first)
        distances[first] = 0
        while not queue.empty():
            node = queue.get()
            d = distances[node]
            for neighbour in self.neighbours(node):
                if neighbour in distances.keys():
                    continue
                distances[neighbour] = d + 1
                queue.put(neighbour)
        return distances

    def find_all_shortcuts(self) -> list[Shortcut]:
        shortcuts = []
        for j, row in enumerate(self.grid):
            for i, is_track in enumerate(row):
                if is_track:
                    continue
                wall = Node(i, j)
                neighbours = self.neighbours(wall)
                if len(neighbours) < 2:
                    continue
                for neighbour in neighbours:
                    new_shortcut = Shortcut(wall, neighbour)
                    shortcuts.append(new_shortcut)
        return shortcuts

    def shortest_distance_of_shortcut(
        self,
        shortcut: Shortcut,
        distances_from_start: dict[Node, int],
        distances_from_end: dict[Node, int],
    ) -> int:
        time_to_end = distances_from_end[shortcut.end]
        closest_to_start = min(
            [
                distances_from_start[neighbour]
                for neighbour in self.neighbours(shortcut.start)
            ]
        )
        return closest_to_start + time_to_end + 2

    def new_distances_using_shorcuts(
        self,
        shorcuts: list[Shortcut],
        distances_from_start: dict[Node, int],
        distances_from_end: dict[Node, int],
    ) -> dict[Shortcut, int]:
        shorcut_distances = dict()
        for shortcut in shorcuts:
            shortest_distance = self.shortest_distance_of_shortcut(
                shortcut, distances_from_start, distances_from_end
            )
            shorcut_distances[shortcut] = shortest_distance
        return shorcut_distances

    def find_how_many_save_Xps(
        self,
        x: int,
        shortest_distance_without_shortcuts: int,
        shorcut_distances: dict[Shortcut, int],
    ) -> int:
        return len(
            list(
                filter(
                    lambda d: shortest_distance_without_shortcuts - d >= x,
                    shorcut_distances.values(),
                )
            )
        )


def main() -> None:
    with open("20_puzzle.txt") as file:
        grid = [line.strip() for line in file]
        graf = Graf(grid)
        distances_from_start = graf.get_distances_from(graf.start)
        distances_from_end = graf.get_distances_from(graf.end)
        assert distances_from_end[graf.start] == distances_from_start[graf.end]
        shortest_distance = distances_from_start[graf.end]
        all_shortcuts_possibilities = graf.find_all_shortcuts()
        shortcut_distances = graf.new_distances_using_shorcuts(
            all_shortcuts_possibilities, distances_from_start, distances_from_end
        )
        x = graf.find_how_many_save_Xps(100, shortest_distance, shortcut_distances)
        print(x)
        return 0


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
