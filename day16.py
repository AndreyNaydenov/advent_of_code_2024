import sys
from copy import deepcopy
from pprint import pprint
import numpy as np
from util import print_grid, get_pos, get_adjacent_coords
import networkx as nx

def parse():
    data = []
    # For matrix data
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data

def get_next_direction(direction):
     match direction:
        case "<": return "^"
        case "^": return ">"
        case ">": return "v"
        case "v": return "<"
    
def get_graph(data, directional=False):
    if directional:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()
    possible_coords = np.where(data != "#")
    possible_coords = list(tuple(c) for c in np.vstack(possible_coords).T)

    possible_directions = ["<", "^", ">", "v"]
    
    for coord in possible_coords:
        adjacent = get_adjacent_coords(data, coord, include_direction=True)
        for d in possible_directions:
            edge = (
                (coord, d),
                (coord, get_next_direction(d)),
                {'weight': 1000}
            )
            graph.add_edges_from([edge])
            for adj_coord, direction in adjacent:
                if data[*adj_coord] == "#": continue
                if direction == d:
                    edge = (
                        (coord, d),
                        (tuple(adj_coord), d),
                        {'weight': 1}
                    )
                    graph.add_edges_from([edge])
    return graph
    
def part1(data):
    start_pos = get_pos(data, "S")
    start_state = (tuple(start_pos), ">")
    end_pos = get_pos(data, "E")

    start_direction = ">"
    graph = get_graph(data)
    # print(graph)

    path = nx.shortest_path(graph, start_state, (tuple(end_pos), "^"), weight="weight")
    weight = nx.path_weight(graph, path, weight="weight")
    return weight

def part2(data):
    start_direction = ">"
    start_pos = get_pos(data, "S")
    start_state = (tuple(start_pos), start_direction)
    end_pos = get_pos(data, "E")

    graph = get_graph(data, directional=True)
    # print(graph)
    paths = nx.all_shortest_paths(graph, start_state, (tuple(end_pos), "^"), weight="weight")
    return len(set([x[0] for p in paths for x in p]))

def main():
    #parse stdin
    data = parse()
    data = np.array(data)
    part2_data = deepcopy(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(part2_data)
    print(f"Part2: {result2}")

main()
