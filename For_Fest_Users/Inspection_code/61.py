def get_No_Ques(i, j):
    Q = ''
    if 35 <= i <= 39:
        col = (j - 5) // 7
        Q = (5 * col) + i - 35

    if (46 <= i <= 55) and (3 <= j <= 41):
        if (j - 3) % 8 != 4 and (j - 3) % 8 != 7:
            Q = ((j - 3) // 8) + 25
    
    return Q


def get_Choice(i, j):
    Choice = ''
    if 35 <= i <= 39:
        Choice = str((j - 5) % 7) if 1 <= (j - 5) % 7 <= 5 else ''
    return Choice


def get_IDX(i, j):
    return (j - 3) % 8


def Multiple_Choice_Area(i, j):
    return (35 <= i <= 39) and (6 <= j <= 38)


def Objective_Area(i, j):
    return (46 <= i <= 55) and (3 <= j <= 41) and not ((j - 3) % 8 == 4 or (j - 3) % 8 == 7)

# ---------------------------------------------------------- #
def ConvertXY(SHADE_FOUND):
    # Answer = [Answer]
    ANSWER = ['' for i in range(25)] + ['XXXX.XX' for i in range(5)]
    for i, j in SHADE_FOUND:
        if Multiple_Choice_Area(i, j):
            ANSWER[get_No_Ques(i, j)] += get_Choice(i, j)

        if Objective_Area(i, j):
            Q = get_No_Ques(i, j)
            idx = get_IDX(i, j)
            if ANSWER[Q][idx] != 'X':
                ANSWER[Q] += 'X'
            ANSWER[Q] =  ANSWER[Q][:idx] + str(i - 46) + ANSWER[Q][idx+1:]
    return ANSWER 
# ---------------------------------------------------------- #
def Score(Ans, SOLUTION):
    score = 0
    for i in range(25):
        if len(Ans[i]) == 1:
            if Ans[i] in SOLUTION[i]:
                score += 3
    for i in range(25, 30):
        if Ans[i] == SOLUTION[i]:
            score += 5
    return score
# ---------------------------------------------------------- #