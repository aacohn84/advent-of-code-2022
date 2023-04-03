"""
https://adventofcode.com/2022/day/9

Question we have to answer:
How many positions does the tail of the rope visit at least once?

Sample input:
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

Sample output:
..##..
...##.
.####.
....#.
s###..

The tail visited 13 positions at least once.

== Implementation of the Space ==
We can represent the space as a 2D plane over X (horizontal) and Y (vertical) coordinates.
The origin O is the coordinate pair (0,0) = {X: 0, Y: 0}
Movement of the Head and Tail will be represented by offsets of this 
We will represent all of the positions visited by the tail in a hash set.

== Movement of the Tail ==
We can determine how to move T by cases.

Case 1: column diff > 1
.....    .....
.T.H. -> ..TH.
.....    .....

Case 2: row diff > 1
....    ....
..T.    ....
.... -> ..T.
..H.    ..H.
....    ....

Case 3: column diff > 1 with diagonal
.....    .....
.....    .....
...H. -> ..TH.
.T...    .....
.....    .....

Case 4: row diff > 1 with diagonal
.....    .....
..H..    ..H..
..... -> ..T..
.T...    .....
.....    .....
"""
offsetsByDirection = {
    #    row col
    'L': (0, -1),
    'U': (1, 0),
    'R': (0, 1),
    'D': (-1, 0)
}

def parseInstruction(string):
    # Returns a tuple with the direction and count of steps from the instruction
    # ex: "U 15\n" --> ('U', 15)
    direction, stepCount = string.strip().split()
    return (direction, int(stepCount))

def parseInstructions(instructions):
    return [parseInstruction(instruction) for instruction in instructions]

def moveHead(head, offset):
    head[0] += offset[0]
    head[1] += offset[1]

def moveTail(head, tail):
    # returns True if the tail moved
    rowDiff = head[0] - tail[0]
    colDiff = head[1] - tail[1]
    if abs(colDiff) > 1: # Case 1: tail moves left or right
        tail[1] += 1 if colDiff > 0 else -1
        diagonal = rowDiff != 0 and colDiff != 0
        if diagonal: # Case 3: tail moves into line row-wise
            tail[0] += 1 if rowDiff > 0 else -1
        return True
    elif abs(rowDiff) > 1: # Case 2: tail moves up or down
        tail[0] += 1 if rowDiff > 0 else -1
        diagonal = rowDiff != 0 and colDiff != 0
        if diagonal: # Case 4: tail moves into line column-wise
            tail[1] += 1 if colDiff > 0 else -1
        return True
    return False

def executeInstructionPart1(instruction, head, tail):
    visited = set()
    headOffset = offsetsByDirection.get(instruction[0])
    for _ in range(instruction[1]):
        moveHead(head, headOffset)
        if moveTail(head, tail):
            visited.add(tuple(tail))
    return visited

def part1():
    instructions = None
    with open("9_input.txt", "r") as f:
        instructions = parseInstructions(f.readlines())
    print(f'The number of instructions is {len(instructions)}')
    head = [0, 0]
    tail = [0, 0]
    visited = {(0, 0)}
    for instruction in instructions:
        newlyVisited = executeInstructionPart1(instruction, head, tail)
        visited = visited.union(newlyVisited)
    print(f'The number of visited spots is {len(visited)}')

def executeInstructionPart2(instruction, rope):
    visited = set()
    headOffset = offsetsByDirection.get(instruction[0])
    for _ in range(instruction[1]):
        moveHead(rope[0], headOffset)
        for i in range(1,9):
            if not moveTail(rope[i-1], rope[i]):
                break
            #visualize((instruction[0], f'{instruction[1]} -- step: {step} -- knot: {i}'), rope)
        if moveTail(rope[8], rope[9]):
            visited.add(tuple(rope[9]))
    return visited

def part2():
    instructions = None
    with open("9_input.txt", "r") as f:
        instructions = parseInstructions(f.readlines())
    rope = [[0, 0] for _ in range(10)]
    visited = {(0, 0)}
    for instruction in instructions:
        newlyVisited = executeInstructionPart2(instruction, rope)
        visited = visited.union(newlyVisited)
    print(f'The number of visited spots is {len(visited)}')

#################
# --- TESTS --- #
#################
def testParseInstructions():
    instructions = ["L 1", "U 2", "R 3", "D 4"]
    assert(parseInstructions(instructions) == [('L', 1), ('U', 2), ('R', 3), ('D', 4)])

def testMoveTail():
    # Case 1: column diff > 1
    head = [0, 2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [0, 1])
    
    head = [0, -2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [0, -1])

    # Case 2: row diff > 1
    head = [2, 0]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [1, 0])

    head = [-2, 0]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [-1, 0])

    # Case 3: column diff > 1 with diagonal
    head = [1, 2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [1, 1])

    head = [1, -2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [1, -1])

    head = [-1, -2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [-1, -1])

    head = [-1, 2]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [-1, 1])

    # Case 4: row diff > 1 with diagonal
    head = [2, 1]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [1, 1])

    head = [2, -1]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [1, -1])

    head = [-2, -1]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [-1, -1])

    head = [-2, 1]
    tail = [0, 0]
    moveTail(head, tail)
    assert(tail == [-1, 1])

def testExecuteInstructionPart1():
    head = [0, 0]
    tail = [0, 0]
    visited = {tuple(tail)}
    instructions = parseInstructions(["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"])
    # R 4
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [0, 4])
    assert(tail == [0, 3])
    assert(newlyVisited == {(0, 1), (0, 2), (0, 3)})
    # U 4
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [4, 4])
    assert(tail == [3, 4])
    assert(newlyVisited == {(1, 4), (2, 4), (3, 4)})
    # L 3
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [4, 1])
    assert(tail == [4, 2])
    assert(newlyVisited == {(4, 3), (4, 2)})
    # D 1
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [3, 1])
    assert(tail == [4, 2])
    assert(len(newlyVisited) == 0)
    # R 4
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [3, 5])
    assert(tail == [3, 4])
    assert(newlyVisited == {(3, 3), (3, 4)})
    # D 1
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 5])
    assert(tail == [3, 4])
    assert(len(newlyVisited) == 0)
    # L 5
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 0])
    assert(tail == [2, 1])
    assert(newlyVisited == {(2, 3), (2, 2), (2, 1)})
    # R 2
    newlyVisited = executeInstructionPart1(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 2])
    assert(tail == [2, 1])
    assert(len(newlyVisited) == 0)
    # Final tally of visited spots
    assert(len(visited) == 13)

def visualize(instruction, rope):
    grid = [['.' for _ in range(V_COLS)] for _ in range(V_ROWS)]
    for i, knot in enumerate(rope):
        row, col = knot
        if i == 0:
            grid[row][col] = 'H'
        elif grid[row][col] == '.':
            grid[row][col] = i
    if grid[V_START[0]][V_START[1]] == '.':
        grid[V_START[0]][V_START[1]] == 's'

    print(f"== {instruction[0]} {instruction[1]} ==")
    for i in range (V_ROWS - 1, -1, -1):
        for j in range(V_COLS):
            print(f"{grid[i][j]} ", end="")
        print()

def testVisualize():
    visualize(['R', 5], [(5,16), (5,15), (5,14), (5,13), (5,12), (5,11)], 25, [5, 11])

V_ROWS = 21
V_COLS = 26
V_START = (5, 11)

def testExecuteInstructionPart2():
    #start = (0, 0)
    start = (5, 11)
    #instructions = [('R', 4), ('U', 4), ('L', 3), ('D', 1), ('R', 4), ('D', 1), ('L', 5), ('R', 2)]
    instructions = [('R',5), ('U', 8), ('L', 8), ('D', 3), ('R', 17), ('D', 10), ('L', 25), ('U', 20)]
    rope = [list(start) for _ in range(10)]
    visited = {start}
    for instruction in instructions:
        newlyVisited = executeInstructionPart2(instruction, rope)
        visualize(instruction, rope)
        visited = visited.union(newlyVisited)
    print(f'The number of visited spots is {len(visited)}')

#################
# - END TESTS - #
#################

#testParseInstructions()
#testMoveTail()
#testExecuteInstructionPart1()
#testVisualize()
#testExecuteInstructionPart2()

#part1()
part2()