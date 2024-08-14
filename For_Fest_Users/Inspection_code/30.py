def get_No_Ques(i, j):
    col = (j - 6) // 7
    if 36 <= i <= 44: return (9 * col) + i - 36
    if 48 <= i <= 52: return (5 * col) + i - 3

def get_Choice(i, j):
    return str((j - 5) % 7) if 1 <= (j - 5) % 7 <= 5 else ''
# ---------------------------------------------------------- #
def ConvertXY(SHADE_FOUND):
    # Answer = [Answer]
    ANSWER = ['' for i in range(70)]
    for i, j in SHADE_FOUND:
        if (36 <= i <= 44) or (48 <= i <= 52) and (6 <= j <= 38):
            ANSWER[get_No_Ques(i, j)] += get_Choice(i, j) 
    return ANSWER 
# ---------------------------------------------------------- #
def Score(Ans, SOLUTION):
    score = 0
    for i in range(70):
        if len(Ans[i]) == 1:
            if Ans[i] in SOLUTION[i]:
                score += (4 * int(0 <= i < 60)) + (6 * int(60 <= i < 70))
    return round(score/3, 2)
# ---------------------------------------------------------- #