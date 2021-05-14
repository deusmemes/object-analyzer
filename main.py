import flask_server as server
from analyzer import Analyzer
import cv2 as cv


server.run()

anlz = Analyzer()
# anlz.analyze([cv.imread('./data/img1.tif'), cv.imread('./data/img2.tif'), cv.imread('./data/img1.tif')])
