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

class Dir(Node):
    def __init__(self, name: str, parentDir: Dir):
        super().__init__(name, parentDir)
        self.children: list[dir] = []
    
    def addChild(self, child: Node):
        self.children.append(child)
    
    def getSize(self):
        return sum([child.getSize() for child in self.children])

class File(Node):
    def __init__(self, name: str, parentDir: Dir, size: int):
        super().__init__(name, parentDir)
        self.size = size
    
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