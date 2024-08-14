import cv2
# ------------------------------------------------------------------- #

def pero_approx(cnts):
    peri = cv2.arcLength(cnts, True)
    approx = cv2.approxPolyDP(cnts, 0.090 * peri, True)
    return approx
# ------------------------------------------------------------------- #

def scope_detector(cnts, rect_Edge):
    approx = pero_approx(cnts)
    if len(approx) == 3:
        for e in rect_Edge:
            X1, Y1 = e[0]
            X2, Y2 = e[1]
            IN = True
            for p in approx:
                xi, yi = p[0]
                if not (X1 <= xi <= X2 and Y1 <= yi <= Y2):
                    IN = False
                    break
            if IN:  
                return True 
    return False
# ------------------------------------------------------------------- #                

def findCorner(point):
    maxN = 999999
    for i in range(len(point)):
        p = point[i]
        if maxN > int(p[0] + p[1]):
            idxLU = i
            maxN = int(p[0] + p[1])

    minN = -1
    for i in range(len(point)):
        p = point[i]
        if maxN < int(p[0] + p[1]):
            idxRD = i
            maxN = int(p[0] + p[1])

    maxN = -1
    for i in range(len(point)):
        p = point[i]
        if maxN < int(p[1] - p[0]):
            idxRU = i
            maxN = int(p[1] - p[0])

    maxN = -1
    for i in range(len(point)):
        p = point[i]
        if maxN < int(p[0] - p[1]):
            idxLD = i
            maxN = int(p[0] - p[1])

    return [point[idxLU], point[idxLD], point[idxRU], point[idxRD]]
# ------------------------------------------------------------------- #

def IsDetector(Rect_edge, cnts, Sheet):
    if cv2.contourArea(cnts) >= 40:
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
# ------------------------------------------------------------------- #

def sort_Detector_position(Detector):
    XY = sorted(Detector)
    idx = 0
    for i in range(1, len(XY)):
        if XY[i][0] - XY[i-1][0] >= 10:
            idx = i
            break
    # print(idx)
    return XY[idx:], sorted(XY[0:idx], key = lambda x: x[1])
# ------------------------------------------------------------------- #