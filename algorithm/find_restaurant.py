import numpy as np
import h5py
import json

def subset_files(photo_json_path, business_json_path, restaurant_list_path):
    '''
    Subset the original Json files according to the images.
    '''
    #Extract the list of restaurants
    f = h5py.File(restaurant_list_path, "r")
    restaurant_list = list(f["files_list_0"])
    print(restaurant_list[0].decode())
    #Create a dictionary whose keys are photo_ids, values are business_ids
    photo_dict = {}
    photo_dict_invert = {}
    photo_business_dict = {}
    with open(photo_json_path) as photo_json:
        for line in photo_json:
            photo_info = json.loads(line)
            photo_string = "subset\\"+photo_info["photo_id"]+".jpg"
            if photo_string.encode() in restaurant_list:
                #print(True)
                photo_dict[photo_info["photo_id"]] = photo_info["business_id"]
                if photo_info["business_id"] in photo_dict_invert:
                    photo_dict_invert[photo_info["business_id"]].append(photo_info["photo_id"])
                else:
                    photo_dict_invert[photo_info["business_id"]] = [photo_info["photo_id"]]

    with open(business_json_path, encoding="utf8") as business_json:
        for line in business_json:
            business_info = json.loads(line)
            if business_info["business_id"] in photo_dict_invert:
                for photo_id in photo_dict_invert[business_info["business_id"]]:
                    photo_business_dict[photo_id] = business_info
    with open("photo_business.json", "w") as photo_business_json:
        json.dump(photo_business_dict, photo_business_json)

def fetch_restaurant(image_id_lst, photo_business_json_path):
    '''
    Return a dict of associated restaurants according to the most similar images.
    '''
    restaurants_dict = {}
    with open(photo_business_json_path) as photo_business_json:
        photo_business_dict = json.load(photo_business_json)
        for image_id in image_id_lst:
            restaurant = photo_business_dict[image_id]
            if restaurant["business_id"] not in restaurants_dict:
                restaurants_dict[restaurant["business_id"]] =  restaurant
    return restaurants_dict

if __name__ == "__main__":
    image_json_path = "C:/Users/sanan/Desktop/yelp_project/yelp_dataset/yelp_dataset/photo.json"
    restaurant_json_path = "C:/Users/sanan/Desktop/yelp_project/yelp_dataset/yelp_dataset/business.json"
    restaurant_list_path = "C:/Users/sanan/Desktop/yelp_project/algorithm/encoded.h5"
    subset_files(image_json_path, restaurant_json_path, restaurant_list_path)
