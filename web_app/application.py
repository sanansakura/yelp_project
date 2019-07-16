from flask import Flask, render_template, request
application = Flask(__name__)

@application.route("/")
def index():
	return render_template('home.html')

@application.route("/results")
def results():

	#sample instance from business.json
	info = {"business_id":"1SWheh84yJXfytovILXOAQ", \
	"name":"Arizona Biltmore Golf Club","address":"2818 E Camino Acequia Drive",\
	"city":"Phoenix","state":"AZ","postal_code":"85016","latitude":33.5221425,\
	"longitude":-112.0184807,"stars":3.0,"review_count":5,"is_open":0,\
	"attributes":{"GoodForKids":"False"},"categories":"Golf, Active Life","hours":None}
	name = info["name"]
	address = info["address"] + ", " + info["city"] + ", " + info["state"] + ", " + info["postal_code"]
	categories = info["categories"]

	restaurant_info_list = [{"name": name, "address": address, "categories" : categories}]
	return render_template("results.html", restaurants = restaurant_info_list)


if __name__ == "__main__":
	application.run()
