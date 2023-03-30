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
            tail[0] = head[0]
        return True
    elif abs(rowDiff) > 1: # Case 2: tail moves up or down
        tail[0] += 1 if rowDiff > 0 else -1
        diagonal = rowDiff != 0 and colDiff != 0
        if diagonal: # Case 4: tail moves into line column-wise
            tail[1] = head[1]
        return True
    return False

def executeInstruction(instruction, head, tail):
    visited = set()
    headOffset = offsetsByDirection.get(instruction[0])
    for _ in range(instruction[1]):
        moveHead(head, headOffset)
        if moveTail(head, tail):
            visited.add(tuple(tail))
    return visited

def main():
    instructions = None
    with open("9_input.txt", "r") as f:
        instructions = parseInstructions(f.readlines())
    print(f'The number of instructions is {len(instructions)}')
    head = [0, 0]
    tail = [0, 0]
    visited = {tuple(tail)}
    for instruction in instructions:
        newlyVisited = executeInstruction(instruction, head, tail)
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

def testExecuteInstruction():
    head = [0, 0]
    tail = [0, 0]
    visited = {tuple(tail)}
    instructions = parseInstructions(["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"])
    # R 4
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [0, 4])
    assert(tail == [0, 3])
    assert(newlyVisited == {(0, 1), (0, 2), (0, 3)})
    # U 4
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [4, 4])
    assert(tail == [3, 4])
    assert(newlyVisited == {(1, 4), (2, 4), (3, 4)})
    # L 3
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [4, 1])
    assert(tail == [4, 2])
    assert(newlyVisited == {(4, 3), (4, 2)})
    # D 1
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [3, 1])
    assert(tail == [4, 2])
    assert(len(newlyVisited) == 0)
    # R 4
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [3, 5])
    assert(tail == [3, 4])
    assert(newlyVisited == {(3, 3), (3, 4)})
    # D 1
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 5])
    assert(tail == [3, 4])
    assert(len(newlyVisited) == 0)
    # L 5
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 0])
    assert(tail == [2, 1])
    assert(newlyVisited == {(2, 3), (2, 2), (2, 1)})
    # R 2
    newlyVisited = executeInstruction(instructions.pop(0), head, tail)
    visited = visited.union(newlyVisited)
    assert(head == [2, 2])
    assert(tail == [2, 1])
    assert(len(newlyVisited) == 0)
    # Final tally of visited spots
    assert(len(visited) == 13)

#################
# - END TESTS - #
#################

#testParseInstructions()
#testMoveTail()
#testExecuteInstruction()

main()