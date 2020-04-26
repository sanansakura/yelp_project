from keras import preprocessing
import tensorflow.compat.v1 as tf
import keras
import os
import numpy as np
import json

def find_highest_score_rest(input_image_path, model_path, image_id_to_label_json, photo_business_json, label_mapping):
    '''
    Return a list of restaurant dicts that have the highest matching scores
    '''
    #load the label mapping
    with open(label_mapping, "r") as label_mapping_file:
        numberical_to_text_label_mapping = json.load(label_mapping_file)

    tf.disable_v2_behavior() 
    #load the model
    model = tf.keras.models.load_model(model_path)

    #load and resize the input image
    img = preprocessing.image.load_img(input_image_path, target_size=(64, 64))

    #append an additional dimention to the input image
    input_image = np.expand_dims(np.array(img), axis=0)

    #make prediction
    prediction = model.predict(input_image)[0]

    #get the top 5 labels
    top_5_prediction = (-prediction).argsort()[:5]

    #translate the numberical labels into text labels based on the mapping between them
    top_5_prediction_text = [numberical_to_text_label_mapping[label] for label in top_5_prediction]

    #compare the labels of the input image and the labels of the yelp photos
    #load the mapping between image ids and their labels 
    with open(image_id_to_label_json, "r") as image_id_to_label_json_file:
        image_id_label_map = json.load(image_id_to_label_json_file)
    #load the mapping between image ids and their corresponding business (restaurant) information
    with open(photo_business_json, "r") as photo_business_json_file:
        photo_business_map = json.load(photo_business_json_file)

    #loop through the images and assign a score (the number of the current image and the input image have in common) 
    #to each image (where the score represents the similarity)
    images_ratings = {}
    for i in range(6):
        images_ratings[i] = []
    for image in image_id_label_map:
        count = len(list(set(top_5_prediction_text) & set(image_id_label_map[image])))
        images_ratings[count].append(image)

    #find the restaurants with the highest rating
    max_score_restaurant = []
    for max_count in reversed(range(6)):
        photos = images_ratings[max_count]
        if len(photos) != 0:
            for photo_id in photos:
                max_score_restaurant.append(photo_business_map[photo_id])
            #return only 10 restaurants
            if len(max_score_restaurant) < 10:
                return max_score_restaurant
            return max_score_restaurant[:10]


if __name__=="__main__":
	current_dir = os.getcwd()
	input_image = os.path.join(current_dir, "test.jpg")
	model_path = os.path.join(current_dir, "../../web_app/src/model.h5")
	label_path = os.path.join(current_dir, "../preprocessed_data/image_id_to_label.json")
	business_info = os.path.join(current_dir, "../preprocessed_data/photo_business.json")
    label_mapping = os.path.join(current_dir, "../preprocessed_data/food101_label_map_inv.json")
	find_highest_score_rest(input_image, model_path, label_path, business_info, label_mapping)
