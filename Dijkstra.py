from enum import Enum
from ConvertMap import convert_address
from typing import List
from ConvertMap import convert
from ConvertMap import paint_map
from config import configC
#
# T, F = True, False
# array = np.asarray(
#     [[T, F, F, T],
#      [T, T, F, T],
#      [F, T, T, F],
#      [T, T, T, T]])
# costs = np.where(array, 1, 1000)
# path, cost = skimage.graph.shortest_path(
#     costs, start=(0, 0), end=(3, 3), fully_connected=True)
#
# print(path)

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Node:
    def __init__(self, coord: list, path=None, weight=0, visited: bool = False):
        if path is None:
            path = []

        self.path: list = path
        self.coord = coord
        self._visited = visited
        self.weight = weight
        # self.North = None
        # self.East = None
        # self.South = None
        # self.West = None

    # def __eq__(self, other):
    #     return self.lastDir == other.position

    def set_visited(self):
        self._visited = True

    def is_visited(self):
        return self._visited

    # def set_weight(self, weight: int):
    #     self.weight = weight


def add_bounds(node: Node, stack: list, node_grid, grid: List[List[bool]], width,
               height) -> None:
    """
    Warning! Coord and cardinal points are mixed up
    :param height: height of grid
    :param width: width of grid
    :param grid: Grid. 0 - blocked, 1 - open
    :return:
    """
    y = node.coord[0]
    x = node.coord[1]
    if y + 1 < height and grid[y + 1][x] and not node.is_visited():
        if not node_grid[y + 1][x]:
            new_dir = node.path.copy()
            new_dir.append(Direction.SOUTH)
            tmp = Node([y + 1, x],new_dir ,node.weight + 1 )
            node_grid[y + 1][x] = tmp
            stack.append(tmp)
        else:
            tmp: Node = node_grid[y + 1][x]
            if tmp.weight > node.weight + 1:
                tmp.weight = node.weight + 1
                tmp.path = node.path.copy()
                tmp.path.append(Direction.SOUTH)

    if y - 1 >= 0 and grid[y - 1][x] and not node.is_visited():
        if not node_grid[y - 1][x]:
            new_dir = node.path.copy()
            new_dir.append(Direction.NORTH)
            tmp = Node([y - 1, x], new_dir, node.weight + 1)
            node_grid[y - 1][x] = tmp
            stack.append(tmp)
        else:
            tmp: Node = node_grid[y - 1][x]
            if tmp.weight > node.weight + 1:
                tmp.weight = node.weight + 1
                tmp.path = node.path.copy()
                tmp.path.append(Direction.NORTH)

    if x + 1 < width and grid[y][x + 1] and not node.is_visited():
        if not node_grid[y][x + 1]:
            new_dir = node.path.copy()
            new_dir.append(Direction.WEST)
            tmp = Node([y, x + 1], new_dir, node.weight + 1 )
            node_grid[y][x + 1] = tmp
            stack.append(tmp)

        else:
            tmp: Node = node_grid[y][x + 1]
            if tmp.weight > node.weight + 1:
                tmp.weight = node.weight + 1
                tmp.path = node.path.copy()
                tmp.path.append(Direction.WEST)

    if x - 1 >= 0 and grid[y][x - 1] and not node.is_visited():
        if not node_grid[y][x - 1]:
            new_dir = node.path.copy()
            new_dir.append(Direction.EAST)
            tmp = Node([y, x - 1], new_dir, node.weight + 1)
            node_grid[y][x - 1] = tmp
            stack.append(tmp)
        else:
            tmp: Node = node_grid[y][x - 1]
            if tmp.weight > node.weight + 1:
                tmp.weight = node.weight + 1
                tmp.path = node.path.copy()
                tmp.path.append(Direction.EAST)


def some_dijkstra(grid: List[List[bool]], pass_coord: [int], height: int, width: int, car_coord: int):
    # grid with len
    res_node_list = []
    node_grid = [[None for w in range(width)] for h in range(height)]
    double_pass_coord: [[int, int]] = [convert_address(s, width) for s in pass_coord]
    double_pass_coord_copy = double_pass_coord.copy()
    #print("Pass coord")
    #print(double_pass_coord)
    #print("Input coord")
    queue = list()
    tmp1 = convert_address(car_coord, width)
    #print(tmp1)
    #print("----------------")
    origNode = Node(tmp1)
    x = tmp1[0]
    y = tmp1[1]
    node_grid[x][y] = origNode
    queue.append(origNode)
    #(double_pass_coord)
    while queue:
        tmp: Node = queue.pop(0)
        add_bounds(tmp, queue, node_grid, grid, width, height)
        tmp.set_visited()


        if not double_pass_coord:
            break

        for coord in double_pass_coord:
            if coord[0] == tmp.coord[0] and coord[1] == tmp.coord[1]:
                res_node_list.append(tmp)
                double_pass_coord.remove(coord)
                break
    ordered_res_node_list = []
    for coord in double_pass_coord_copy:
        flag = False
        for node in res_node_list:
            if node.coord[0] == coord[0] and node.coord[1] == coord[1]:
                ordered_res_node_list.append(node)
                flag = True
                break
        if not flag:
            ordered_res_node_list.append(None)

    return ordered_res_node_list


if __name__ == '__main__':
    t = configC

    pass_arr = []
    car_pos = []
    s = convert(t["grid"], t['width'])
    paint_map(s)
    for a in t["customers"].values():
        pass_arr.append(int(a['origin']))
    for a in t["cars"].values():
        car_pos.append(int(a['position']))
    for a in car_pos:
        nodes, some_t = some_dijkstra(s, pass_arr, t["height"], t["width"], a)
        for i in nodes:
            # row = []
            #print(i.weight)
            #print(i.coord)
            #print(i.path)
            if some_t[i.coord[0]][i.coord[1]]:
                print(some_t[i.coord[0]][i.coord[1]].coord)
            else:
                print(some_t[i.coord[0]][i.coord[1]])

        for i in some_t:
            row = []
            for a in i:
                if a:
                    sl = a.weight
                else:
                    sl = -1
                row.append(sl)
            for rows in row:
                print(f"{rows:3}",end=" ")
            print("\n")
        print("-----------------------------------------------")
        break

# s = [[]]
#
# for i in range(N):
#     pass
