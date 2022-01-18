from sympy import im
import cashflow_complete
import cv2

def extract_data(img_path):
    img = cv2.imread(img_path)

    d = cashflow_complete.predictIMG(img)