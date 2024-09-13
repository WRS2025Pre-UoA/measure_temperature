import cv2
import numpy as np


def calc_average_temperature(img, threshold=150):
    ave = np.average(img[img >= threshold])
    return np.where(img < threshold, 0, img), ave


def main():
    from matplotlib import pyplot as plt
    img = cv2.imread("../test_image/test_image1.jpg", cv2.IMREAD_GRAYSCALE)
    new_img, ave = calc_average_temperature(img,180)
    print(ave)
    plt.imshow(new_img)
    plt.show()


if __name__ == "__main__":
    main()
