import cv2
# -------------------------------------- #
def sort_Detector_position(Detector):
    XY = sorted(Detector)
    idx = 0
    for i in range(1, len(XY)):
        if XY[i][0] - XY[i-1][0] >= 10:
            idx = i
            break
    # print(idx)
    return XY[idx:], sorted(XY[0:idx], key = lambda x: x[1])

def IsDetector(Rect_edge, cnts, img):
    for e in Rect_edge:
        X1, Y1 = e[0]
        X2, Y2 = e[1]
        IN = True
        for p in cnts:
            xi, yi = p[0]
            if not (X1 <= xi <= X2 and Y1 <= yi <= Y2):
                IN = False
                break
        if IN:  
            return True 
    return False
# -------------------------------------------- #