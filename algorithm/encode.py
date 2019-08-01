import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from keras import backend as K
import os
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics.pairwise import euclidean_distances
import h5py
def encode(image_path, preprocess_function, model, input_size, batch_size):
    '''
    Encode the data in the given directory. Return an array of encoded data.
    '''
    #initialize the data data generator
    datagen = ImageDataGenerator(
                shear_range = 0.2, \
                zoom_range = 0.2, \
                preprocessing_function = preprocess_function,\
                horizontal_flip = True)
    data_generator = datagen.flow_from_directory(image_path,\
                target_size = (input_size, input_size),\
                batch_size = batch_size,\
                shuffle = False,\
                color_mode="rgb",\
                class_mode = None
                )
    data_generator.reset()
    n_images = len(data_generator.filenames)
    features = model.predict_generator(data_generator, \
                steps = np.ceil(n_images/batch_size)
                )
    return features, data_generator.filenames

def similarity(source_image, input_image, source_files):
    '''
    Find the most similar image.
    '''
    idx = np.argmax(euclidean_distances(source_image, input_image))
    return source_files[idx]

def main():
    '''
    Encode the images contained in the specific folder.
    '''
    model = MobileNetV2(weights='imagenet', include_top=False)
    path = "C:/Users/sanan/Desktop/yelp_project/food_subset/"
    input_path = "C:/Users/sanan/Desktop/yelp_project/input_image/"
    data, files = encode(path, preprocess_input, model, input_size = 224, batch_size = 128)
    data_input, files_input = encode(input_path, preprocess_input, model, input_size = 224, batch_size = 1)
    #print(files)
    data, data_input = np.reshape(data, (len(files), data.shape[1]*data.shape[2]*data.shape[3])), \
                np.reshape(data_input, (len(files_input), data_input.shape[1]*data_input.shape[2]*data_input.shape[3]))
    print(data.shape, data_input.shape)
    print(similarity(data, data_input, files))
    print(files)
    with h5py.File('encoded.h5', 'w') as hf:
        hf.create_dataset("image_data_0",  data=data)
        hf.create_dataset("files_list_0", data = np.chararray.encode(np.array(files), encoding='utf8'))
        #hf.create_dataset("files_list_0",  data=np.array(files))
    K.clear_session()

if __name__ == "__main__":
    main()
