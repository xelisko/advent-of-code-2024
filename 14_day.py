import time
import math
from PIL import Image
import numpy as np
import re


class area:
    def __init__(self, positions, velocity):
        self.rows = 103
        self.columns = 101
        grid = [[0 for i in range(self.columns)] for i in range(self.rows)]
        self.grid = grid
        self.robots = positions
        self.v = velocity
        self.d_min = 1000000000000

    def get_grid(self):
        for row in self.grid:
            print(row)

    def get_quantrants(self, time_stamp=1):
        product = 1
        a = 0
        for i in range(2):
            if i == 0:
                top_part = self.grid[0 : self.rows // 2]
            else:
                top_part = self.grid[self.rows // 2 + 1 :]
            left_part = [row[0 : self.columns // 2] for row in top_part]
            right_part = [row[self.columns // 2 + 1 :] for row in top_part]
            product *= np.sum(left_part)
            product *= np.sum(right_part)

        return product

    def convert_to_textfile(self, i):
        f = open(f"14_out_{i}.txt", "w")
        for row in self.grid:
            line = " ".join(map(str, row))
            f.write(line + "\n")
        f.close()

    def generate_image(self, i):
        # Create a new image with mode '1' for 1-bit pixels (black and white)
        image = Image.new("RGB", (self.columns, self.rows))
        colors = {
            0: (255, 255, 255),  # White
            1: (0, 0, 0),  # Black
            2: (255, 0, 0),  # Red
            3: (0, 255, 0),
        }
        # Set pixels based on the array values
        for y in range(self.rows):
            for x in range(self.columns):
                image.putpixel((x, y), colors[self.grid[y][x]])

        # Save the image
        image.save(f"14_img_{i}.png")

    def moveRobot(self):
        time_steps = 100
        for i in range(time_steps):
            self.grid = [[0 for i in range(self.columns)] for i in range(self.rows)]
            for id in range(len(self.robots)):
                vx, vy = self.v[id]
                x, y = self.robots[id]
                newx, newy = x + vx, y + vy
                newx, newy = self.check_wrap(newx, newy)
                self.robots[id] = [newx, newy]
                # mark the final position for that time step
                self.grid[newy][newx] += 1
            # check the symmetry for xmas tree
            p = self.get_quantrants(i)
            self.check_xmas(i)

    def check_xmas(self, time_step):
        d_center = 0
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                # calculate Euclidean distance to the centre
                euclidean = math.sqrt((i - self.rows) ** 2 + (j - self.columns) ** 2)
                if item != 0:
                    d_center += euclidean * item

        if d_center < self.d_min:
            self.d_min = d_center
            print(time_step, d_center)
            self.generate_image(time_step)

    def check_wrap(self, newx, newy):

        if newx < 0:  # wrap to back
            newx = self.columns + newx
        elif newx >= self.columns:
            newx = newx - self.columns

        if newy < 0:  # wrap to back
            newy = self.rows + newy
        elif newy >= self.rows:  # wrap to front
            newy = newy - self.rows
        return newx, newy


def main():
    f = open("14_puzzle.txt", "r")
    line = f.readline().strip()
    positions = []
    velocities = []

    while line:
        px, py, vx, vy = list(map(int, re.findall(r"-?\d+", line)))
        # print(px, py, vx, vy)
        positions.append([px, py])
        velocities.append([vx, vy])

        line = f.readline().strip()

    object = area(positions=positions, velocity=velocities)
    object.moveRobot()
    safety_factor = object.get_quantrants()
    print(safety_factor)

    return 0


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
