import cv2
import numpy as np


def capture_photo():
    cap = cv2.VideoCapture(1)  # 1 or 2 for real sense
    ret, frame = cap.read()
    cap.release()
    cv2.imwrite("captured_photo.jpg", frame)

    return "captured_photo.jpg"


captured_photo_path = capture_photo()
cap = cv2.imread(captured_photo_path)
cv2.waitKey(10)
cv2.destroyAllWindows()


def HVS():
    def stack(scale, imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]

        # Check if rows are available
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                    None, scale, scale)
                    if len(imgArray[x][y].shape) == 2:
                        imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank] * rows

            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                             scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor

        return ver

    def empty(s):
        pass

    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 640, 240)
    # hier vul je de waardes in van de kleur die je wilt herkennen
    cv2.createTrackbar('HueMin', 'Trackbars', 0, 179,empty)
    cv2.createTrackbar('HueMax', 'Trackbars', 179, 179, empty)
    cv2.createTrackbar('SatMin', 'Trackbars', 0, 255, empty)
    cv2.createTrackbar('SatMax', 'Trackbars', 255, 255, empty)
    cv2.createTrackbar('ValMin', 'Trackbars', 95, 255, empty)
    cv2.createTrackbar('ValMax', 'Trackbars', 255, 255, empty)

    while True:
        imgO = cv2.imread("captured_photo.jpg")
        img = cv2.resize(imgO, (1000, 450))

        imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos('HueMin', 'Trackbars')
        h_max = cv2.getTrackbarPos('HueMax', 'Trackbars')
        s_min = cv2.getTrackbarPos('SatMin', 'Trackbars')
        s_max = cv2.getTrackbarPos('SatMax', 'Trackbars')
        v_min = cv2.getTrackbarPos('ValMin', 'Trackbars')
        v_max = cv2.getTrackbarPos('ValMax', 'Trackbars')

        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(imghsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(img, img, mask=mask)

        imgStack = stack(0.5, ([img, imghsv], [mask, result]))

        cv2.imshow('Stack', imgStack)
        cv2.imshow('Mask', mask)
        mask = cv2.resize(mask, (1920, 1080))
        cv2.imwrite('maskPATS.jpg', mask)

        cv2.waitKey(10)
        break
    cv2.destroyAllWindows()


def pixel(p1, p2, p3, p4):
    img = cv2.imread("maskPATS.jpg")
    global check
    cv2.imwrite('final.jpg', img)
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    imgCrop1 = img[y1:y2, x1:x2]
    imgCrop2 = img[y3:y4, x3:x4]
    cv2.imshow('img', img)
    cv2.imshow('crop 1', imgCrop1)
    cv2.imshow('crop 2', imgCrop2)

    blackPix1 = np.sum(imgCrop1 == 0)
    blackPix2 = np.sum(imgCrop2 == 0)

    print('Number of black pixels magnet 1:', blackPix1)
    print('Number of black pixels magnet 2:', blackPix2)
    cv2.waitKey(10)
    cv2.destroyAllWindows()

    if 100 < blackPix1 < 4000 and 100 < blackPix2 < 4000:   # Pixel value of 1 magnet between 750 and 2500
        check = True
    else:
        check = False
