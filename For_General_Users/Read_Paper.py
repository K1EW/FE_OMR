# ---------------------------------------------------------------------------------- #
import cv2
import pos_det
import numpy as np
# ---------------------------------------------------------------------------------- #
def get_AnswerSheet(FILENAME, shift):
    img = cv2.imread(FILENAME)

    # Pre Processing
    ratio = 600 / img.shape[1]
    h, w = int(img.shape[0] * ratio), int(img.shape[1] * ratio)
    img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)    
    img = np.roll(img, 30 * int(shift), axis = 0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThres = cv2.threshold(imgGray, 253, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    

    rect_Edge = [[(0, 0), (25, h)], [(w-25, 0), (w, h)]]
    XYZ = [pos_det.pero_approx(cnts) for cnts in contours if pos_det.scope_detector(cnts, rect_Edge)]
    _XYZ = list()

    for cnts in XYZ:
        XXYYZZ = cnts.reshape(3, 2)
        _XYZ.append([np.mean(XXYYZZ[:, 0]), np.mean(XXYYZZ[:, 1])])

    _Corner = pos_det.findCorner(_XYZ) 

    H, W = 600, int(600 * 1.414) + 1
    pt1 = np.float32(_Corner)
    pt2 = np.float32([[0, 0], [H, 0], [0, W], [H, W]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    output = cv2.warpPerspective(img, matrix, (H, W))

    return output
# ---------------------------------------------------------------------------------- #
def get_XY_Detector_and_imgThes(Sheet):
    SheetGray = cv2.cvtColor(Sheet, cv2.COLOR_BGR2GRAY)
    _, SheetThres = cv2.threshold(SheetGray, 220, 255, cv2.THRESH_BINARY_INV)

    # Contours
    contours, hierarchy = cv2.findContours(SheetThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Rect_edge = [[(0, 0), (30, 850)], [(0, 820), (600, 850)]]
    XY = [cv2.boundingRect(cnts) for cnts in contours if pos_det.IsDetector(Rect_edge, cnts, Sheet)]
    XYZ = [cnts for cnts in contours if pos_det.IsDetector(Rect_edge, cnts, Sheet)]

    '''cv2.imshow('CON', cv2.drawContours(Sheet, XYZ, -1, (0, 255, 0), 2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    X_axis_detector, Y_axis_detector = pos_det.sort_Detector_position(XY)

    return X_axis_detector, Y_axis_detector, SheetThres
# ---------------------------------------------------------------------------------- #