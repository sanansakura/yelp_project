import boto3
import json
import decimal

dynamodb = boto3.resource("dynamodb", region_name = "us-east-2")
table = dynamodb.Table('photo_business')
with open("photo_business.json") as photo_business:
    photo_info = json.load(photo_business, parse_float=decimal.Decimal)
    for photo in photo_info:
        photo_id = photo["photo_id"]
        business_id = photo["business_id"]
        info = photo["info"]
        print("Adding info of: " + photo_id)
        table.put_item(Item = {"photo_id": photo_id, \
                                "business_id": business_id, \
                                "info": info})
