def Check_Area(i, j):
    return ID_Area(i, j) or Subject_ID_Area(i, j) or \
           Cancel_Area(i, j) or Multiple_Choice_Area(i, j) or \
           Multiple_Choice_Area(i, j) or Objective_Area(i, j)

def ID_Area(i, j):
    return 3 <= i <= 12 and 40 <= j <= 47

def Subject_ID_Area(i, j):
    return 3 <= i <= 12 and 36 <= j <= 38

def Cancel_Area(i, j):
    return i == 11 and j == 4

def Multiple_Choice_Area(i, j):
    return ((28 <= i <= 32) or (35 <= i <= 39)) and \
           (1 <= (j - 8) % 7 <= 5 and 8 <= j <= 41)

def Objective_Area(i, j):
    return (44 <= i <= 53 or 57 <= i <= 66) and \
           0 <= (j - 5) % 8 <= 6 and (j - 5) % 8 != 4 and 4 <= j <= 43

def get_No_Ques(i, j):
    col = (j - 8) // 7
    if 28 <= i <= 32: return (5 * col) + i - 28
    if 35 <= i <= 39: return (5 * col) + i - 10

    if 44 <= i <= 53: return (j - 5) // 8 + 50
    if 57 <= i <= 66: return (j - 5) // 8 + 55

def get_choice(i, j):
    return str((j - 8) % 7) if 1 <= (j - 8) % 7 <= 5 else ''

def get_idx(i, j):
    return (j - 5) % 8

def get_Num(i, j):
    return str((i - 44) % 13) if 0 <= (i - 44) % 13 <= 9 else ''
# ---------------------------------------------- #
def ConvertXY(Shade_Found):
    ID = "XXXXXXXX"
    Subject_ID = "XXX"
    Cancel = False
    Answer = ['' for i in range(50)] + ['XXXX.XX' for i in range(10)]

    for i, j in Shade_Found:
        if ID_Area(i, j):
            ID = ID[:j-40] + str(i-3) + ID[j-39:]

        if Subject_ID_Area(i, j):
            Subject_ID = Subject_ID[:j-36] + str(i-3) + Subject_ID[j-35:]

        if Cancel_Area(i, j):
            Cancel = True

        if Multiple_Choice_Area(i, j):
            Answer[get_No_Ques(i, j)] += get_choice(i, j)
        
        if Objective_Area(i, j):
            Q = get_No_Ques(i, j)
            idx = get_idx(i, j)
            N = get_Num(i, j)
            if N != '': 
                if Answer[Q][idx] != 'X':
                    Answer[Q] += 'X'
                Answer[Q] = Answer[Q][:idx] + N + Answer[Q][idx+1:]

    #print(ID, Subject_ID, Cancel)
    #print(Answer)
    return (ID, Subject_ID, Cancel), Answer

# ---------------------------------------------- #
def graded(Ans, Solution):
    Math = Chem = Phys = 0
    return (Math, Chem, Phys)