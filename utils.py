import cv2
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

PAPER_WIDTH = 538
BIN_THRESHOLD = 230
AXIS_DETECTOR_BOUNDARY = [[(0, 0), (30, 760)], [(0, 730), (540,760)]]
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
    c.save()

    with open(circle_pdf_path, "rb") as circle_pdf:
        circle_reader = PdfReader(circle_pdf)
        writer.add_page(reader.pages[0])
        writer.pages[0].merge_page(circle_reader.pages[0])
    
    with open("annotated.pdf", "wb") as f:
        writer.write(f)

def is_detector(contour):
    for boundary in AXIS_DETECTOR_BOUNDARY:
        (x1, y1), (x2, y2) = boundary
        cx, cy, ch, cw = cv2.boundingRect(contour)
        if x1 <= cx <= x2 and y1 <= cy <= y2:
            return True
    return False

def get_crop_section(x1, x2, y1, y2, offset, x_detectors, y_detectors, img):
    distance_between_detectors = x_detectors[1][0] - (x_detectors[0][0] + x_detectors[0][2])
    upper_left = (x_detectors[x1][0] - distance_between_detectors//2 * offset[3], y_detectors[y1][1] - distance_between_detectors//2 * offset[0])
    lower_right = (x_detectors[x2][0] + x_detectors[x2][2] + distance_between_detectors//2 * offset[1], y_detectors[y2][1] + y_detectors[y2][3] + distance_between_detectors//2 * offset[2])
    crop_section = img[upper_left[1]:lower_right[1], upper_left[0]:lower_right[0]]

    cv2.rectangle(img, upper_left, lower_right, (0, 0, 255), 1)
    return crop_section

def read_exam_id(img):
    exam_id = "--"
    # devide the image into 10 by 2 grid using its width and height
    h, w = img.shape
    grid_h, grid_w = h // 2, w // 10
    # check each grid
    return exam_id

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
        cv2.rectangle(binary_img, (x, y), (x + w, y + h), (0 + int(idx/len(detectors) * 255), 255 - int(idx/len(detectors) * 255), 0), 2)
    for idx, (x, y, w, h) in enumerate(y_detectors):
        cv2.rectangle(binary_img, (x, y), (x + w, y + h), (0 + int(idx/len(detectors) * 255), 255 - int(idx/len(detectors) * 255), 0), 2)

    crop_sections = []
    # exam_id
    offset = [False, True, True, False]
    meta = {"section_type": "exam_id"}
    crop_sections.append((get_crop_section(31, 32, 2, 11, offset, x_detectors, y_detectors, binary_img), meta))
    # id
    offset = [False, True, True, True]
    meta = {"section_type": "id", "digits": 8}
    crop_sections.append((get_crop_section(34, len(x_detectors) - 1, 2, 11, offset, x_detectors, y_detectors, binary_img), meta))
    # cancel
    offset = [True, True, True, True]
    meta = {"section_type": "cancel"}
    crop_sections.append((get_crop_section(4, 4, 10, 10, offset, x_detectors, y_detectors, binary_img), meta))
    # choice
    meta = {"section_type": "choice", "choices": 5, "items": 5}
    for i in range(0, 5):
        offset = [True, True, True, True]
        crop_sections.append((get_crop_section(5 + i*7, 9 + i*7, 34, 38, offset, x_detectors, y_detectors, binary_img), meta))
    # fill
    meta = {"section_type": "fill", "items": 5}
    for i in range(0, 5):
        offset = [True, True, True, True]
        crop_sections.append((get_crop_section(2 + i*8, 8 + i*8, 45, 54, offset, x_detectors, y_detectors, binary_img), meta))

    section, meta = crop_sections[0]
    exam_id = read_exam_id(section)

    # for binary_img, meta in crop_sections:
    #     cv2.imshow(meta["section_type"], binary_img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
