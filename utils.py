import cv2
import numpy as np
import math

def convert2Gray(image):
    """Function that verify the image dimension and convert image to grayscale if needed. 

    Args:
        image (image): image to verify.

    Raises:
        ValueError: Dimension of image must be 2 or 3.

    Returns:
        ndarray: grayscale image.
    """    
    if len(image.shape)==3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape)==2:
        return image
    else:
        raise ValueError('Dimension of image must be 2 or 3.')


def isBright(image, thresh_dark=0.3, thresh_bright=0.8):
    """Function that read an image and compute the brightness score of the image.
    If brightness score is less than thresh_dark, the the image is considered too dark.
    If brightness score is more than thresh_bright, the image is considered too bright.

    Args:
        image (ndarray): image to evaluate.
        thresh_dark (float, optional): darkness threshold. Defaults to 0.3.
        thresh_bright (float, optional): brightness threshold. Defaults to 0.8.

    Returns:
        bool: True if image is too dark.
        bool: True if image is too bright.
    """    
    # Convert image to grayscale
    image = convert2Gray(image)
    
    # Normalize image by dividing all pixel values with maximum pixel value
    L = image/np.max(image)
    
    # Return True if mean is greater than thresh else False
    return np.mean(L) < thresh_dark, np.mean(L) > thresh_bright


def isUniform(image, c_low_thresh=100, c_high_thresh=200, thresh=0.5):
    """Function that read an image and compute the uniform score of image.
    If image only has a single color, it must has a high uniform score.

    Args:
        image (ndarray): image to evaluate.
        c_low_thresh (int, optional): 	first threshold for the hysteresis procedure used in Canny filter. Defaults to 100.
        c_high_thresh (int, optional): 	second threshold for the hysteresis procedure used in Canny filter. Defaults to 200.
        thresh (float, optional): uniform threshold. Defaults to 0.5.

    Returns:
        bool: True if image is too uniform.
    """    
    # convert image to grayscale
    image = convert2Gray(image)
    
    # get the image area
    image_area = image.shape[0]*image.shape[1]
    
    # do edge detection
    edges = cv2.Canny(image, c_low_thresh, c_high_thresh)
    
    # get percentage of edge over image area
    edge_percent = float(np.sum(edges/255)) / image_area

    return edge_percent < thresh


def isBlur(image, thresh=200):
    """Function that read an image as input and compute the blurring score.

    Args:
        image (ndarray): image to evaluate.
        thresh (int, optional): blurring threshold. Defaults to 200.

    Returns:
        bool: True if image is too blur (blurring score is greater than blurring threshold).
    """    
    # convert image to grayscale
    image = convert2Gray(image)

    # apply Laplacian filter to estimate blurring score
    fm = cv2.Laplacian(image, cv2.CV_64F).var()
    
    return fm > thresh

def isNoise(image, thresh=5):
    """Function that read image and compute the noise variance.

    Args:
        image (ndarray): image to evaluate.
        thresh (int, optional): noise variance threshold. Defauts to

    Returns:
        bool: True if noise variance of image is greater than noise threshold.
    """
    # convert image to grayscale
    image = convert2Gray(image)

    # get the height and width of image
    H, W = image.shape

    # define noise estimation operator
    M = np.array([[1, -2, 1],
        [-2, 4, -2],
        [1, -2, 1]])

    # compute the variance of noise in the given image
    sigma = np.sum(np.sum(np.absolute(cv2.filter2D(src=image, ddepth=-1, kernel=M))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))

    return sigma > thresh


def checkImageQuality(image, thresh_dark=0.3, thresh_bright=0.8, c_low_thresh=500, c_high_thresh=1000, thresh_uniform=0.5, thresh_blur=200, thresh_noise=70):
    """Function that take input image and return if image is good or poor quality.

    Args:
        image (ndarray): image to evaluate.
        thresh_dark (float, optional): darkness threshold. Defaults to 0.3.
        thresh_bright (float, optional): brightness threshold. Defaults to 0.8.
        c_low_thresh (int, optional): first threshold for the hysteresis procedure used in Canny filter. Defaults to 500.
        c_high_thresh (int, optional): second threshold for the hysteresis procedure used in Canny filter. Defaults to 1000.
        thresh_uniform (float, optional): uniform threshold. Defaults to 0.5.
        thresh_blur (int, optional): blurring threshold. Defaults to 200.
        thresh_noise (int, optional): noise threshold. Defaults to 70.

    Returns:
        string: type of degradation if poor quality or "good quality".
    """
    # is image too dark or too bright
    is_dark, is_bright = isBright(image, thresh_dark, thresh_bright)

    # is image too uniform
    is_uniform = isUniform(image, c_low_thresh, c_high_thresh, thresh_uniform)

    # is image too blur
    is_blur = isBlur(image, thresh_blur)

    # is image too noise
    is_noise = isNoise(image, thresh_noise) 

    # if there are one of these degradation type, so image is poor quality
    if is_dark:
        return "too dark"
    elif is_bright:
        return "too bright"
    elif is_uniform:
        return "too uniform"
    elif is_blur:
        return "too blur"
    elif is_noise:
        return "too noise"
    else:
        return "good quality"