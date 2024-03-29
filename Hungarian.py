from munkres import Munkres, print_matrix, DISALLOWED
from random import randint
from Apathfind import astar
from Dijkstra import some_dijkstra
import ConvertMap as cm
import config
from client import move_car, add_team_and_get_token
from copy import deepcopy

def manipulate_cars(orders, token):
    for order in orders:
        move_car(order[0], order[1], token)


def make_matrix(configM):
    cars_keys = configM['cars'].keys()
    keys = []
    for key in cars_keys:
        keys.append(key)
    grid = configM['grid']
    width = configM['width']
    height = configM['height']
    cars = configM['cars'].values()
    customers = configM['customers'].values()
    # print(customers)
    origins = []
    for i in customers:
        origins.append(i['origin'])
    new = cm.convert(grid, width)
    cm.paint_map(new)
    custom = []
    custom_id = 0
    car_id = 0
    hren = []
    nahuy = []

    for customer in configM['customers'].values():
        s = int(customer['origin'])
        e = int(customer['destination'])
        start = cm.convert_address(s, width)
        end = [cm.convert_address(e, width)]
        if customer['car_id'] != -1:
            hren.append((customer['car_id'], end))
        else:
            pr = [custom_id, end]
            # print(start, end)
            # path = astar(new, start, end)
            nodes = some_dijkstra(new, [e], height, width, s)
            # print(nodes)
            # print(path)
            if nodes[0] != None:
                pr.append(nodes[0])
                custom.append(pr)
            else:
                pr.append(None)
                custom.append(pr)
            custom_id = custom_id + 1
    # print(custom)

    cars = [[[], [], [], []]]
    # print(len(cars[0][2]))
    count = 0
    for car in configM['cars'].values():
        if car['team_id'] == 0:  # teamid mb != 0
            for h in hren:
                if h[0] == keys[car_id]:
                    cars[car_id][2].append(h[1])
                    count += 1
            if len(cars[car_id][2]) < car['capacity'] and len(cars[car_id][2]) > 0:
                origins.extend(car[car_id][2])
                nodes = some_dijkstra(new, origins, height, width, car['position'])
                newnodes = nodes[len(nodes) - len(car[car_id][2]):len(nodes):1]
            elif len(cars[car_id][2]) == car['capacity']:
                newnodes = some_dijkstra(new, car[car_id][2], height, width, car['position'])
                nodes = []
            elif len(cars[car_id][2]) == 0:
                nodes = some_dijkstra(new, origins, height, width, car['position'])
                newnodes = []

            # if curr_capicity > 0

            cars.append((keys[car_id], nodes, [], newnodes))

            car_id += 1
    # print(cars)
    cars.pop(0)

    return custom, cars, count


def hung(custom, cars, count):
    if custom:
        # n, m = 4, 10
        # a = [[randint(1, 10) for j in range(m)] for i in range(n)]
        ## Если исполнить нельзя - DISABLED
        # matrix = a

        # matrix = [[5, 9, 1, 12, 54, 75, 3],
        #           [10, 3, 2, 3, 7, 23, 12],
        #           [8, 7, 4, 12, 12, 12, 9],
        #           [19, 17, 13, 10, 9, 8, 7]]
        matrix = []

        m = Munkres()

        counter = 0
        # print(cars)
        # print('csccs')
        customers_map = []
        gopa = 0
        for car in cars:
            serial_num = 0
            row = []
            for pas in custom:
                if (pas != None) and (car[1][pas[0]] != None) and (pas[2] != None):
                    # print(car[1])
                    row.append(car[1][pas[0]].weight + pas[2].weight)
                    customers_map.append((0, pas[0]))
                else:
                    customers_map.append((0, pas[0]))
                    row.append(DISALLOWED)
            for i in range(count - gopa - len(car[3])):
                row.append(DISALLOWED)
            for t in car[3]:
                gopa += 1
                row.append(t.weight)
                customers_map.append((1, counter, serial_num))
                serial_num += 1

            counter += 1
            # if car[2] != []:
            matrix.append(row)

        m.pad_matrix(matrix, 0)
        print_matrix(matrix)

        nah = []
        flag = 0
        cnt = 0
        for i in matrix:
            flag = 0
            for j in i:
                if j != DISALLOWED:
                    flag = 1
            if flag == 0:
                print(cnt)
                nah.append(cnt-len(nah))
            cnt += 1
        #matrix_copy = deepcopy(matrix)
        t = [i for i in range(len(matrix))]
        for n in nah:
            matrix.pop(n)
            t.pop(n)
            print('deleted', n)
        row_index = []
        for ma in matrix:
            tr=0

        # print('\n', nah[1])
        print_matrix(matrix)
        print(t)
        indexes = m.compute(matrix)
        # print('csccs')

        total = 0
        i = 0
        values = []
        flag = 0

        kot = []

        for row, column in indexes:
            values.append(matrix[row][column])
            total += values[i]
            print(f'({t[row]}, {column}) -> {values[i]}')
            if customers_map[column][0] == 0:
                kot.append((cars[t[row]][0], cars[t[row]][1][column].path[0]))
            else:
                kot.append((cars[t[row]][0], cars[t[row]][3][customers_map[column][2]].path[0]))
            i += 1
            # if cars[row][1][column].weight == 1:
            #    cars[row][2].append(custom[column][1][2])
        # print(f'total cost: {total}')
        return kot
    else:
        return None


if __name__ == '__main__':
    # token = add_team_and_get_token()
    result = make_matrix(config.configE)
    custom = result[0]
    cars = result[1]
    count = result[2]
    print(custom)
    if custom != []:
        orders = hung(custom, cars, count)
        print(orders)

    # manipulate_cars(orders)
    # manipulate_cars(orders, cars)
