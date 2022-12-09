def getCommonType(rucksack_contents: str) -> str:
    mid = int(len(rucksack_contents) / 2)
    compartment_1 = rucksack_contents[0:mid]
    compartment_2 = rucksack_contents[mid:]
    c1_hist = dict()
    for t in compartment_1:
        c1_hist[t] = None
    for t in compartment_2:
        if t in c1_hist:
            return t
    raise Exception(f"Couldn't find a common type between the compartments: {compartment_1}, {compartment_2}")

def getCommonTypePart2(rucksack_groups: list[str]) -> str:
    rs1, rs2, rs3 = rucksack_groups
    rs1_hist = dict()
    for ch in rs1:
        rs1_hist[ch] = None
    t = ""
    for ch in rs2:
        if ch in rs1_hist:
            t = ch
            if t in rs3:
                return t
    raise Exception(f"Couldn't find a common type between the rucksacks: {rs1}, {rs2}, {rs3}")

def getPriority(t: str) -> int:
    """
    a-z: 01-26
    A-Z: 27-52
    """
    if t.isupper():
        return ord(t) - 38 # ex: ord("A") = 65, so ord("A") - 38 = 65 - 38 = 27
    else:
        return ord(t) - 96

def part1():
    f = open("3_input.txt", "r")
    s = 0
    for line in f.readlines():
        rucksack_contents = line.strip()
        t = getCommonType(rucksack_contents)
        p = getPriority(t)
        s += p
    f.close()
    print(s)

def part2():
    f = open("3_input.txt", "r")
    lines = [s.strip() for s in f.readlines()]
    num_groups = int(len(lines) / 3)
    s = 0
    for g in range(num_groups):
        rucksacks_in_group = lines[3*g : 3*g + 3]
        t = getCommonTypePart2(rucksacks_in_group)
        p = getPriority(t)
        s += p
    f.close()
    print(s)
part2()