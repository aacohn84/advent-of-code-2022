def maxCalories() -> int:
    f = open("1_input.txt", "r")
    max_cals = 0
    tally = 0
    for line in f.readlines():
        line = line.strip()
        if line == "":
            max_cals = max(max_cals, tally)
            tally = 0
        else:
            tally += int(line)
    f.close()
    return max_cals

def top3() -> int:
    f = open("1_input.txt", "r")
    tally = 0
    cals = []
    for line in f.readlines():
        line = line.strip()
        if line == "":
            cals.append(tally)
            tally = 0
        else:
            tally += int(line)
    cals.sort(reverse=True)
    f.close()
    return sum(cals[0:3])

def main():
    print(maxCalories())
    print(top3())

main()