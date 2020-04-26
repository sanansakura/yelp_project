import os, shutil
import json
def sort_image():
    '''
    Move the images contained in the yelp_photos folder to corresponding folders
    according to their labels specified in photo.json.
    '''
    #create folders if the folder does not exists
    labels = ["food", "drink", "menu", "inside", "outside"]
    for label in labels:
        if os.path.isdir(label):
            pass
        else:
            print("creating folder '" + label + "'")
            os.mkdir(label)
    #load photo.json
    photo_info = []
    with open("yelp_photos/photo.json") as photo_json:
        for line in photo_json:
            info_dict = json.loads(line)
            photo_id, photo_label = info_dict["photo_id"], info_dict["label"]
            old_dir = "yelp_photos/photos/" + photo_id + ".jpg"
            if photo_label == "food":
                #shutil.move(old_dir, "food")
                pass
            elif photo_label == "drink":
                shutil.move(old_dir, "drink")
            elif photo_label == "menu":
                shutil.move(old_dir, "menu")
            elif photo_label == "inside":
                shutil.move(old_dir, "inside")
            elif photo_label == "outside":
                shutil.move(old_dir, "outside")
            else:
                pass
           

    print(info_dict)
if __name__ == "__main__":
    sort_image()
    
