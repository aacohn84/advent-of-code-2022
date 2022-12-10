def fullyContains(a: str, b: str) -> bool:
    a1, a2 = [int(c) for c in a.split("-")]
    b1, b2 = [int(c) for c in b.split("-")]
    return (a1 <= b1 and a2 >= b2) \
        or (b1 <= a1 and b2 >= a2)

def overlaps(a: str, b: str) -> bool:
    a1, a2 = [int(c) for c in a.split("-")]
    b1, b2 = [int(c) for c in b.split("-")]
    
    # case 1: a overlaps with the left side of b
    # case 2: a overlaps with the right side of b
    # case 3: a is fully contained by b
    # case 4: b is fully contained by a
    return (a1 < b1 and a2 >= b1 and a2 <= b2) \
        or (a1 > b1 and a1 <= b2 and a2 > b2) \
        or (a1 <= b1 and a2 >= b2) \
        or (b1 <= a1 and b2 >= a2)

def part1():
    f = open("4_input.txt", "r")
    s = 0
    for line in [l.strip() for l in f.readlines()]:
        first, second = line.split(",")
        if fullyContains(first, second):
            s += 1
    f.close()
    print(s)

def part2():
    f = open("4_input.txt", "r")
    s = 0
    for line in [l.strip() for l in f.readlines()]:
        first, second = line.split(",")
        if overlaps(first, second):
            s += 1
    f.close()
    print(s)

part2()