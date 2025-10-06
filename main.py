import os
import time
from copy import deepcopy
from math import tan, radians, degrees, atan, floor

x_step = 1
ray_degrees = degrees(atan(2/3))
world_size = 40
ray_y = 0


class Position2D:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Position2D'):
        return self.__init__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Position2D'):
        return self.__init__(other.x - self.x, other.y - self.y)

    def __eq__(self, other: 'Position2D'):
        return (self.x == other.x) and (self.y == other.y)


class Voxel:
    position: Position2D
    triggered: bool  # whether a ray hit the voxel
    enabled: bool  # whether the ray is enabled
    voxel_out: str = " "

    def __init__(self, position: Position2D, enabled: bool = False, triggered: bool = False):
        self.position = position
        self.triggered = triggered
        self.enabled = enabled

    def __eq__(self, other: 'Voxel'):
        return self.position == other.position


voxel_world: list[list[Voxel]] = []
for x in range(world_size):
    x_axis = []

    for y in range(world_size):
        x_axis.append(Voxel(Position2D(x, y)))

    voxel_world.append(x_axis)


# previous_y_position = 0


def small_step_find(voxel_matrix: list[list[Voxel]], y_step: float) -> list[Voxel]:
    """
    Finds voxels that are within the ray's path — used when the absolute value of the step is <= 0.5 (aka 45
    degrees). Do not use this function — use `find_voxels(...)` instead.
    :param voxel_matrix:
    :param y_step:
    :return:
    """
    found_voxels = []
    max_value = len(voxel_matrix)
    # global previous_y_position

    for i, x_axis in enumerate(voxel_matrix):
        y_position = floor(y_step * (i + 1)) + ray_y

        if (y_position >= max_value) or (y_position < 0):
            continue

        # if y_position != previous_y_position:
        #     previous_y_position = y_position
        #     found_voxels.append(voxel_matrix[i - 1][y_position])

        found_voxels.append(x_axis[y_position])

    return found_voxels


def large_step_find(voxel_matrix: list[list[Voxel]], x_step: float) -> list[Voxel]:
    """
    Finds voxels that are within the ray's path — used when the absolute value of the step is larger than 0.5 (aka 45
    degrees). Do not use this function — use `find_voxels(...)` instead.
    :param voxel_matrix:
    :param x_step:
    :return:
    """
    found_voxels = []
    max_value = len(voxel_matrix)

    for y in range(len(voxel_matrix)):
        x_position = floor(abs(x_step * (y + 0)))

        if x_step < 0:
            y = -y

        if (y + ray_y >= max_value) or (y + ray_y < 0):
            continue

        # print(x_step * (y + 0), x_position, y + ray_y)

        found_voxels.append(voxel_matrix[x_position][y + ray_y])

    # transpose(found_voxels)

    return found_voxels


# I'm going to assume that x_step = 1 — no reason for it to be otherwise.
def find_voxels(voxel_matrix: list[list[Voxel]], y_step: float) -> list[Voxel]:
    if -1 <= y_step <= 1:
        return small_step_find(voxel_matrix, y_step)

    return large_step_find(voxel_matrix, 1 / y_step)


def enable_voxels(voxel_matrix: list[list[Voxel]], enabled_voxels: list[Voxel]):
    """
    Takes a matrix of voxels, and enables voxels based on `enabled_voxels`.
    :param voxel_matrix: The matrix of voxels to modify. Does not create a deep copy!
    :param enabled_voxels: The voxels that are enabled.
    """
    for voxel in enabled_voxels:
        # voxel_matrix[voxel.position.x][voxel.position.y].voxel_out = "▓"
        voxel_matrix[voxel.position.x][voxel.position.y].triggered = voxel.enabled
        voxel_matrix[voxel.position.x][voxel.position.y].voxel_out = "▒" if not voxel.enabled else "▓"

        if voxel.enabled: return


def print_voxels(voxel_matrix: list[list[Voxel]]):
    # [y][x]
    zero_array = [0] * len(voxel_matrix)
    print_buf: list[list[int]] = []

    for i in range(len(zero_array)):
        print_buf.append(deepcopy(zero_array))

    for i, x_axis in enumerate(voxel_matrix):
        for j, voxel in enumerate(x_axis):
            print_buf[j][i] = voxel.voxel_out

    print_buf.reverse()

    for x_axis in print_buf:
        for y_value in x_axis:
            # print(y_value)
            print(y_value, end=" ")

        print()


def main():
    ray_radians = radians(ray_degrees)
    y_step = tan(ray_radians)
    triggered_voxels = find_voxels(voxel_world, y_step)
    enable_voxels(voxel_world, triggered_voxels)
    print_voxels(voxel_world)


if __name__ == "__main__":
    # ray_y = floor((world_size / 2) - 1)
    ray_y = 9
    angle_step = 2/3

    for i in range(10):
        voxel_world[9][i + 5].enabled = True

    for i in range(10):
        voxel_world[12][i + 10].enabled = True

    voxel_world[3][9].enabled = True

    for i in range(floor(180 / angle_step)):
        start = time.time()
        # frac = input("Type in degrees: ")
        os.system("clear")
        # ray_degrees = degrees(atan(eval(frac)))
        ray_degrees = (i * angle_step) - 90

        main()
        end = time.time()

        print(end - start)
        time.sleep((1 / 45) - (end - start))

    # ray_degrees = -90
    # main()
