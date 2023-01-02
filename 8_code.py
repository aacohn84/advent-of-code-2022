"""
Example:
30373
25512
65332
33549
35390

correct output is 21 (16 trees visible on the edge, 5 visible in the interior)

All trees on the outside edge are visible. 
Since the input grid is 99x99, the minimum number of visible trees is 99 * 4 - 4 = 392.

The tree height goes from 0 to 9, with 9 being the tallest. 
If we find a tree of height 9 on a row or column, then it's impossible to see anything beyond it.
Thus, our job can be simplified by searching for the tallest tree on each row or column. 
We know that all the trees behind it are not visible, so we don't need to look any farther in that direction.


There may be plateaus and valleys. For example:

12332758

Looking from the left edge, the 2nd '3' is not visible, nor are the following '2' and '5'. The visible trees are 1,2,3,4,7,8.
So we need some way of saying, what's the tallest tree I've seen so far up to a certain point?
So we can say everything from the edge to the first '3' is visible. Anything behind the 3 has to be taller.
I think we need to go through this grid 4 times, once from each direction.
As we go, we track whether we've seen a tree with a height less than or equal to any of the trees closer to the edge.
We'll keep track of the tallest tree we've seen, and we'll only count trees that are taller than it.
Once we see a tree of height 9, we can stop counting from that direction.

We need to keep track of whether I've seen a tree or not, to avoid double counting them.
"""
class Tree:
    def __init__(self, height, index):
        self.height = height
        self.index = index

    def __eq__(self, right):
        return self.height == right.height and self.index == right.index

    def __str__(self):
        return f"{self.height}"

    def __repr__(self):
        return str(self)

class TreeGrid:
    DIRECTIONS = ["RIGHT", "LEFT", "DOWN", "UP"]
    def __init__(self, grid):
        self.grid = TreeGrid.treeify(grid)
        self.seen = set()
    
    def __str__(self):
        return str(self.grid)
    
    def __repr__(self):
        return str(self)
    
    @staticmethod
    def treeify(grid):
        i = 0
        treeifiedGrid = []
        for row in grid:
            treeifiedRow = []
            for element in row:
                treeifiedRow.append(Tree(element, i))
                i += 1
            treeifiedGrid.append(treeifiedRow)
        return treeifiedGrid

    def linesForDirection(self, direction):
        if direction == "LEFT":
            return self.grid # view of each row from the left
        elif direction == "RIGHT":
            return [list(reversed(line)) for line in self.grid] # view of each row from the right
        elif direction == "DOWN":
            return [
                [row[i] for row in self.grid] 
                for i in range(len(self.grid))
            ] # view of each column from the top
        else:
            return [
                list(reversed([row[i] for row in self.grid])) 
                for i in range(len(self.grid))
            ] # view of each column from the bottom
    
    def viewTreesInLine(self, line):
        tallestTree = -1
        for tree in line:
            if tree.height > tallestTree and tree.index not in self.seen:
                self.seen.add(tree.index)
            tallestTree = max(tallestTree, tree.height)
            if tallestTree == 9:
                break

    def getTotalVisibleTrees(self):
        for d in TreeGrid.DIRECTIONS:
            for line in self.linesForDirection(d):
                self.viewTreesInLine(line)
        return len(self.seen)

def testLinesForDirection():
    grid = [[1,2,3], [4,5,6], [7,8,9]]
    gridLeft = [[Tree(1,0), Tree(2,1), Tree(3,2)], [Tree(4,3), Tree(5,4), Tree(6,5)], [Tree(7,6), Tree(8,7), Tree(9,8)]]
    gridRight = [[Tree(3,2),Tree(2,1),Tree(1,0)], [Tree(6,5),Tree(5,4),Tree(4,3)], [Tree(9,8),Tree(8,7),Tree(7,6)]]
    gridDown = [[Tree(1,0),Tree(4,3),Tree(7,6)], [Tree(2,1),Tree(5,4),Tree(8,7)], [Tree(3,2),Tree(6,5),Tree(9,8)]]
    gridUp = [[Tree(7,6),Tree(4,3),Tree(1,0)], [Tree(8,7),Tree(5,4),Tree(2,1)], [Tree(9,8),Tree(6,5),Tree(3,2)]]
    tg = TreeGrid(grid)
    assert(tg.linesForDirection("LEFT") == gridLeft)
    assert(tg.linesForDirection("RIGHT") == gridRight)
    assert(tg.linesForDirection("DOWN") == gridDown)
    assert(tg.linesForDirection("UP") == gridUp)

def testGetTotalVisibleTrees():
    grid = [
        [3,0,3,7,3],
        [2,5,5,1,2],
        [6,5,3,3,2],
        [3,3,5,4,9],
        [3,5,3,9,0]
    ]
    tg = TreeGrid(grid)
    assert(tg.getTotalVisibleTrees() == 21)

def main():
    fGrid = []
    with open("8_input.txt", "r") as f:
        fGrid.extend([int(element) for element in line.strip()] for line in f)
    tGrid = TreeGrid(fGrid)
    totalTreesVisible = tGrid.getTotalVisibleTrees()
    print(f"Trees visible: {totalTreesVisible}")

def runTests():
    testLinesForDirection()
    testGetTotalVisibleTrees()
    print("All tests passed.")

runTests()
main()