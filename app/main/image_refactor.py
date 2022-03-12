import io
import os
import numpy as np
from PIL import Image

from django.conf import settings


# def impose_ico_to_image(avatar):
#     import cv2
#     image = cv2.imdecode(np.frombuffer(avatar.read(), np.uint8), -1)
#     image_height, image_wight, _ = image.shape
#     path_to_ico = os.path.join(settings.STATIC_ROOT, 'favicon.jpeg')
#     ico = cv2.imread(path_to_ico)
#     ico_height, ico_width, _ = ico.shape
#     # refactoring ico
#     new_ico_width = image_wight // 10
#     new_ico_height = int(ico_height * (new_ico_width / ico_width))
#     new_ico = cv2.resize(ico, (new_ico_width, new_ico_height))
#     # Impose ico to image
#     top = image_height // 20
#     left = image_wight // 20
#     image[top:top + new_ico_height, left:left + new_ico_width] = new_ico
#
#     return image

def impose_ico_to_image(avatar):
    # Avatar
    image = Image.open(io.BytesIO(avatar.read()))
    image_height, image_wight = image.size
    # Ico
    path_to_ico = os.path.join(settings.STATIC_ROOT, 'favicon.jpeg')
    ico = Image.open(path_to_ico)
    ico_height, ico_width = ico.size
    # refactoring ico
    new_ico_width = image_wight // 10
    new_ico_height = int(ico_height * (new_ico_width / ico_width))
    ico = ico.resize((new_ico_height, new_ico_width))
    # Impose ico to image
    top = image_height // 20
    left = image_wight // 20
    image_np = np.array(image)
    ico_np = np.array(ico)
    image_np[top:top + new_ico_height, left:left + new_ico_width] = ico_np

    image_name = avatar.name
    _format = image_name.split('.')[-1]
    buf = io.BytesIO()
    new_image = Image.fromarray(image_np)
    new_image.save(buf, format='JPEG')
    return buf.getvalue()
