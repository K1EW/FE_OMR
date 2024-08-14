import cv2
import pos_det
# ------------------------------------------------------------------------------------------------------------------ #
def get_XY_Detector_and_imgThes(FILENAME):
    img = cv2.imread(FILENAME)
    
    # Pre processesing
    ratio = 538 / img.shape[1]
    h, w = int(img.shape[0] * ratio), int(img.shape[1] * ratio)
    img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThres = cv2.threshold(imgGray, 230, 255, cv2.THRESH_BINARY_INV) # 230 if use 60% paper


    # Contours
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Rect_edge = [[(0, 0), (30, 760)], [(0, 730), (540,760)]]
    # draw Rect_edge on img
    cv2.rectangle(img, Rect_edge[0][0], Rect_edge[0][1], (0, 0, 255), 1)
    cv2.rectangle(img, Rect_edge[1][0], Rect_edge[1][1], (0, 0, 255), 1)

    '''for edge in Rect_edge:
        cv2.rectangle(img, edge[0], edge[1], (0, 0, 255), 2)
    cv2.imshow('Rect_edge', img)
    cv2.waitKey(0)'''

    XY = [cv2.boundingRect(cnts) for cnts in contours if pos_det.IsDetector(Rect_edge, cnts, img)]
    X_axis_detector, Y_axis_detector = pos_det.sort_Detector_position(XY)
    for idx, (x, y, w, h) in enumerate(X_axis_detector):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0 + int(idx/len(XY) * 255), 255 - int(idx/len(XY) * 255), 0), 2)
    for idx, (x, y, w, h) in enumerate(Y_axis_detector):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0 + int(idx/len(XY) * 255), 255 - int(idx/len(XY) * 255), 0), 2)
    cv2.imshow(FILENAME, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return X_axis_detector, Y_axis_detector, imgThres, img
# ------------------------------------------------------------------------------------------------------------------ #
