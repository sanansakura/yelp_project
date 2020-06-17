import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET

def upload_file(file, bucket_name, acl="public-read"):
	try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as error:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", error)
        return error
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
