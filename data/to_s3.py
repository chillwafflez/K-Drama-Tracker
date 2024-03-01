import boto3
from dotenv import load_dotenv
import os

load_dotenv() 

s3 = boto3.resource(
    service_name = 's3',
    region_name = 'us-west-1',
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
    