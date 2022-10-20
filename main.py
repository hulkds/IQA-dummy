import utils
import cv2
import glob
import numpy as np
import yaml
import time
import argparse
import tqdm
import os

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', action='store_true', help='process images')
    parser.add_argument('--videos', action='store_true', help='process videos')
    parser.add_argument('--show', action='store_true', help='show result using opencv')
    args = parser.parse_args()

    # get params from config file
    cfg = ConfigFile(file="config.yaml")

    if args.images:
        # get images file name in the images folder
        images_fn = glob.glob('images/*.jpg') + glob.glob('images/*.png') + glob.glob('images/*.jpeg')
        
        # loop over the folder that contain image
        for im_f in tqdm.tqdm(images_fn):
            # read image
            image = cv2.imread(im_f)
            
            # convert to grayscale
            image_gray = utils.convert2Gray(image)

            # resize image
            image_gray = cv2.resize(image_gray, (cfg.image_size, cfg.image_size))

            # evaluate image quality
            quality = utils.checkImageQuality(image, cfg.thresh_dark, cfg.thresh_bright,
                                                    cfg.c_low_thresh, cfg.c_high_thresh, cfg.thresh_uniform,
                                                    cfg.thresh_blur,
                                                    cfg.thresh_noise)
        
            # put text on image 
            cv2.putText(image, "{}".format(quality), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # save image
            name, ext = os.path.splitext(im_f)
            im_f_save = name + '_iqa' + ext
            cv2.imwrite(im_f_save, image)

            # show image
            if args.show:
                cv2.imshow(im_f, image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    if args.videos:
        # get images file name in the images folder
        videos_fn = glob.glob('videos/*.mp4') + glob.glob('videos/*.avi')
        
        # loop over the folder that contain image
        for vid_f in tqdm.tqdm(videos_fn):
            cap = cv2.VideoCapture(vid_f)

            # Check if camera opened successfully
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")

            # Default resolutions of the frame are obtained.The default resolutions are system dependent.
            # We convert the resolutions from float to integer.
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
            name, ext = os.path.splitext(vid_f)
            vid_f_save = name + '_iqa' + ext
            out = cv2.VideoWriter(vid_f_save,cv2.VideoWriter_fourcc('M','J','P','G'), cap.get(cv2.CAP_PROP_FPS), (frame_width,frame_height))

            while(cap.isOpened()):
                # capture the video frame by frame
                ret, frame = cap.read()

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

                    # put text on image and save 
                    cv2.putText(frame, "FPS: {}".format(1/(end_time-start_time)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, "{}".format(quality), (int(frame_width / 2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                    # Write the frame into the file 'output.avi'
                    out.write(frame)

                    # show frame
                    if args.show:
                        cv2.imshow('frame', frame)

                    if cv2.waitKey(25) & 0xFF==ord('q'):
                        break
                
                else:
                    break
            
            cap.release()

            cv2.destroyAllWindows()
