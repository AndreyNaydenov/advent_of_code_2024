import sys
from copy import deepcopy
from pprint import pprint
import numpy as np
from util import print_grid, get_pos, get_adjacent_coords
import networkx as nx
from tqdm import tqdm

def parse():
    coords = []
    # For matrix data
    for line in sys.stdin:
        i, j = line.strip().split(",")
        coord = (int(j), int(i))
        coords.append(coord)
    return coords
  
def get_graph_from_grid(grid):
    graph = nx.Graph()
    possible_coords = np.where(grid != "#")
    possible_coords = list(tuple(c) for c in np.vstack(possible_coords).T)

    for coord in possible_coords:
        adjacent = get_adjacent_coords(grid, coord)
        for adj_coord in adjacent:
            if grid[*adj_coord] == "#": continue
            edge = (
                coord,
                tuple(adj_coord),
                {'weight': 1}
            )
            graph.add_edges_from([edge])
    return graph

def add_coords_to_grid(grid, coords, limit=None):
    i = 0
    for coord in coords:
        if i >= limit: break
        grid[*coord] = "#"
        i += 1
    return grid

def add_coord_to_grid(grid, coord):
    grid[*coord] = "#"
    return grid

def part1(coords):
    shape = (71, 71)
    # shape = (7, 7)
    start_pos = (0, 0)
    end_pos = (shape[0]-1, shape[1]-1)

    grid = np.full(shape, ".")
    add_coords_to_grid(grid, coords, limit=1024)
    graph = get_graph_from_grid(grid)
    
    path = nx.shortest_path(graph, start_pos, end_pos, weight="weight")
    weight = nx.path_weight(graph, path, weight="weight")
    return weight

def part2(coords):
    # TODO: optimize by skipping grid, just by removing node from the graph
    shape = (71, 71)
    # shape = (7, 7)
    start_pos = (0, 0)
    end_pos = (shape[0]-1, shape[1]-1)

    grid = np.full(shape, ".")
    add_coords_to_grid(grid, coords, limit=1024)
    graph = get_graph_from_grid(grid)

    for i in tqdm(range(1024, len(coords))):
        add_coords_to_grid(grid, coords, limit=i)
        # coord = coords[i]
        # add_coord_to_grid(grid, coord)
        graph = get_graph_from_grid(grid)
        try:
            path = nx.shortest_path(graph, start_pos, end_pos, weight="weight")
        except:
            y, x = coords[i-1]
            return f"{x},{y}"

def main():
    #parse stdin
    data = parse()
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
