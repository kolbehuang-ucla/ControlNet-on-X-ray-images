import cv2
import os
import numpy as np
from PIL import Image
from annotator.util import resize_image, HWC3

# Canny detector from cv2
class CannyDetector:
    def __call__(self, img, low_threshold, high_threshold):
        return cv2.Canny(img, low_threshold, high_threshold)
    
model_canny = None

# Generate canny edges with parameters:
# img: Image file
# res: Resolution of the final image
# l: low threshold
# h: high threshold
def canny(img, res, l, h):
    img = resize_image(HWC3(img), res)
    global model_canny
    if model_canny is None:
        from annotator.canny import CannyDetector
        model_canny = CannyDetector()
    result = model_canny(img, l, h)
    return result

# Set the directory
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xray/Test/ablative'))

# Set target(original images) and destination paths
# Dest paths are organized as source-lowthreshold-highthreshold
targetPath = os.path.abspath(os.path.join(directory, 'target'))
destPath25 = os.path.abspath(os.path.join(directory, 'source-25-50'))
destPath50 = os.path.abspath(os.path.join(directory, 'source-50-100'))
destPath100 = os.path.abspath(os.path.join(directory, 'source-100-150'))

# Loop through the target path and make canny edges of the images and put it in corresponding directories
for filename in os.listdir(targetPath):
    f = os.path.join(targetPath, filename)
    d25 = os.path.join(destPath25, filename)
    d50 = os.path.join(destPath50, filename)
    d100 = os.path.join(destPath100, filename)
    # checking if it is a file
    if os.path.isfile(f):
        image = Image.open(f)
        arrayImage = np.asarray(image)
        edge25 = canny(arrayImage, 1024, 25, 50)
        edge50 = canny(arrayImage, 1024, 50, 100)
        edge100 = canny(arrayImage, 1024, 100, 150)
        Image.fromarray(edge25).save(d25)
        Image.fromarray(edge50).save(d50)
        Image.fromarray(edge100).save(d100)


