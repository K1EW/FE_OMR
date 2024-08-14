# import cv2
import numpy as np
# ------------------------------------------------------------------------ #
def READ_SHADE(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio):
    SHADE_Found = list()
    for i in range(25, 57):
        x1, y1, w1, h1 = Y_axis_detector[i]
        y1 += 7
        for j in range(1, 42):
            x2, y2, w2, h2 = X_axis_detector[j]
            x2 -= 1

            MAX_Black = -5
            SKIP = False
            for k in [0, -1, 1, 2, -2]:
                if SKIP: break
                for l in [0, -1, 1, 2, -2]:
                    roi = imgThres[y1-W+k:y1+k, x2+l:x2+W+l]
                    black_pixels = np.sum(roi == 255)

                    if black_pixels <= (W * W) * 0.40: 
                        SKIP = True
                        break

                    if black_pixels >= (W * W) * Black_Ratio:
                        #cv2.rectangle(img, (x2 + l, y1 + k), (x2 + W + l, y1 - W + k), (255, 0, 0), 2)
                        SHADE_Found.append((i+1, j+1))
                        SKIP = True
                        break
            #cv2.rectangle(img, (x2, y1), (x2 + W, y1 - W), (255, 0, 0), 1)
    #cv2.imshow('Detect_Area', img)
    #cv2.waitKey(0)
    return SHADE_Found
# ------------------------------------------------------------------------ #
def READ_information(img, imgThres, X_axis_detector, Y_axis_detector, W, Black_Ratio):
    Subject_ID = 'XX'
    ID = 'XXXXXXXX'
    Cancel = False

    for i in range(2, 12):
        x1, y1, w1, h1 = Y_axis_detector[i]
        y1 += 7
        for j in range(31, 42):
            x2, y2, w2, h2 = X_axis_detector[j]
            x2 -= 3
            
            MAX_Black = -5
            for k in range(-2, 3):
                for l in range(-2, 3):
                    roi = imgThres[y1-W+k:y1+k, x2+l:x2+W+l]
                    black_pixels = np.sum(roi == 255)
                    MAX_Black = max(MAX_Black, black_pixels)

            if MAX_Black >= (W * W) * Black_Ratio:
                if 31 <= j <= 32:
                    Subject_ID = Subject_ID[:j-31] + str(i-2) + Subject_ID[j-30:]
                elif j >= 34:
                    ID = ID[:j-34] + str(i-2) + ID[j-33:]      
                #cv2.rectangle(img, (x2, y1), (x2 + W, y1 - W), (255, 0, 0), 1)         

    x1, y1, w1, h1 = Y_axis_detector[10]
    x2, y2, w2, h2 = X_axis_detector[4]
    y1 += 6
    x2 -= 5
    
    MAX_Black = -5
    for k in range(-2, 3):
        for l in range(-2, 3):
            roi = imgThres[y1-W+k:y1+k, x2+l:x2+W+l]
            black_pixels = np.sum(roi == 255)
            MAX_Black = max(MAX_Black, black_pixels)

    if MAX_Black >= (W * W) * Black_Ratio:
        Cancel = True
    #cv2.rectangle(img, (x2 + l, y1 + k), (x2 + W + l, y1 - W + k), (255, 0, 0), 1)

    # print((ID, Subject_ID, Cancel)) 
    return (ID, Subject_ID, Cancel)
# ------------------------------------------------------------------------ #
        
