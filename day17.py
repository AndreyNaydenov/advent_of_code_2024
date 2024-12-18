import sys
import numpy as np
from tqdm import tqdm

def parse():
    state = {}
    code = []
    sections = "".join(sys.stdin.readlines()).strip().split("\n\n")
    for line in sections[0].split("\n"):
        register_name = line[9]
        register_value = int(line[12:])
        state[register_name] = register_value
    for line in sections[1].split("\n"):
        for instruction in line.replace("Program: ", "").split(","):
            code.append(int(instruction))
    return (state, code)

class Computer():
    pointer: int = 0
    registers: dict[str, int]
    code: list[int]

    def __init__(self, registers, code):
        self.registers = registers.copy()
        self.code = code.copy()

    def __repr__(self):
        return f"Computer {self.registers} {self.code} cur_i: {self.pointer}"

    def calc_combo_operand(self, operand):
        match operand:
            case 0|1|2|3: return operand
            case 4: return self.registers["A"]
            case 5: return self.registers["B"]
            case 6: return self.registers["C"]
            case 7: raise Exception("Combo operand 7 used!")

    def adv(self, instruction, operand):
        nominator = self.registers["A"]
        denominator = 2 ** self.calc_combo_operand(operand)
        self.registers["A"] = nominator // denominator
        # print(f"ADV {nominator}/{denominator}={self.registers['A']}")

    def bxl(self, instruction, operand):
        self.registers["B"] = self.registers["B"] ^ operand 
        
    def bst(self, instruction, operand):
        self.registers["B"] = self.calc_combo_operand(operand) % 8

    def jnz(self, instruction, operand):
        if self.registers["A"] == 0: return False
        self.pointer = operand
        return True

    def bxc(self, instruction, operand):
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, instruction, operand):
        return self.calc_combo_operand(operand) % 8

    def bdv(self, instruction, operand):
        nominator = self.registers["A"]
        denominator = 2 ** self.calc_combo_operand(operand)
        self.registers["B"] = nominator // denominator

    def cdv(self, instruction, operand):
        nominator = self.registers["A"]
        denominator = 2 ** self.calc_combo_operand(operand)
        self.registers["C"] = nominator // denominator    

    def do_cur_instruction(self):
        instruction_pos_in_code = self.pointer
        operand_pos_in_code = instruction_pos_in_code + 1
        instruction = self.code[instruction_pos_in_code]
        operand = self.code[operand_pos_in_code]
        # print(f"Run instr:{instruction}, oprnd:{operand}")

        match instruction:
            case 0: self.adv(instruction, operand)
            case 1: self.bxl(instruction, operand)
            case 2: self.bst(instruction, operand)
            case 3: 
                if self.jnz(instruction, operand):
                    return # to skip pointer increment if jumped
            case 4: self.bxc(instruction, operand)
            case 5: 
                out = self.out(instruction, operand)
                self.pointer += 2
                return out
            case 6: self.bdv(instruction, operand)
            case 7: self.cdv(instruction, operand)
        
        self.pointer += 2

    def run(self):
        # runs and yields values until halt (returns on halt)
        while self.pointer < len(self.code):
            out = self.do_cur_instruction()
            if out != None: yield out
        return

def try_possible_a_in_range(state, code, ran):
    for possible_a in tqdm(range(ran[0], ran[1])):
        c = Computer(state, code)
        res = list(c.run())
        if res == code:
            return possible_a

def part1(data):
    state, code = data
    c = Computer(state, code)
    print(c)
    res = c.run()
    return ",".join(str(i) for i in res)

def part2(data):
    state, code = data

    matched_count_max = 0
    possible_a = 0
    rate = 1
    while possible_a < 281474976710656:
    # for possible_a in tqdm(range(1, 200000, 1)):
        # print(f"checking with A={possible_a}")
        state["A"] = possible_a
        c = Computer(state, code)
        
        it = c.run()
        code_it = iter(code)
        matched_count = 0
        try:
            for i in range(len(code)):
                got = next(it)
                expected = next(code_it)
                # print(got, expected)
                if got != expected:
                    # print("diff detect, next")
                    matches = False
                    break
                matched_count += 1
                matches = True
        except StopIteration:
            matches = False
            # print("stop")
        # print(f"Current max {matched_count_max}")
        # matched_count_max = max(matched_count_max, matched_count)    
        if matched_count > matched_count_max:
            matched_count_max = matched_count
            print(f"New max: {matched_count}, at {possible_a}")
            if possible_a == 0:
                possible_a = 1
            # possible_a *= 20
            rate *= 27
            print("set A to:", possible_a, "set speed to:", rate)
        # print(f"A:{possible_a}, matched:{matched_count}")  
        if matches:
            return possible_a
        possible_a += rate

def main():
    #parse stdin
    data = parse()
    print(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
