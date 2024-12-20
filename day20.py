import sys
from copy import deepcopy
from pprint import pprint
import numpy as np
from util import print_grid, get_pos, get_adjacent_coords
import networkx as nx
import time
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

def get_graph_path_weight(data, start_pos, end_pos):
    graph, path = get_graph_path(data, start_pos, end_pos)
    weight = nx.path_weight(graph, path, weight="weight")
    return graph, path, weight

def get_weight_with_skip(data, start_pos, end_pos, skip_start, skip_end):
    graph = get_graph(data)
    path1 = nx.shortest_path(graph, start_pos, skip_start, weight="weight")
    path2 = nx.shortest_path(graph, skip_end, end_pos, weight="weight")
    weight1 = nx.path_weight(graph, path1, weight="weight")
    if weight1 >= 9410: return
    weight2 = nx.path_weight(graph, path2, weight="weight")
    return weight1 + weight2 + 2

def get_weight_graph(data, start_pos, end_pos):
    graph, path = get_graph_path(data, start_pos, end_pos)
    weight = nx.path_weight(graph, path, weight="weight")
    return weight, graph

def get_graph_path(data, start_pos, end_pos):
    graph = get_graph(data)
    # print(graph)
    path = nx.shortest_path(graph, start_pos, end_pos, weight="weight")
    return graph, path
    
def generate_all_possible_grids(data):
    grids = []
    walls_that_can_be_modified = np.where(data == "#")
    walls_that_can_be_modified = list(tuple(c) for c in np.vstack(walls_that_can_be_modified).T)
    for base_coord in walls_that_can_be_modified:
        new_grid = deepcopy(data)
        new_grid[*base_coord] = "1"
        for next_coord in get_adjacent_coords(data, base_coord):
            # if new_grid[*next_coord] == "#":
                new_new_grid = deepcopy(new_grid)
                if new_new_grid[*next_coord] != "S" or new_new_grid[*next_coord] != "E":
                    new_new_grid[*next_coord] = "2"
                grids.append(new_new_grid)
    return grids

def generate_all_possible_grids2(data):
    grids = []
    cheat_start_positions = np.where(data != "#")
    cheat_start_positions = list(tuple(c) for c in np.vstack(cheat_start_positions).T)
    for start_coord in cheat_start_positions:
        new_grid = deepcopy(data)
        new_grid[*start_coord] = "0"
        for first_coord in get_adjacent_coords(data, start_coord):
            if new_grid[*first_coord] == "#":
                new_new_grid = deepcopy(new_grid)
                new_new_grid[*first_coord] = "1"
                for second_coord in get_adjacent_coords(data, first_coord):
                    if new_new_grid[*second_coord] in ("#", "0"): continue
                    new_new_new_grid = deepcopy(new_new_grid)
                    new_new_new_grid[*second_coord] = "2"
                    grids.append(new_new_new_grid)
    return grids

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
    start_pos = tuple(get_pos(data, "S"))
    end_pos = tuple(get_pos(data, "E"))
    base_time, G = get_weight_graph(data, start_pos, end_pos)
    min_saved_time = 100
    print("Base time ", base_time)

    dist_from_start, _ = nx.single_source_dijkstra(G, source=start_pos, weight='weight')
    dist_from_end, _   = nx.single_source_dijkstra(G, source=end_pos, weight='weight')

    skips = generate_all_possible_skips(data)
    time_save = []

    for skip_start, skip_end in tqdm(skips):
        # weight = get_weight_with_skip(data, start_pos, end_pos, skip_start, skip_end)
        weight = dist_from_start[skip_start] + dist_from_end[skip_end] + 2
        
        if not weight: continue
        if weight >= base_time: continue
        # if weight == 80: 
        #     print_grid(data)
        time_save.append(base_time - weight)

    summ = 0
    for i in time_save:
        if i >= min_saved_time:
            summ += 1
            
    print(Counter(time_save))
    return summ

def part2(data):
    return

def main():
    #parse stdin
    data = parse()
    data = np.array(data)
    print(data)
    part2_data = deepcopy(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(part2_data)
    print(f"Part2: {result2}")

main()
