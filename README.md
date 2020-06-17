# yelp-project

## Introduction
Given an input food image, the goal of the web app is to give the users a list of restaurants that provide the same kind of cuisine.
## Datasets
The restaurant data used by this project is from [Yelp Open Dataset](https://www.yelp.com/dataset) ([Documentation](https://www.yelp.com/dataset/documentation/main)) and [Food101 Dataset](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/).

Files used from the yelp open dataset include:\
Yelp Dataset JSON: photo.json, and business.json\
Yelp Dataset Photos

I used yelp dataset to find the restaurant information and generate the restaurant recommendations. The food101 dataset is used to train the model.


## Yelp Data Preprocessing

1. Reorganize the yelp photos into different folders according to their labels (food, drink, menu, outside, inside). In this project, only the food images from the yelp dataset are used. Then, randomly choose a subset of 500,000 images. [reorganize_images.py](src/utils/reorganize_images.py)

2. Resize the images and save them into a numpy array. [load_yelp_data](src/utils/process_yelp_data.py)

3. Create a subset of business.json containing only the restaurants mapped to the food images selected in step 1; \
extract only the useful information (name, address, city, state, stars, categories) for each restaurant; \
create a mapping between the photo ids and their related restaurant information, save it into photo_business.json. [create_image_business_mapping](src/utils/process_yelp_data.py)

## Methodology

#### Goal
Assign cuisine types as labels to the yelp food images.

#### Dataset
For the dataset, I used food101 dataset and manually groupped the food labels into different cuisines. Then each food image is associated with a food label and an additional cuisine label.

An example is: \
salad = ["beet_salad", 'caesar_salad', 'caprese_salad', "greek_salad"]


#### Food101 Dataset Preprocessing
1. Read the food labels from text files and save the mapping between class labels and text food labels into json files (food101_label_map.json and food101_label_map_inv.json). [load_label](src/utils/process_food101_data.py)

2. Load the training and test data into numpy arrays. Then assign text food labels to the images. [load_train_test_data](src/utils/process_food101_data.py)

3. Group the food labels into 15 different cuisines. [group_food_label](src/utils/process_food101_data.py)

4. Assign cuisine labels to the images. [assign_cuisine_label_to_image](src/utils/process_food101_data.py)

5. (optional) Show random images and their labels. [show_random_image](src/utils/process_food101_data.py)

#### Model

For the model part, I did transfer learning on the pretrained model MobileNetV2 using keras. The code could be found here [model](src/utils/model.py).
The evaluation metrics being used is top-5 accuracy.
More model experiment is in the notebook [cnn_models](src/utils/cnn_model.ipynb).

#### Assign Cuisine labels to yelp food photos

Make classifications on the yelp food images [predict_on_image](src/utils/process_yelp_data.py); get the top 5 classes for each image [top_n_prediction](src/utils/process_yelp_data.py); translate the class labels back to the cuisine names [assign_label_to_image](src/utils/process_yelp_data.py).

#### Make recommendations

1. Make prediction on the user input image.

2. Compare the cuisine labels of the input image and the cuisine labels of the yelp food images. Find the top 10 food images of the highest similarities. Recommend the users with the restaurants of these yelp food images [algorithm_test.py](src/utils/algorithm_test.py). 
