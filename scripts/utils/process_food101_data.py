import os
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from PIL import Image
import json
import re
from sklearn.preprocessing import LabelBinarizer
from matplotlib import pyplot
from random import sample

def load_label(label_txt_path):
    '''
    Save the label mapping for food101 dataset into json files.
    '''
    labels_mapping = {}
    labels_inv_mapping = {}
    labels_food101_file = open(label_txt_path, "r")
    labels_food101_lines = labels_food101_file.readlines()
    current_id = 0
    for label in labels_food101_lines:
        current_label = label[:-1]
        labels_mapping[current_label] = current_id
        labels_inv_mapping[current_id] = current_label
        current_id +=1
    with open("food101_label_map.json", "w") as label_map_json:
        json.dump(labels_mapping, label_map_json)
    with open("food101_label_map_inv.json", "w") as label_map_inv_json:
        json.dump(labels_inv_mapping, label_map_inv_json)

def load_data_helper(data_dict, label_dict, image_path, target_size, filename):
    '''
    A helper function to convert images into numpy arrays.
    '''
    images = []
    labels = []
    for label in data_dict:
        label_id = label_dict[label]
        for image in data_dict[label]:
            current_image_path = os.path.join(image_path,image)

            current_image = Image.open(current_image_path + ".jpg")
            current_image = current_image.resize((target_size, target_size), Image.ANTIALIAS)
            current_image = img_to_array(current_image, dtype = "uint8")
            if current_image.shape != (target_size, target_size, 3):
                print("Error dimension found %s, %s" % (label, image))
                print(current_image.shape)
                continue
            print("processing %s, %s" % (label, image))
            images.append(current_image)
            labels.append(label_id)
    print("finished preprocessing" + filename)
    X, y = np.asarray(images), np.asarray(labels)
    np.savez_compressed(filename, X, y)


def load_train_test_data(train_data_json, test_data_json, label_json_path, image_path, target_size):
    '''
    Load the training data and the testing data according to the json files provided.
    Save the datasets into numpy arrays respectively.
    '''
    with open(label_json_path) as label_map_json:
        label_map = json.load(label_map_json)
    with open(train_data_json) as train_data_file:
        train_data_dict = json.load(train_data_file)
    with open(test_data_json) as test_data_file:
        test_data_dict = json.load(test_data_file)
    #load the training dataset
    load_data_helper(train_data_dict, label_map, image_path, target_size, "train_food101.npz")
    #load the testing dataset
    load_data_helper(test_data_dict, label_map, image_path, target_size, "test_food101.npz")

def show_random_image(dataset_path, label_path):
    '''
    Random display 9 images and their labels in the given dataset.
    '''
    with open(label_path) as label_map_json:
        label_map = json.load(label_map_json)
    data = np.load(dataset_path)
    X,y = data["arr_0"], data["arr_1"]
    idx = sample(range(0, X.shape[0]), 9)
    square = 3
    ix = 1
    for _ in range(square):
        for _ in range(square):
            # specify subplot and turn of axis
            ax = pyplot.subplot(square, square, ix)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel(label_map[str(y[idx[ix-1]])])
            # plot filter channel in grayscale
            pyplot.imshow(X[idx[ix-1], :, :, :])
            ix += 1
    # show the figure
    pyplot.show()
def group_label(index_to_label_path, label_to_content_path):
    '''
    Manually group labels together to reduce the number of classes.
    Save the mappings between labels and class numbers into json files.
    '''
    salad = ["beet_salad", 'caesar_salad', 'caprese_salad', "greek_salad"]
    sandwich_hamburger = ["hot_dog", "hamburger", "club_sandwich", "lobster_roll_sandwich",
                            "pulled_pork_sandwich", "grilled_cheese_sandwich"]
    dessert = ["churros", "beignets", "cheesecake", "carrot_cake", "red_velvet_cake", "strawberry_shortcake", "chocolate_cake", "chocolate_mousse",
                        "tiramisu","bread_pudding", "cup_cakes", "donuts", "creme_brulee","waffles", "apple_pie",
                        "panna_cotta", "macarons", "baklava", "cannoli", "pancakes"]
    ice_cream = ["ice_cream", "frozen_yogurt"]
    japanese = ["edamame", "miso_soup", "sashimi", "ramen", "seaweed_salad", "sushi", "takoyaki" ,"gyoza", "dumplings"]
    seafood = ["oysters", "scallops", "mussels", "ceviche", "tuna_tartare", "shrimp_and_grits", "crab_cakes", "paella"]
    bread = ["french_toast", "garlic_bread"]
    middle_east = ["chicken_curry", "falafel", "hummus"]
    brunch = ["chicken_quesadilla", "breakfast_burrito", "omelette", "huevos_rancheros", "deviled_eggs", "croque_madame", "eggs_benedict"]
    mexican = ["tacos", "nachos", "guacamole"]
    fast_food = ["french_fries", "onion_rings", "poutine", "pizza", "fish_and_chips", "chicken_wings", "fried_calamari"]
    soup = ["clam_chowder", "lobster_bisque"]
    steak = ["pork_chop", "prime_rib", "steak", "foie_gras", "baby_back_ribs", "grilled_salmon", "filet_mignon"]
    italian_french = ["bruschetta", "beef_tartare", "beef_carpaccio", "cheese_plate", "french_onion_soup", "escargots", "spaghetti_bolognese", "spaghetti_carbonara", "lasagna", "macaroni_and_cheese", "ravioli", "risotto", "gnocchi"]
    asia = ["bibimbap", "fried_rice", "spring_rolls",  'peking_duck', "pho", "pad_thai", "samosa", "hot_and_sour_soup"]

    label_to_content = {}
    label_to_content["salad"] = salad
    label_to_content["sandwich_hamburger"] = sandwich_hamburger
    label_to_content["dessert"] = dessert
    label_to_content["ice_cream"] = ice_cream
    label_to_content["japanese"] = japanese
    label_to_content["seafood"] = seafood
    label_to_content["bread"] = bread
    label_to_content["middle_east"] = middle_east
    label_to_content["brunch"] = brunch
    label_to_content["mexican"] = mexican
    label_to_content["fast_food"] = fast_food
    label_to_content["soup"] = soup
    label_to_content["steak"] = steak
    label_to_content["italian_french"] = italian_french
    label_to_content["asia"] = asia
    keys = list(label_to_content.keys())
    index_to_label = {}
    for i in range(len(keys)):
        index_to_label[str(i)] = keys[i]
    with open(index_to_label_path, "w") as index_to_label_json:
        json.dump(index_to_label, index_to_label_json)
    with open(label_to_content_path, "w") as label_to_content_json:
        json.dump(label_to_content, label_to_content_json)

def group_food101_label(food101_data_path, index_to_label_path, label_to_content_path, food101_label_map):
    '''
    Create new training labels based on the groupped label mapping.
    '''
    with open(index_to_label_path) as index_to_label_json:
        index_to_label = json.load(index_to_label_json)
    with open(label_to_content_path) as label_to_content_json:
        label_to_content = json.load(label_to_content_json)
    with open(food101_label_map) as label_map_file:
        label_map = json.load(label_map_file)
    data = np.load(food101_data_path)
    X, y = data["arr_0"], data["arr_1"]
    old_idx_to_new_idx = {}
    for index in list(index_to_label.keys()):
        new_idx = int(index)
        new_label = index_to_label[index]
        old_labels = label_to_content[new_label]
        for old_label in old_labels:
            old_idx = label_map[old_label]
            old_idx_to_new_idx[old_idx] = new_idx
    for i in range(y.shape[0]):
        y[i] = old_idx_to_new_idx[y[i]]
    np.savez_compressed("groupped_"+food101_data_path, X, y)



if __name__ == "__main__":
    base_dir = os.getcwd()
    label_food101_file = "data/food-101/meta/classes.txt"
    image_dir = "data/food-101/images"
    label_dir_food101 = os.path.join(base_dir, label_food101_file)
    image_dir = os.path.join(base_dir, image_dir)
    load_label(label_dir_food101)
    train_json_path = os.path.join(base_dir, "data/food-101/meta/train.json")
    test_json_path = os.path.join(base_dir, "data/food-101/meta/test.json")
    label_json_path = os.path.join(base_dir, "food101_label_map.json")
    load_train_test_data(train_json_path, test_json_path, label_json_path, image_dir, 64)
    show_random_image("groupped_train_food101.npz", "food101_index_label_map.json")
    group_label("food101_index_label_map.json", "food101_label_content.json")
    group_food101_label("test_food101.npz", "food101_index_label_map.json", "food101_label_content.json", "food101_label_map.json")
