import sys
from copy import deepcopy
import numpy as np
from util import print_grid, get_pos, get_adjacent_coords
import networkx as nx
from tqdm import tqdm
from collections import Counter

def parse():
    data = []
    # For matrix data
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data
    
def get_graph(data):
    graph = nx.Graph()
    possible_coords = np.where(data != "#")
    possible_coords = list(tuple(c) for c in np.vstack(possible_coords).T)
    
    for coord in possible_coords:
        adjacent = get_adjacent_coords(data, coord)
        for adj_coord in adjacent:
            if data[adj_coord[0], adj_coord[1]] == "#": continue
            edge = (
                coord,
                tuple(adj_coord),
                {'weight': 1}
            )
            graph.add_edges_from([edge])
    return graph

def generate_all_possible_skips(data):
    skips = []
    cheat_start_positions = np.where(data != "#")
    cheat_start_positions = list(tuple(c) for c in np.vstack(cheat_start_positions).T)

    for start_coord in cheat_start_positions:
        for first_coord in get_adjacent_coords(data, start_coord):
            if data[*first_coord] == "#":
                for second_coord in get_adjacent_coords(data, first_coord):
                    if data[*second_coord] == "#" or (second_coord == start_coord).all(): continue
                    skips.append((tuple(start_coord), tuple(second_coord)))
    return skips

def part1(data):
    min_saved_time = 100
    start_pos = tuple(get_pos(data, "S"))
    end_pos = tuple(get_pos(data, "E"))
    G = get_graph(data)
    path = nx.shortest_path(G, start_pos, end_pos, weight="weight")
    base_time = nx.path_weight(G, path, weight="weight")
    print("Base time ", base_time)

    dist_from_start, _ = nx.single_source_dijkstra(G, source=start_pos, weight='weight')
    dist_from_end, _   = nx.single_source_dijkstra(G, source=end_pos, weight='weight')

    skips = generate_all_possible_skips(data)
    time_save = []

    for skip_start, skip_end in skips:
        weight = dist_from_start[skip_start] + dist_from_end[skip_end] + 2
        if weight >= base_time: continue
        time_save.append(base_time - weight)

    summ = 0
    for i in time_save:
        if i >= min_saved_time:
            summ += 1
            
    # print(Counter(time_save))
    return summ

def part2(data):
    return

def main():
    #parse stdin
    data = parse()
    data = np.array(data)
    # print(data)
    part2_data = deepcopy(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(part2_data)
    print(f"Part2: {result2}")

main()
