"""
FILE FORMAT:
[T]     [D]         [L]            \n // each stack item on the line is enclosed by 2 brackets and separated by 4 characters
[R]     [S] [G]     [P]         [H]\n // lin_len = (n_stacks * 3 chars per stack) + (n_stacks * 1 whitespace per stack) = n_stacks * 4
[G]     [H] [W]     [R] [L]     [P]\n // so n_stacks = line_len / 4
[W]     [G] [F] [H] [S] [M]     [L]\n
[Q]     [V] [B] [J] [H] [N] [R] [N]\n
[M] [R] [R] [P] [M] [T] [H] [Q] [C]\n
[F] [F] [Z] [H] [S] [Z] [T] [D] [S]\n
[P] [H] [P] [Q] [P] [M] [P] [F] [D]\n
 1   2   3   4   5   6   7   8   9 \n // index line
\n
move 3 from 8 to 9\n // 1st instruction line
...
"""
def readStacks(f) -> list[list[int]]:
    # Get total length of first line including trailing whitespace. This is just so we can calculate the number of stacks.
    line = f.readline()
    length = len(line)
    n_stx = int(length / 4)
    
    # Create empty stacks to ingest the table
    stx = []
    for n in range(0, n_stx):
        stx.append([])
    
    # begin line processing
    line = line.strip()
    length = len(line)
    while "1" not in line: # process lines until we see the index line
        stk_id = 0
        for c in range(1, length, 4): # starting at the 2nd character, check every 4th character in the line
            if line[c] != " ":
                stx[stk_id].append(line[c])
            stk_id += 1
        line = f.readline().strip()
        length = len(line)
    f.readline() # consume the blank line after the index line and leave the cursor on the first line of instructions
    return stx

def parseInstruction(line: str) -> list[int]:
    """
    INSTRUCTION FORMAT:
    move 3 from 8 to 9\n
    
    After split:
    ['move', '3', 'from', '8', 'to', '9']
       0     (1)     2    (3)   4    (5)
    """
    raw_split = line.split()
    return int(raw_split[1]), int(raw_split[3]), int(raw_split[5])

def executeInstruction(stx: list[list[str]], qty: int, from_stk: int, to_stk: int) -> None:
    # We need to subtract 1 from every stack index because we have a zero-based index, while the instructions are 1-based
    from_stk = from_stk - 1
    to_stk = to_stk - 1

    # Copy the first 'qty' items of the 'from' stack
    to_move = stx[from_stk][0:qty]

    # Add them to the front of the 'to' stack in reverse order
    #to_move.reverse() # comment out this line for part 2
    stx[to_stk] = to_move + stx[to_stk]

    # Remove the first 'qty' items of the 'from' stack
    stx[from_stk] = stx[from_stk][qty:]

def main():
    with open("5_input.txt", "r") as f:
        stx = readStacks(f) # this function should leave us at the first line of instructions
        line = f.readline()
        while line != "": # continue parsing instructions until we hit the end of the file
            qty, from_stk, to_stk = parseInstruction(line)
            executeInstruction(stx, qty, from_stk, to_stk)
            line = f.readline()
            if line == "\n":
                break
        stk_tops = []
        for stk in stx:
            stk_tops.append(stk[0])
        print(''.join(stk_tops))

def testReadStacks():
    with open("5_input.txt", "r") as f:
        stx = readStacks(f)
        assert(len(stx) == 9)
        assert(stx[0][0] == 'T' and len(stx[0]) == 8)
        assert(stx[1][0] == 'R' and len(stx[1]) == 3)
        assert(stx[2][0] == 'D' and len(stx[2]) == 8)
        assert(stx[3][0] == 'G' and len(stx[3]) == 7)
        assert(stx[4][0] == 'H' and len(stx[4]) == 5)
        assert(stx[5][0] == 'L' and len(stx[5]) == 8)
        assert(stx[6][0] == 'L' and len(stx[6]) == 6)
        assert(stx[7][0] == 'R' and len(stx[7]) == 4)
        assert(stx[8][0] == 'H' and len(stx[8]) == 7)

def testParseInstruction():
    instructions = [
        "move 3 from 8 to 9",
        "move 14 from 7 to 1"
    ]
    parsed = [
        (3,8,9),
        (14,7,1)
    ]
    for i, s in enumerate(instructions):
        assert(parseInstruction(s) == parsed[i])

def testExecuteInstruction():
    stx = [
        ["C", "B", "A"],
        ["D", "E", "F"]
    ]
    stxState1 = [
        [],
        ["A", "B", "C", "D", "E", "F"]
    ]
    stxState2 = [
        ["F", "E", "D", "C", "B", "A"],
        []
    ]
    stxState3 = [
        ["C", "B", "A"],
        ["D", "E", "F"]
    ]
    executeInstruction(stx, 3, 1, 2) # move 3 from 1 to 2
    assert(stx == stxState1)
    executeInstruction(stx, 6, 2, 1) # move 6 from 2 to 1
    assert(stx == stxState2)
    executeInstruction(stx, 3, 1, 2) # move 3 from 1 to 2
    assert(stx == stxState3)

testReadStacks()
testParseInstruction()
#testExecuteInstruction()
main()