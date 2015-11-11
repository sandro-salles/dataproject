#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


def _cv2open(filename):
    obj = cv2.imread(filename)
    obj = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
    obj = cv2.Canny(obj, 50, 200)

    if obj is None:
        raise IOError('cv2 read file error:' + filename)
    return obj


def findall(search_file, image_file, threshold=0.7):
    '''
    Locate image position with cv2.templateFind

    Use pixel match to find pictures.

    Args:
        search_file(string): filename of search object
        image_file(string): filename of image to search on
        threshold: optional variable, to ensure the match rate should >= threshold

    Returns:
        A tuple like (x, y) or None if nothing found

    Raises:
        IOError: when file read error
    '''
    search = _cv2open(search_file)
    image = _cv2open(image_file)

    w, h = search.shape[::-1]

    method = cv2.TM_CCOEFF
    # method = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(image, search, method)

    points = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        if max_val > threshold:
            # floodfill the already found area
            sx, sy = top_left
            for x in range(sx - w / 2, sx + w / 2):
                for y in range(sy - h / 2, sy + h / 2):
                    try:
                        res[y][x] = np.float32(-10000)  # -MAX
                    except IndexError:  # ignore out of bounds
                        pass

            (startX, startY) = (int(max_loc[0]), int(max_loc[1]))
            (endX, endY) = (int(max_loc[0] + w), int(max_loc[1] + h))
            points.append((startX, startY, endX, endY))
        else:
            break
    return points

if __name__ == '__main__':
    search_file = '/vagrant/char-n.jpg'
    image_file = '/vagrant/captcha-n.jpg'
    threshold = 1000000
    positions = findall(search_file, image_file, threshold)

    if positions:
        w, h = cv2.imread(search_file, 0).shape[::-1]
        img = cv2.imread(image_file)
        for (startX, startY, endX, endY) in positions:
            cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)

        cv2.imwrite("./outlined.jpg", img)

        # from matplotlib import pyplot as plt
        # plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
        # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        # plt.show()
