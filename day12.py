import sys
import numpy as np

def parse():
    data = []
    # For matrix data
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data

def in_bounds(data, coord):
    il, jl = data.shape
    if coord[0] < 0 or coord[0] >= il: return False
    if coord[1] < 0 or coord[1] >= jl: return False
    return True

def get_adjacent_coords(data, coord, all_coords=False):
    adjacent = (
        (coord[0] - 1, coord[1]),
        (coord[0] + 1, coord[1]),
        (coord[0], coord[1] - 1),
        (coord[0], coord[1] + 1)
    )
    return [c for c in adjacent if in_bounds(data, c) or all_coords ]

def find_region(data, current_coord):
    coords_checked = set()
    region = set()
    letter = data[*current_coord]
    next_cells_to_check = [current_coord]
    while next_cells_to_check:
        coord = next_cells_to_check.pop(0)
        if coord in coords_checked:
            #already was on that cell, skip
            continue
        coords_checked.add(coord)
        current_letter = data[*coord]
        if current_letter == letter:
            region.add(coord)
        else:
            continue
        for cell in get_adjacent_coords(data, coord):
            next_cells_to_check.append(cell)
    # print(f"Found region {letter}, size {len(region)}, {region}")
    return region

def is_part_of_some_region(regions, coord):
    for region in regions:
        if coord in region:
            return True
    return False

def get_perimeter(data, region):
    perimeter = 0
    for cell in region:
        for adj_cell in get_adjacent_coords(data, cell, all_coords=True):
            if adj_cell in region: continue
            perimeter += 1
    return perimeter

def get_cell_corners(coord):
    # returns 4 corners around the cell point
    corners = (
        (coord[0] - 0.5, coord[1] - 0.5), # left up
        (coord[0] - 0.5, coord[1] + 0.5), # right up
        (coord[0] + 0.5, coord[1] - 0.5), # left down
        (coord[0] + 0.5, coord[1] + 0.5)  # right down
    )
    return corners

def get_cells(coord):
    # returns 4 cells around the corner point
    cells = (
        (coord[0] - 0.5, coord[1] - 0.5), # left up
        (coord[0] - 0.5, coord[1] + 0.5), # right up
        (coord[0] + 0.5, coord[1] - 0.5), # left down
        (coord[0] + 0.5, coord[1] + 0.5)  # right down
    )
    result = [(int(x[0]), int(x[1])) for x in cells]
    return list(result)

def is_diagonal(cells, region):
    res = tuple([cell in region for cell in cells])
    if res == (True, False, False, True): return True
    if res == (False, True, True, False): return True
    return False

def get_sides(data, region):
    #we need to count cornters, not sides
    corners = set()
    additional_count = 0
    all_possible_corners = set()
    #side is continous row or column of non region cells, that have region cells on the same side
    for cell in region:
        all_possible_corners.update(get_cell_corners(cell))
    for corner in all_possible_corners:
        summ_cells_in_reg = 0
        cells = get_cells(corner)
        for cell in cells:
            if cell in region:
                summ_cells_in_reg += 1
        #if 2 or 4 cell in corner are from region, this is not a corner
        if summ_cells_in_reg == 4: continue
        if summ_cells_in_reg == 2:
            # if diagonal, count +2, else 0
            if is_diagonal(cells, region):
                corners.add(corner)
                additional_count += 1
        else:
            corners.add(corner)
            
    # print("Corners", corners)
    return len(corners) + additional_count

def get_region_letter(data, region):
    it = iter(region)
    cell = next(it)
    return data[*cell]

def calc_part1_score(data, regions):
    summ = 0
    for region in regions:
        area = len(region)
        perimeter = get_perimeter(data, region)
        score = area * perimeter
        summ += score
        # print(f"Calulated area {get_region_letter(data, region)} {area}, perimeter {perimeter}")
    return summ

def calc_part2_score(data, regions):
    summ = 0
    for region in regions:
        area = len(region)
        sides = get_sides(data, region)
        score = area * sides
        summ += score
        # print(f"Calulated area {get_region_letter(data, region)} {area}, sides {sides}")
    return summ

def get_regions(data):
    regions = []
    il, jl = data.shape
    for i in range(il):
        for j in range(jl):
            current_coord = (i, j)
            # check that current coord is not part of found region
            if is_part_of_some_region(regions, current_coord):
                continue
            region = find_region(data, current_coord)
            regions.append(region)
    return regions
    
def part1(data):
    regions = get_regions(data)
    return calc_part1_score(data, regions)
            
def part2(data):
    regions = get_regions(data)
    return calc_part2_score(data, regions)

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
