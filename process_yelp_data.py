import numpy as np
import h5py
import json
import os
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from PIL import Image
import json
from keras.models import load_model

def replace_empty(info):
    '''
    Fill in the missing information if not provided.
    '''
    if info =="":
        return "Not provided."
    else:
        return info

def subset_files(photo_json_path, business_json_path, output_path):
    '''
    Subset the original Json files according to the selected images.
    '''
    #Create a dictionary whose keys are photo_ids, values are business_ids
    photo_dict = {}
    photo_dict_invert = {}
    photo_business_dict = {}
    #load images ids
    data = np.load(output_path + "yelp_image_subset.npz")
    _, image_ids = data["arr_0"], data["arr_1"]
    with open(photo_json_path) as photo_json:
        for line in photo_json:
            photo_info = json.loads(line)
            photo_id = photo_info["photo_id"]
            if photo_id in image_ids:
                #print(True)
                photo_dict[photo_info["photo_id"]] = photo_info["business_id"]
                if photo_info["business_id"] in photo_dict_invert:
                    photo_dict_invert[photo_info["business_id"]].append(photo_info["photo_id"])
                else:
                    photo_dict_invert[photo_info["business_id"]] = [photo_info["photo_id"]]
    #Create a mapping between photo_ids and their business information
    with open(business_json_path, encoding="utf8") as business_json:
        for line in business_json:
            business_info = json.loads(line)
            if business_info["business_id"] in photo_dict_invert:
                for photo_id in photo_dict_invert[business_info["business_id"]]:
                    photo_business_dict[photo_id] = business_info
    #Make the information into a nicer format.
    data = {}
    for photo_id in photo_business_dict:
        print(photo_id + " is being processed.")
        data[photo_id] = {}
        data[photo_id]["business_id"] = replace_empty(photo_business_dict[photo_id]["business_id"])
        data[photo_id]["info"] = {}
        data[photo_id]["info"]["name"] = replace_empty(photo_business_dict[photo_id]["name"])
        data[photo_id]["info"]["address"] = replace_empty(photo_business_dict[photo_id]["address"])
        data[photo_id]["info"]["city"] = replace_empty(photo_business_dict[photo_id]["city"])
        data[photo_id]["info"]["state"] = replace_empty(photo_business_dict[photo_id]["state"])
        data[photo_id]["info"]["stars"] = replace_empty(photo_business_dict[photo_id]["stars"])
        data[photo_id]["info"]["categories"] = replace_empty(photo_business_dict[photo_id]["categories"])
    #Save the mapping between photo ids and business information
    with open(output_path + "photo_business.json", "w") as photo_business_json:
        json.dump(data, photo_business_json)

def load_yelp_data(yelp_image_dir, output_path, target_size):
    '''
    Load the yelp images, resize them into the target size and save the images into
    numpy arrays.
    '''
    images = []
    image_ids = []
    for filename in os.listdir(yelp_image_dir):
        if filename.endswith(".jpg"):
            image_id = filename[:-4]
            current_image_path = os.path.join(yelp_image_dir, filename)
            current_image = Image.open(current_image_path)
            current_image = current_image.resize((target_size, target_size), Image.ANTIALIAS)
            current_image = img_to_array(current_image, dtype = "uint8")
            if current_image.shape != (target_size, target_size, 3):
                print("Error dimension found %s, %s" % (label, image))
                print(current_image.shape)
                continue
            print("processing %s" % (image_id))
            images.append(current_image)
            image_ids.append(image_id)
    images = np.asarray(images)
    np.savez_compressed(output_path + "yelp_image_subset.npz", images, image_ids)

def predict_on_image(yelp_image_array_path, model_path, output_path):
    '''
    Return a dict, whose ids are image ids, values are lists of labels.
    '''
    data = np.load(yelp_image_array_path)
    images, _ = data["arr_0"], data["arr_1"]
    model = load_model(model_path)
    output = model.predict(images)
    np.savez_compressed(output_path, output)

def top_n_prediction(path_to_prediction, k=5):
    '''
    Return the top k predictions.
    '''
    predictions = np.load(path_to_prediction)["arr_0"]
    top_k = np.argsort(predictions, axis=-1)[:,-k:]
    return top_k

def assign_label_to_image(path_to_top_k_prediction, path_to_images, path_to_label_mapping, output_path):
    '''
    Assign labels to images and create a mapping, which is a dictionary whose keys
    are photo ids, each photo id is associated with a list of labels.
    Save it into a json file.
    '''
    image_data = np.load(path_to_images)
    images, image_ids = image_data["arr_0"], image_data["arr_1"]
    top_k_prediction = np.load(path_to_top_k_prediction)["arr_0"]
    with open(path_to_label_mapping, "r") as label_map_file:
        label_mapping = json.load(label_map_file)
    print(top_k_prediction.shape, label_mapping)
    image_to_label = {}
    for i in range(len(image_ids)):
        images_id = image_ids[i]
        image_to_label[images_id] = []
        for label in top_k_prediction[i, :]:
            image_to_label[images_id].append(label_mapping[str(label)])
    with open(output_path + "image_id_to_label.json", "w") as output:
        json.dump(image_to_label, output)
if __name__ == "__main__":
    base_dir = os.getcwd()
    image_json_path = os.path.join(base_dir, 'yelp_dataset/yelp_dataset/photo.json')
    restaurant_json_path = os.path.join(base_dir, "yelp_dataset/yelp_dataset/business.json")
    yelp_image_dir = os.path.join(base_dir, "food_subset/subset/")
    output_path = os.path.join(base_dir, "algorithm_cnn/")
    #load_yelp_data(yelp_image_dir, output_path, 64)
    #predict_on_image(output_path + "yelp_image_subset.npz", output_path + "model.h5", output_path + "prediction.npz")
    #subset_files(image_json_path, restaurant_json_path, output_path)
    #topk = top_n_prediction(output_path + "prediction.npz")
    #np.savez_compressed(output_path + "top_5_predictions.npz", topk)
    assign_label_to_image(output_path+"top_5_predictions.npz", output_path + "yelp_image_subset.npz", output_path + "food101_index_label_map.json", output_path)
