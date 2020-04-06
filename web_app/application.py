from flask import Flask, render_template, request, redirect, flash
from werkzeug import secure_filename
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET, SECRET_KEY
from algorithm import *

#set up the s3 storage credentials 
S3 = boto3.client(
   		"s3",
  		aws_access_key_id=S3_KEY,
   		aws_secret_access_key=S3_SECRET
		)

#flask app settings
application = Flask(__name__)
application.secret_key = SECRET_KEY
application.config['DEBUG'] = False

@application.route("/")
def index():
	return render_template('home.html')

@application.route("/", methods=['POST'])
def upload_file():
	if request.method == "POST":
		#print(request.files)
		if "file" not in request.files:
			return redirect(request.url)
		else:
			file = request.files["file"]
			#print(file.filename)
		if file.filename == "":
			return "Please select a file."
		#elif file and allowed_file(file.filename):
		elif file.filename:
			#print(type(file))
			file.filename = secure_filename("input_image.jpg")
			#print(file, S3_BUCKET, file.filename)
			try:
				S3.upload_fileobj(
				file,
				S3_BUCKET,
				file.filename,
				ExtraArgs={
				"ACL": "public-read",
				"ContentType": file.content_type
				}
				)
			except Exception as error:
       		 # This is a catch all exception, edit this part to fit your needs.
				print("Something Happened: ", error)
				return error
			flash('File successfully uploaded')
			return redirect("/results")
	else:
		return render_template('home.html')

@application.route("/results")
def results():
	#Fetch the image data from s3 storage
	S3.download_file(S3_BUCKET, "input_image.jpg", "temp/input_image.jpg")

	#The relavant file paths
	input_image_path = "temp/input_image.jpg"
	model_path = "src/model.h5"
	photo_business_path = "data/photo_business.json"
	image_id_label_path = "data/image_id_to_label.json"
	food101_label_mapping = "data/food101_label_map_inv.json"

	#run the algorithm
	info_list = find_highest_score_rest(
		input_image_path,
		model_path,
		image_id_label_path,
		photo_business_path,
		food101_label_mapping
		 )
	
	#subset the restaurant information
	restaurant_info_list = []
	for info in info_list:
		info_summary = {}
		info_summary["name"] = info["info"]["name"]
		info_summary["address"] = info["info"]["address"] + ", " + info["info"]["city"] + ", " + info["info"]["state"]
		info_summary["categories"] = info["info"]["categories"]
		restaurant_info_list.append(info_summary)
	return render_template("results.html", restaurants = restaurant_info_list)


if __name__ == "__main__":
	application.run()
