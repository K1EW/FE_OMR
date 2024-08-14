import importlib

def Load_module(Subject_ID):
    module = importlib.import_module("Inspection_code." + Subject_ID)
    return module
    
def ConvertXY(SHADE_FOUND, Subject_ID):
    module = Load_module(Subject_ID)
    ANSWER = module.ConvertXY(SHADE_FOUND)
    return ANSWER

def Graded(Ans, SOLUTION, Subject_ID):
    module = Load_module(Subject_ID)
    Score = module.Score(Ans, SOLUTION)
    return Score