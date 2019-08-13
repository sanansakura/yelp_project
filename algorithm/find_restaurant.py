import numpy as np
import h5py
import json
import os

def replace_empty(info):
    '''
    Fill in the missing information if not provided.
    '''
    if info =="":
        return "Not provided."
    else:
        return info

def subset_files(photo_json_path, business_json_path, restaurant_list_path):
    '''
    Subset the original Json files according to the images.
    '''
    #Extract the list of restaurants
    f = h5py.File(restaurant_list_path, "r")
    restaurant_list = list(f["files_list_0"])
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
    #create a mapping between photo_ids and their business information
    with open(business_json_path, encoding="utf8") as business_json:
        for line in business_json:
            business_info = json.loads(line)
            if business_info["business_id"] in photo_dict_invert:
                for photo_id in photo_dict_invert[business_info["business_id"]]:
                    photo_business_dict[photo_id] = business_info
    #format the information into nicer format
    data_collection = []
    for id in photo_business_dict:
        print(id + " is being processed.")
        data = {}
        data["photo_id"] = id
        data["business_id"] = replace_empty(photo_business_dict[id]["business_id"])
        data["info"] = {}
        data["info"]["name"] = replace_empty(photo_business_dict[id]["name"])
        data["info"]["address"] = replace_empty(photo_business_dict[id]["address"])
        data["info"]["city"] = replace_empty(photo_business_dict[id]["city"])
        data["info"]["state"] = replace_empty(photo_business_dict[id]["state"])
        data["info"]["stars"] = replace_empty(photo_business_dict[id]["stars"])
        data["info"]["categories"] = replace_empty(photo_business_dict[id]["categories"])
        data_collection.append(data)

    with open("photo_business.json", "w") as photo_business_json:
        json.dump(data_collection, photo_business_json)

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
	base_dir = os.getcwd()
	image_json_path = os.path.join(base_dir, 'yelp_dataset/yelp_dataset/photo.json')
    restaurant_json_path = os.path.join(base_dir, "yelp_dataset/yelp_dataset/business.json")
    restaurant_list_path = os.path.join(base_dir, "encoded.h5")
    subset_files(image_json_path, restaurant_json_path, restaurant_list_path)
