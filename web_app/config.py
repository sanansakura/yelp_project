import os

S3_BUCKET = os.environ.get("AWSBucketName")
S3_KEY = os.environ.get("AWSAccessKeyId")
S3_SECRET = os.environ.get("AWSSecretKey")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000

