"""
command regular expressions:
list: ^\$ ls$
change dir: ^\$ cd (\.\.|[a-zA-Z]+)$

output regular expressions:
file: ^([\d]+) (.+)$
directory: ^dir [a-zA-Z]+$
"""

class Dir:
    pass

class Node:
    def __init__(self, name: str, parentDir: Dir):
        self.name = name
        self.parent = parentDir
        if parentDir:
            parentDir.addChild(self)

    def getSize(self):
        return NotImplementedError("Tried to call Node.getSize() instead of the subclass method.")
    
    def getParent(self):
        return self.parent
    
    def getName(self):
        return self.name
    
    def isDir(self):
        pass

class Dir(Node):
    def __init__(self, name: str, parentDir: Dir):
        super().__init__(name, parentDir)
        self.children: dict[(str, Dir)] = {}
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"dir {self.name}"
    
    def addChild(self, child: Node):
        self.children[child.getName()] = child
    
    def getChild(self, childName: str) -> str:
        return self.children[childName]
    
    def getSize(self):
        return sum([child.getSize() for child in self.children.values()])
    
    def isDir(self):
        return True
    
    def getSizePart1(self) -> int:
        """
        We need to traverse the directory tree and find all directories whose size is less than or equal to 100,000.
        
        We can do this via Breadth First Search. As we visit each directory, we will calculate its size and add it 
        to a list if it does not exceed 100,000.
        """
        runningTotal = 0
        toVisit = [self]
        while len(toVisit) != 0:
            currentNode = toVisit.pop(0)
            toVisit += filter(lambda n: n.isDir(), currentNode.children.values())
            size = currentNode.getSize()
            if size <= 100000:
                runningTotal += size
        return runningTotal
    
    def getSizePart2(self) -> int:
        totalDiskSpace = 70000000
        spaceNeeded = 30000000
        maxUsedSpace = totalDiskSpace - spaceNeeded
        sizeRootDir = self.getSize()
        excess = sizeRootDir - maxUsedSpace
        if excess > 0:
            deletionCandidates = []
            toVisit = [self]
            while len(toVisit) != 0:
                currentNode = toVisit.pop(0)
                toVisit += filter(lambda n: n.isDir(), currentNode.children.values())
                size = currentNode.getSize()
                if size >= excess:
                    deletionCandidates.append(size)
            deletionCandidates.sort()
            return deletionCandidates[0]
        else:
            return 0


class File(Node):
    def __init__(self, name: str, parentDir: Dir, size: int):
        super().__init__(name, parentDir)
        self.size = size
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.size} {self.name}"
    
    def getSize(self):
        return self.size

def testGetSize():
    rootDir = Dir("/", None)
    subDir = Dir("sub", rootDir)
    File("hello.txt", subDir, 5)
    File("gitignore.txt", subDir, 6)
    File("readme.txt", rootDir, 7)
    assert(rootDir.getSize() == 18)

def runTests():
    testGetSize()

def main():
    with open("7_input.txt", "r") as f:
        root = None
        cwd = None
        line = f.readline()
        line_counter = 1
        while line != "\n" and line != "":
            tokens = line.strip().split()
            if tokens[0] == '$':
                if tokens[1] == 'cd':
                    if tokens[2] == '/':
                        root = Dir("root", None)
                        cwd = root
                    elif tokens[2] == '..':
                        cwd = cwd.getParent()
                    else:
                        cwd = cwd.getChild(tokens[2])
                else: # list command ("$ ls")
                    pass
            elif tokens[0] == 'dir':
                cwd.addChild(Dir(tokens[1], cwd))
            else: # file (ex: "216592 pcg.wnr")
                cwd.addChild(File(tokens[1], cwd, int(tokens[0])))
            line = f.readline()
            line_counter += 1
        #print(root.getSizePart1())
        print(root.getSizePart2())

main()