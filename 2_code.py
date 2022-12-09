"""
(R)ock (P)aper (S)cissors
R beats S
P beats R
S beats P

A = X = Rock
B = Y = Paper
C = Z = Scissors

A beats Z
B beats X
C beats Y
"""

DECODER_DICT = dict()
DECODER_DICT["A"] = DECODER_DICT["X"] = "R"
DECODER_DICT["B"] = DECODER_DICT["Y"] = "P"
DECODER_DICT["C"] = DECODER_DICT["Z"] = "S"

SCORE_DICT = dict()
SCORE_DICT["R"] = 1
SCORE_DICT["P"] = 2
SCORE_DICT["S"] = 3
SCORE_DICT["RP"] = (0,6)
SCORE_DICT["PR"] = (6,0)
SCORE_DICT["RS"] = (6,0)
SCORE_DICT["SR"] = (0,6)
SCORE_DICT["RS"] = (6,0)
SCORE_DICT["PS"] = (0,6)
SCORE_DICT["SP"] = (6,0)

"""
X means you need to lose
Y means draw
Z means win
"""
RPS_DICT = dict()
RPS_DICT["RX"] = "S"
RPS_DICT["RZ"] = "P"
RPS_DICT["PX"] = "R"
RPS_DICT["PZ"] = "S"
RPS_DICT["SX"] = "P"
RPS_DICT["SZ"] = "R"

def calculateRoundScores(opponent_selection: str, my_selection: str) -> tuple[int, int]:
    # calculate the score of each player's selection
    selection_scores = (SCORE_DICT[opponent_selection], SCORE_DICT[my_selection])

    round_scores = None
    if opponent_selection == my_selection:
        round_scores = (3,3)
    else:
        round_scores = SCORE_DICT[opponent_selection + my_selection]

    return (selection_scores[0] + round_scores[0], 
            selection_scores[1] + round_scores[1])

def getSelection(opponent_selection: str, desired_result: str) -> str:
    if desired_result == "Y":
        return opponent_selection
    else:
        return RPS_DICT[opponent_selection + desired_result]

def part1():
    f = open("2_input.txt", "r")
    scores = []
    for line in f.readlines():
        opponent_selection, my_selection = map(lambda s: DECODER_DICT[s], line.strip().split())
        scores.append(calculateRoundScores(opponent_selection, my_selection))
    myScore = sum(map(lambda x: x[1], scores))
    print(f'My score: {myScore}')

def part2():
    f = open("2_input.txt", "r")
    scores = []
    for line in f.readlines():
        opponent_selection, desired_result = line.strip().split()
        opponent_selection = DECODER_DICT[opponent_selection]
        my_selection = getSelection(opponent_selection, desired_result)
        scores.append(calculateRoundScores(opponent_selection, my_selection))
    myScore = sum(map(lambda x: x[1], scores))
    print(f'My score: {myScore}')

part2()