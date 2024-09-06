import cv2
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

PAPER_WIDTH = 538
BIN_THRESHOLD = 230
WHITE_PERCENTAGE_THRESHOLD = 0.4

class Student:
    def __init__(self, id):
        self.id = id

def create_paper(student: Student, exam_id: str):
    pdf_path = "./fe18_fest_alevel_answer_sheet.pdf"
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    circle_pdf_path = "canvas.pdf"
    c = canvas.Canvas(circle_pdf_path, pagesize=A4)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    for idx, digit in enumerate(exam_id):
        c.circle(419+14*idx, 781-(11.25)*int(digit), 5, fill=1)
        c.drawString(416+14*idx, 790, digit)
    for idx, digit in enumerate(student.id):
        c.circle(461+14*idx, 781-(11.25)*int(digit), 5, fill=1)
        c.drawString(459+14*idx, 790, digit)
    for idx, digit in enumerate(student.id):
        c.drawString(275+14*idx, 765, digit)
    c.save()

    with open(circle_pdf_path, "rb") as circle_pdf:
        circle_reader = PdfReader(circle_pdf)
        writer.add_page(reader.pages[0])
        writer.pages[0].merge_page(circle_reader.pages[0])
    
    with open("annotated.pdf", "wb") as f:
        writer.write(f)

AXIS_DETECTOR_BOUNDARY = [[(0, 0), (30, 760)], [(0, 730), (540,760)]]

def is_detector(contour):
    for boundary in AXIS_DETECTOR_BOUNDARY:
        (x1, y1), (x2, y2) = boundary
        cx, cy, cw, ch = cv2.boundingRect(contour)
        if x1 <= cx and cx + cw <= x2 and y1 <= cy and cy + ch <= y2:
            return True
    return False

def get_axis_detector(path: str):
    # pre-processing
    img = cv2.imread(path)
    scaling_ratio = PAPER_WIDTH / img.shape[1]
    h, w = int(img.shape[0] * scaling_ratio), int(img.shape[1] * scaling_ratio)
    img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(img_gray, BIN_THRESHOLD, 255, cv2.THRESH_BINARY_INV)

    # find contours
    contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # filter out the contours that are not inside the detector boundary
    detectors = [cv2.boundingRect(contour) for contour in contours if is_detector(contour)]
    x_detectors = sorted([detector for detector in detectors if detector[2] < detector[3]], key=lambda x: x[0])
    y_detectors = sorted([detector for detector in detectors if detector[2] > detector[3]], key=lambda x: x[1])

    # draw the detector contours
    for idx, (x, y, w, h) in enumerate(x_detectors):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0 + int(idx/len(detectors) * 255), 255 - int(idx/len(detectors) * 255), 0), 1)
    for idx, (x, y, w, h) in enumerate(y_detectors):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0 + int(idx/len(detectors) * 255), 255 - int(idx/len(detectors) * 255), 0), 1)
    # draw a line between the first and last y-detector
    cv2.line(img, (y_detectors[0][0], y_detectors[0][1]), (y_detectors[-1][0], y_detectors[-1][1]), (0, 0, 255), 1)
    cv2.imshow("Detectors", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
