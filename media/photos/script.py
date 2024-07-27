from pyzbar import pyzbar
import cv2

import os

os.chdir('D:\Личное\Програмирование\Django projects\ProductSite\Project\media\photos')


def decode(image):
    decoded_objects = pyzbar.decode(image)
    if decoded_objects:
        return decoded_objects[0].data
    else:
        return False


def run_decoding(image):
    image = str(image).replace('photos/', '')
    img = cv2.imread(image)
    if img.any():
        barcode = decode(img).decode('utf-8')
        return barcode
    else:
        return False
