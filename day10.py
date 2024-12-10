import sys
import numpy as np

def parse():
    data = []
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data

def in_bounds(data, coord):
    il, jl = data.shape
    if coord[0] < 0 or coord[0] >= il: return False
    if coord[1] < 0 or coord[1] >= jl: return False
    return True

def get_adjacent_coords(data, coord):
    adjacent = (
        (coord[0] - 1, coord[1]),
        (coord[0] + 1, coord[1]),
        (coord[0], coord[1] - 1),
        (coord[0], coord[1] + 1)
    )
    return [c for c in adjacent if in_bounds(data, c)]

def build_graph(data):
    graph = {}
    il, jl = data.shape
    for i in range(il):
        for j in range(jl):
            curr_coord = (i, j)
            curr_val = data[*curr_coord]
            for c in get_adjacent_coords(data, curr_coord):
                adjacent_val = data[*c]
                if int(adjacent_val)- int(curr_val) != 1: continue
                ls = graph.get(curr_coord)
                if ls:
                    ls.append(c)
                else:
                    graph[curr_coord] = [c]
    return graph
                
def get_path(graph, start_coord, finish_coord):
    if start_coord == finish_coord: return [start_coord]
    next_possible = graph.get(start_coord)
    if not next_possible: return
    for coord in next_possible:
        path = get_path(graph, coord, finish_coord)
        if path:
            return [start_coord, *path]

def get_all_paths(graph, start_coord, finish_coord):
    if start_coord == finish_coord: return [start_coord]
    next_possible = graph.get(start_coord)
    if not next_possible: return
    all_paths = []
    for coord in next_possible:
        paths = get_all_paths(graph, coord, finish_coord)
        if paths:
            for path in paths:
                all_paths.append([start_coord, *path])
    return all_paths

def part1(data):
    # print(data)
    graph = build_graph(data)
    # print(graph)
    all_zeroes = np.vstack(np.where(data == "0")).T
    all_nines = np.vstack(np.where(data == "9")).T
    summ_all = 0
    for start_coord in all_zeroes:
        start_coord = tuple(start_coord)
        # print(f"Checking trailhead {start_coord}")
        summ_this_trailhead = 0
        for finish_coord in all_nines:
            finish_coord = tuple(finish_coord)
            # print(f"Trying to find path from {np.array(start_coord)} to {np.array(finish_coord)}")
            path = get_path(graph, start_coord, finish_coord)
            if path:
                summ_this_trailhead += 1
        summ_all += summ_this_trailhead
    return summ_all

def part2(data):
    # print(data)
    graph = build_graph(data)
    # print(graph)
    all_zeroes = np.vstack(np.where(data == "0")).T
    all_nines = np.vstack(np.where(data == "9")).T
    summ_all = 0
    for start_coord in all_zeroes:
        start_coord = tuple(start_coord)
        # print(f"Checking trailhead {start_coord}")
        summ_this_trailhead = 0
        for finish_coord in all_nines:
            finish_coord = tuple(finish_coord)
            # print(f"Trying to find path from {np.array(start_coord)} to {np.array(finish_coord)}")
            paths = get_all_paths(graph, start_coord, finish_coord)
            if paths:
                for path in paths:
                    summ_this_trailhead += 1
        summ_all += summ_this_trailhead
    return summ_all

def main():
    #parse stdin
    data = parse()
    data = np.array(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
