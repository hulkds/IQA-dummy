import utils
import cv2
import glob
import numpy as np
import yaml
import time

class ConfigFile(object):
    def __init__(self, file="config.yaml"):
        with open(file, "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)

        # configuration of image size
        self.image_size = config["size"]
        
        # configuration of brightness
        self.thresh_dark = config["brightness_params"]["thresh_dark"]
        self.thresh_bright = config["brightness_params"]["thresh_bright"]

        # configuration of uniform
        self.c_low_thresh = config["uniform_params"]["c_low_thresh"]
        self.c_high_thresh = config["uniform_params"]["c_high_thresh"]
        self.thresh_uniform = config["uniform_params"]["thresh"] 

        # configuration of blurring
        self.thresh_blur = config["blur_params"]["thresh"]

        # configuration of noise
        self.thresh_noise = config["noise_params"]["thresh"]   


if __name__ == "__main__":
    
    # get params from config file
    cfg = ConfigFile(file="config.yaml")

    # # loop over the folder that contain image
    # for im_f in glob.glob("image/*"):
    #     # read image
    #     image = cv2.imread(im_f)
        
    #     # convert to grayscale
    #     image_gray = utils.convert2Gray(image)

    #     image_gray = cv2.resize(image_gray, (cfg.image_size, cfg.image_size))

    #     # evaluate image quality
    #     quality = utils.checkImageQuality(image, cfg.thresh_dark, cfg.thresh_bright,
    #                                             cfg.c_low_thresh, cfg.c_high_thresh, cfg.thresh_uniform,
    #                                             cfg.thresh_blur,
    #                                             cfg.thresh_noise)
    #     # put text on image and show image
    #     cv2.putText(image, "{}".format(quality), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    #     cv2.imshow("NOISE: " + im_f, image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    video_path = "video/dark_bright.mp4"

    cap = cv2.VideoCapture(video_path)

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('video/dark_bright_qa.avi',cv2.VideoWriter_fourcc('M','J','P','G'), cap.get(cv2.CAP_PROP_FPS), (frame_width,frame_height))

    while(cap.isOpened()):
        # capture the video frame by frame
        ret, frame = cap.read()

        width_center = int(frame_width / 2)

        if ret==True:
            # convert to grayscale
            image_gray = utils.convert2Gray(frame)

            image_gray = cv2.resize(image_gray, (cfg.image_size, cfg.image_size))
            
            start_time = time.time()
            # evaluate image quality
            quality = utils.checkImageQuality(image_gray, cfg.thresh_dark, cfg.thresh_bright,
                                                    cfg.c_low_thresh, cfg.c_high_thresh, cfg.thresh_uniform,
                                                    cfg.thresh_blur,
                                                    cfg.thresh_noise)
            end_time = time.time()

            # put text on image and show image
            cv2.putText(frame, "FPS: {}".format(1/(end_time-start_time)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, "{}".format(quality), (width_center, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow('frame', frame)

            # Write the frame into the file 'output.avi'
            out.write(frame)

            if cv2.waitKey(25) & 0xFF==ord('q'):
                break
        
        else:
            break
    
    cap.release()

    cv2.destroyAllWindows()
