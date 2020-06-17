import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET, SECRET_KEY


S3 = boto3.client(
   		"s3",
  		aws_access_key_id=S3_KEY,
   		aws_secret_access_key=S3_SECRET
		)


S3.download_file(S3_BUCKET, "input_image.jpg", "temp/input_image.jpg")
