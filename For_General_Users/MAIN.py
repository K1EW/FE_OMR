import os
import cv2
import time
import shutil
import Grading
import Read_AS
import Read_Paper

S = time.time()

W = 8
Black_Ratio = 0.80

for f_Answersheet in os.listdir("For_General_Users/Solution"):
    #Sheet = Read_Paper.get_AnswerSheet("For_General_Users/Solution/" + f_Answersheet, shift = False)
    pass

for f_Answersheet in os.listdir("For_General_Users/TestCase"):
    try:
        Sheet = Read_Paper.get_AnswerSheet("For_General_Users/TestCase/" + f_Answersheet, shift = True)
        X_axis_detector, Y_axis_detector, imgThres = Read_Paper.get_XY_Detector_and_imgThes(Sheet)

        # Read Shade
        Shade_Found = Read_AS.Read_Shade(Sheet, imgThres, W, Black_Ratio, X_axis_detector, Y_axis_detector)
        DATA, ANS   = Grading.ConvertXY(Shade_Found)
        
        '''FILENAME = "For_General_Users/Proof_Image/"  + DATA[1] + '_' + DATA[0] + '.png'
        cv2.imwrite(FILENAME, Sheet)'''

        print(DATA)

    except: 
        print(f_Answersheet)

try:    
    shutil.rmtree('For_General_Users/__pycache__')
except: 
    pass

total = time.time() - S
print('TIME USED =', total, 'seconds')
print('TIME USED =', int(total // 3600), 'hour', int(total // 60), 'min', int(total % 60) + 1, 'seconds')