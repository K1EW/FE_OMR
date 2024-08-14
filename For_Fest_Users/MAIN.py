# from Install_package import *
# Install_Package()
# ---------------------------------------------------------- #
import os
import time
import shutil
import Grading
import READ_AS
import READ_IMG 
# ---------------------------------------------------------- #
S = time.time()

W = 8
Black_Ratio = 0.70

# READ_Solution
path = "./Solution"
SOLUTION = dict()
for f_answersheet in os.listdir(path):
    X_axis_detector, Y_axis_detector, imgThres, img = READ_IMG.get_XY_Detector_and_imgThes(path + "/" + f_answersheet)

    Subject_ID  = READ_AS.READ_information(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio)[1]
    SHADE_Found = READ_AS.READ_SHADE(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio)
    ANSWER      = Grading.ConvertXY(SHADE_Found, Subject_ID)
    
    if Subject_ID not in SOLUTION: SOLUTION[Subject_ID] = ANSWER

print(SOLUTION)
# ---------------------------------------------------------- #       
# ---------------------------------------------------------- #
# READ_ANSWER
path = "./AS_Scanned"
for f_answersheet in os.listdir(path):
    X_axis_detector, Y_axis_detector, imgThres, img = READ_IMG.get_XY_Detector_and_imgThes(path + '/' + f_answersheet)

    ID, Subject_ID, Cancel = READ_AS.READ_information(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio)
    SHADE_Found            = READ_AS.READ_SHADE(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio)
    ANSWER                 = Grading.ConvertXY(SHADE_Found, Subject_ID)

    Score = 0
    if Subject_ID in SOLUTION: 
        Score = Grading.Graded(ANSWER, SOLUTION[Subject_ID], Subject_ID) * int(not Cancel)

        # Rename AnswerSheet File
        '''dot_idx = f_answersheet.rfind('.')
        File_extension = f_answersheet[dot_idx:]
        os.rename(path + '/' + f_answersheet, path + '/' + Subject_ID + '_' + ID + File_extension)'''
    
    print((ID, Subject_ID, Cancel, Score))
    #print((ID, Subject_ID, Cancel, Score), '\n', ANSWER, '--> Finished')
# ---------------------------------------------------------- #
# ---------------------------------------------------------- #
try:    
    shutil.rmtree('For_Fest_Users/__pycache__')
    shutil.rmtree('For_Fest_Users/Inspection_code/__pycache__')
except: 
    pass
# Uninstall_Package()
# ---------------------------------------------------------- #
total = time.time() - S
print('TIME USED =', total, 'seconds')
print('TIME USED =', int(total // 3600), 'hour', int(total // 60), 'min', int(total % 60) + 1, 'seconds')
