import boto3
from requests_aws4auth import AWS4Auth
import requests


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    s3 = boto3.client("s3")
    rekognition = boto3.client("rekognition")
    response = s3.get_object(Bucket=bucket, Key=key)
    custom_labels = response["Metadata"].get("x-amz-meta-customlabels", "").split(",")
    rekognition_response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            },
        },
    )
    detected_labels = [label["Name"] for label in rekognition_response["Labels"]]
    labels = custom_labels + detected_labels
    image_metadata = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": response["LastModified"].strftime("%Y-%m-%d %H:%M:%S"),
        "labels": labels,
    }
    region = "us-east-1"
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token,
    )
    index = "photos"
    host = "search-photos1-hwrbp5mxflgqrrzwku2dllowjm.us-east-1.es.amazonaws.com"
    url = "https://" + host + "/" + index + "/_doc/"
    headers = {"Content-Type": "application/json"}
    requests.post(url, auth=awsauth, json=image_metadata, headers=headers)
