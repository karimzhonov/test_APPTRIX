import os
import cv2
import numpy as np

from django.conf import settings


def impose_ico_to_image(avatar):
    image = cv2.imdecode(np.frombuffer(avatar.read(), np.uint8), -1)
    image_height, image_wight, _ = image.shape
    path_to_ico = os.path.join(settings.STATIC_ROOT, 'favicon.jpeg')
    ico = cv2.imread(path_to_ico)
    ico_height, ico_width, _ = ico.shape
    # refactoring ico
    new_ico_width = image_wight // 10
    new_ico_height = int(ico_height * (new_ico_width / ico_width))
    new_ico = cv2.resize(ico, (new_ico_width, new_ico_height))
    # Impose ico to image
    top = image_height // 20
    left = image_wight // 20
    image[top:top + new_ico_height, left:left + new_ico_width] = new_ico

    return image
