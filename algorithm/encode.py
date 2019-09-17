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

def main(image_path, images_label, files_label, encoded_file_name):
    '''
    Encode the images contained in the specific folder.
    '''
    model = MobileNetV2(weights='imagenet', include_top=False)
    data, files = encode(image_path, preprocess_input, model, input_size = 224, batch_size = 128)
    data = np.reshape(data, (len(files), data.shape[1]*data.shape[2]*data.shape[3]))
    with h5py.File(encoded_file_name, 'w') as hf:
        hf.create_dataset(images_label,  data=data)
        hf.create_dataset(files_label, data = np.chararray.encode(np.array(files), encoding='utf8'))
    K.clear_session()

if __name__ == "__main__":
	base_dir = os.getcwd()
	input_path = os.path.join(base_dir, "input_image/")
	images_label = "image_data_0"
    files_label = "files_list_0"
    encoded_file_name = "encoded.h5"
    main(input_path, "input_image", "input_file", "encoded_input.h5")
