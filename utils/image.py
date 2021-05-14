import cv2 as cv
import numpy as np


def normalize(image):
    norm_image = np.zeros((400, 400))
    final_image = cv.normalize(image, norm_image, 0, 255, cv.NORM_MINMAX)
    return final_image


def resize(image, dsize):
    output = cv.resize(image, (dsize[0], dsize[1]), interpolation=cv.INTER_AREA)
    return output


def get_mask_area(mask):
    count = cv.countNonZero(mask)
    return count


def add_mask(image, mask):
    image[mask == 1] = (0, 0, 255)
    return image


def convert_to_gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
