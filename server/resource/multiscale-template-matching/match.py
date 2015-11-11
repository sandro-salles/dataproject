# USAGE
# python match.py --template cod_logo.png --images images

# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
from matplotlib import pyplot as plt

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True,
                help="Path to template image")
ap.add_argument("-i", "--images", required=True,
                help="Path to images where template will be matched")
ap.add_argument("-v", "--visualize",
                help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread(args["template"])
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.bilateralFilter(template, 11, 17, 17)
template = cv2.Canny(template, 50, 200)
cv2.imwrite("./outlinechar.jpg", template)
(tH, tW) = template.shape[:2]
# cv2.imshow("Template", template)

# loop over the images to find the template in
for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # load the image, convert it to grayscale, and initialize the
    # bookkeeping variable to keep track of the matched region
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoisingColored(gray,None,10,10,7,21)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    (cnts, _) = cv2.findContours(gray.copy(),
                                 cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    sorted_cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    top_cnts = []
    removed_cnts = []

    for i, cnt in enumerate(sorted_cnts):
        if i <= 4:
            top_cnts.append(cnt)
        else:
            removed_cnts.append(cnt)

    mask = np.ones(image.shape[:2], dtype="uint8") * 255

    for c in removed_cnts:
        cv2.drawContours(mask, [c], -1, 0, -1)

    #import pdb; pdb.set_trace()

    gray = cv2.bitwise_and(gray, gray, mask=mask)

    # detect edges in the resized, grayscale image and apply template
    # matching to find the template in the image
    edged = cv2.Canny(gray, 50, 200)

    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)

    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    print maxVal
    if maxVal >= 857441:
        r = gray.shape[1] / float(gray.shape[1])

        # unpack the bookkeeping varaible and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        cv2.rectangle(edged, (startX, startY), (endX, endY), (0, 0, 255), 1)

    # import pdb
    # pdb.set_trace()
    # draw a bounding box around the detected result and display the image
    # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imwrite("./outlined.jpg", edged)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
