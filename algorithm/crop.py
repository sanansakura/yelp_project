from PIL import Image
from PIL import ImageOps
import os
import numpy as np
import cv2


def crop_img(image_folder, image_name_lst, output_dir):
    '''
    Crop the given list of images. Each image is crop into three pieces.
    After cropping, save the images into output_dir.
    '''
    #go through each image in image_name_lst
    #image_array = np.zeros((len(image_name_lst), 299, 299, 3))
    labels = []
    for image_idx in range(len(image_name_lst)):
        image_name = image_name_lst[image_idx]
        if image_name[-4:] == ".jpg":
            image_dir = image_folder + image_name
            current_img = Image.open(image_dir)
            w, h = current_img.size
            #find the width of the maximum square window
            window_size = min(w, h)
            #initialize the collection of windows being cropped to be empty
            windows = []
            if w < h:
                window_top = (0, 0, window_size, window_size)
                window_center = (0, h//2 - window_size//2, window_size, h//2 + window_size//2)
                window_bottom = (0, h - window_size, w, h)
                windows.append(window_top)
                windows.append(window_center)
                windows.append(window_bottom)

            elif h < w:
                window_left = (0, 0, window_size, window_size)
                window_center = (w//2 - window_size//2, 0, w//2 + window_size//2, h)
                window_right = (w - window_size, 0, w, h)
                windows.append(window_left)
                windows.append(window_center)
                windows.append(window_right)
            else:
                window_center = (0, 0, w, h)
                windows.append(window_center)
            for window_index in range(len(windows)):
                temp = current_img.copy()
                temp = temp.crop(windows[window_index])
                w_temp, h_temp = temp.size
                if w_temp != h_temp:
                    delta = max(w_temp, h_temp) - min(w_temp, h_temp)
                    if w_temp < h_temp:
                        padding = (delta//2,0, delta-(delta//2), 0)
                    elif h_temp < w_temp:
                        padding = (0, delta//2, 0, delta-(delta//2))
                    temp = ImageOps.expand(temp, padding, fill = 1)

                temp = temp.resize((299, 299),  Image.ANTIALIAS)
                temp.save(output_dir + image_name[:-4] + "_" + str(window_index) + ".jpg")
                #labels.append(image_name[:-4] + "_" + str(window_index))
                #image_array[image_idx, :, :, :] = np.array(temp)
            #np.save("food_images.npy", image_array)
            #np.save("food_labels.npy", np.array(labels))
            print(" %d / %d" % (image_idx + 1, len(image_name_lst)))




if __name__ == "__main__":
    photo_dir = "C:/Users/sanan/Desktop/yelp_project/food/"
    output_dir = "C:/Users/sanan/Desktop/yelp_project/food_cropped/"
    files_lst = os.listdir(photo_dir)[:50000]
    crop_img(photo_dir, files_lst, output_dir)
