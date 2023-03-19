# import the necessary packages
from datetime import datetime
from PIL import Image

import numpy
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import os
import ctypes
import sys

def diff_func(file1, file2, mode, path_folder_result):
    """
    .:param file1: expect image
    .:param file2: real image
    .:param mode: mode run file/ mode run folder
    .    function compare between 2 image file and draw red square on each different
    .    save result into result folder
    """
    # load file image 1 and image 2
    fileImage1 = cv2.imread(file1)
    fileImage2 = cv2.imread(file2)

    # check size two file input
    try:
        if(fileImage1.shape[0] != fileImage2.shape[0] or fileImage1.shape[1] != fileImage2.shape[1]):
            write_log('File ' + file1 + ' and file ' + file2 +' compare not same size.')
            m_box('Error003', 'File ' + file1 + ' and file ' + file2 +' compare not same size.', 0)
            return 2
    except:
        write_log('File ' + file1 + ' and file ' + file2 +' can not compare')
        m_box('Error003', 'File ' + file1 + ' and file ' + file2 +' can not compare', 0)
        return 3

    # convert to grayscale two file input
    grayImage1 = cv2.cvtColor(fileImage1, cv2.COLOR_BGR2GRAY)
    grayImage2 = cv2.cvtColor(fileImage2, cv2.COLOR_BGR2GRAY)

    # ensuring check difference two image and return
    (score, diff) = compare_ssim(grayImage1, grayImage2, full=True)
    diff = (diff * 255).astype("uint8")
    write_log("The score two file mapping: {}".format(score))

    # followed by finding contours to  obtain the regions of the two input images that difference
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    imageA = numpy.concatenate((fileImage1, fileImage2), axis=1)
    # loop over the contours
    i = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the bounding box for images diff
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(fileImage1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(fileImage2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    st = file1[file1.rfind("/") + 1:]
    write_log('Filename: %s' % st)
    # save the output image
    imageB = numpy.concatenate((imageA, fileImage1), axis=1)
    name = "result_" + st

    # save result when diff image 1 and image 2
    rs = 0
    if score < 1.0:
        cv2.imwrite(path_folder_result + st, fileImage1)
        cv2.imwrite(path_folder_result + name, imageB)
        rs = 1
    # After run check then should show file
    if mode == 0 and rs == 1:
        imm = Image.open(path_folder_result + name)
        imm.show()
    return rs

def diff_folder(expectedFile, realFile, mode, path_folder_result):
    """
    .:param file1: expect image
    .:param file2: real image
    .:param mode: mode run file/ mode run folder
    .    function compare between 2 image file and draw red square on each different
    .    save result into result folder
    """
    # load file image 1 and image 2
    fileImage1 = cv2.imread(expectedFile)
    fileImage2 = cv2.imread(realFile)

    # check size two file input
    try:
        if(fileImage1.shape[0] != fileImage2.shape[0] or fileImage1.shape[1] != fileImage2.shape[1]):
            write_log('File ' + expectedFile + ' and file ' + realFile +' compare not same size.')
            return 2
    except:
        write_log('File ' + expectedFile + ' and file ' + realFile +' can not compare')
        return 3

    # convert to grayscale two file input
    grayImage1 = cv2.cvtColor(fileImage1, cv2.COLOR_BGR2GRAY)
    grayImage2 = cv2.cvtColor(fileImage2, cv2.COLOR_BGR2GRAY)

    # ensuring check difference two image and return
    (score, diff) = compare_ssim(grayImage1, grayImage2, full=True)
    diff = (diff * 255).astype("uint8")
    # write_log("The score two file mapping: {}".format(score))

    # followed by finding contours to  obtain the regions of the two input images that difference
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    imageA = numpy.concatenate((fileImage1, fileImage2), axis=1)
    # loop over the contours
    # print(len(cnts))
    i = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the bounding box for images diff
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(fileImage1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(fileImage2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    st = expectedFile[expectedFile.rfind("/") + 1:]
    
    # save the output image
    imageB = numpy.concatenate((imageA, fileImage1), axis=1)
    name = "result_" + st
    # save result when diff image 1 and image 2
    rs = 0
    if score < 1.0:
        cv2.imwrite(path_folder_result + st, fileImage1)
        cv2.imwrite(path_folder_result + name, imageB)
        rs = 1
        
    return rs

def write_log(text):
    print(text)
    now = datetime.now().strftime('%m%d%Y')
    name = os.getcwd().title() + '/log' + '/' + "log_" + now + ".txt"
    with open(name, 'a+') as f:
        f.write(text + '\n')
        f.close()

def m_box(title, text, style):
    write_log(title + ":" + text)
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
