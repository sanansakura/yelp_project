import numpy as np
import os
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.neighbors import KNeighborsClassifier
import h5py

def most_similar(encoded_image_array, encoded_files_array, input_image_array, k):
    '''
    Find the k most similar image in the training set using Euclidean distance.
    '''

    distances = euclidean_distances(encoded_image_array, input_image_array)
    idx_lst = np.argpartition(distances, k, axis=0)[:k]
    similar_images = [encoded_files_array[idx[0]] for idx in idx_lst]
    return similar_images

def main(encoded_file_location, encoded_input_location, k):
    '''
    Main function that finds the k most similar image in the training set.
    '''
    f_source = h5py.File(encoded_file_location, "r")
    f_input = h5py.File(encoded_input_location, "r")
    source_images = list(f_source["image_data_0"])
    source_files = list(f_source["files_list_0"])
    input_image = list(f_input["input_image"])
    image_lst = most_similar(source_images, source_files, input_image, k)
    image_ids = [image.decode()[7:] for image in image_lst]
    return image_ids

if __name__ == "__main__":
    base_dir = os.getcwd()
    encoded_image_path = os.path.join(base_dir, "encoded.h5")
    encoded_input_image = os.path.join(base_dir, "encoded_input.h5")
    ids = main(encoded_image_path, encoded_input_image, k)
