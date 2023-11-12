import cv2
import os
import numpy as np

start_path = os.path.dirname(os.path.abspath(__file__))
abs_path = r'C:\Python\PhotosWebSiteProject\static'


def border_img(img, type_border, color_border, user_id, filename):
    # img = cv2.resize(img, (518, 388))
    with_border = cv2.copyMakeBorder(img, 30, 30, 30, 30, type_border, value=color_border)

    path_dir = os.path.relpath(abs_path, start_path)

    file_name = os.path.join(abs_path, 'border--{}-{}.JPG'.format(filename, user_id))
    print(cv2.imwrite(file_name, with_border))
    print(file_name)

    my_file = os.path.basename(file_name)
    print(my_file)
    return my_file


def change_color_img(img, color, user_id, filename):
    # img = cv2.resize(img, (518, 388))
    image_gray = cv2.cvtColor(img, color)

    path_dir = os.path.relpath(abs_path, start_path)
    cv2.imshow("image_gray", image_gray)
    file_name = os.path.join(abs_path, 'color-{}-{}.JPG'.format(filename, user_id))
    print(cv2.imwrite(file_name, image_gray))

    print(file_name)
    my_file = os.path.basename(file_name)
    return my_file


def identify_object(img, user_id, filename):
    lower = np.array([50, 50, 30])
    upper = np.array([179, 179, 255])
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    path_dir = os.path.relpath(abs_path, start_path)

    file_name = os.path.join(abs_path, 'result-{}-{}.JPG'.format(filename, user_id))
    cv2.imwrite(file_name, result)
    my_file_result = os.path.basename(file_name)

    file_name = os.path.join(abs_path, 'mask-{}-{}.JPG'.format(filename, user_id))
    cv2.imwrite(file_name, mask)
    my_file_mask = os.path.basename(file_name)
    return my_file_mask, my_file_result
