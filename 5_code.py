def readStacks(f) -> list[list[int]]:
    """
    FILE FORMAT:
    [T]     [D]         [L]            \n
    [R]     [S] [G]     [P]         [H]\n
    [G]     [H] [W]     [R] [L]     [P]\n
    [W]     [G] [F] [H] [S] [M]     [L]\n
    [Q]     [V] [B] [J] [H] [N] [R] [N]\n
    [M] [R] [R] [P] [M] [T] [H] [Q] [C]\n
    [F] [F] [Z] [H] [S] [Z] [T] [D] [S]\n
    [P] [H] [P] [Q] [P] [M] [P] [F] [D]\n
     1   2   3   4   5   6   7   8   9 \n
     \n
     move 3 from 8 to 9\n
     ...
    """
    line = f.readline().strip()
    line_len = len(line)
    stacks = []
    num_stacks = int((line_len + 1) / 4)
    for n in range(0, num_stacks):
        stacks.append([])
    while "1" not in line: # stop when we see the index line
        stack_id = 0
        for c in range(1, line_len, 4):
            if line[c] != " ":
                if stacks[]
                stacks[stack_id].append(line[c])
            stack_id += 1
    f.readline() # consume the blank line and leave the cursor on the first line of instructions
    return stacks

def parseInstructions(line: str) -> list[int]:
    return None

def part1():
    with open("5_input.txt", "r") as f:
        stacks = readStacks(f)
        line = f.readline()
        while line is not "":
            qty, c1, c2 = parseInstructions(line)
            to_move = stacks[c1][0:qty]
            stacks[c2] = to_move.reverse() + stacks[c2]
            line = f.readline()
            if line == "\n":
                break
        tops = []
        for stack in stacks:
            tops.append(stack[0])
        print(tops)

def testReadStacks():
    with open("5_input.txt", "r") as f:
        print(readStacks(f))

testReadStacks()