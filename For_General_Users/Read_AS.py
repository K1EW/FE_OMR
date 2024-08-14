import numpy as np
#import cv2

def Read_Shade(Sheet, imgThres, W, Black_Ratio, X_axis_detector, Y_axis_detector):
    SHADE_FOUND = list()
    for i in range(len(Y_axis_detector)):
        x1, y1, w1, h1 = Y_axis_detector[i]
        y1 += 6
        for j in range(len(X_axis_detector)):
            x2, y2, w2, h2 = X_axis_detector[j]
            x2 -= 2
            
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
                        #cv2.rectangle(Sheet, (x2 + l, y1 + k), (x2 + W + l, y1 - W + k), (255, 0, 0), 1)
                        SHADE_FOUND.append((i+1, j+1))
                        SKIP = True
                        break
            #cv2.rectangle(Sheet, (x2, y1), (x2 + W, y1 - W), (255, 0, 0), 1)

    '''cv2.imshow('Detect_Area', Sheet)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    return SHADE_FOUND