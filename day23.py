import sys
import numpy as np
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import time

def parse():
    connections = []
    # For matrix data
    for line in sys.stdin:
        a, b = line.strip().split("-")
        connections.append((a, b))
    return connections

def make_graph(data):
    graph = nx.Graph()
    graph.add_edges_from(data)
    return graph

def select_starting_with_t(cycles):
    new_cycles = []
    for c in cycles:
        has = False
        for node in c:
            if node[0] == 't': has = True
        if has:
            new_cycles.append(c)
    return new_cycles

def part1(data, visualize=False):
    G = make_graph(data)
    if visualize:
        nx.draw_networkx(G, with_labels=True)
        plt.show()
    cycles = nx.chordless_cycles(G, length_bound=3)
    with_t = select_starting_with_t(cycles)
    # print(with_t)
    return len(with_t)

def part2(data):
    G = make_graph(data)
    # clique = nx.approximation.max_clique(G)
    cliques = nx.find_cliques(G)
    max_len = 0
    max_clique = []
    for clique in cliques:
        clen = len(clique)
        if clen > max_len:
            max_len = clen
            max_clique = clique
    # print(max_clique)
    return ",".join(sorted(max_clique))

def main():
    #parse stdin
    data = parse()
    
    #PART1
    result1 = part1(data, False)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
