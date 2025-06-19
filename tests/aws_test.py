import os

import boto3
from dotenv import load_dotenv

load_dotenv(".env")


client = boto3.client("polly", region_name="ap-southeast-2")
response = client.describe_voices()
print(response)
