import boto3
import traceback
from requests_aws4auth import AWS4Auth
import requests


def lambda_handler(event, context):
    labels = custom_labels + detected_labels
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        s3 = boto3.client("s3")
        rekognition = boto3.client("rekognition")

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            custom_labels = (
                response["Metadata"].get("x-amz-meta-customLabels", "").split(",")
            )
            rekognition_response = rekognition.detect_labels(
                Image={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key,
                    },
                },
            )
        except Exception as e:
            print(f"Failed to get object or detect labels. Exception: {str(e)}")
            print(traceback.format_exc())
            return

        detected_labels = [label["Name"] for label in rekognition_response["Labels"]]
        labels = custom_labels + detected_labels
        image_metadata = {
            "objectKey": key,
            "bucket": bucket,
            "createdTimestamp": response["LastModified"].strftime("%Y-%m-%d %H:%M:%S"),
            "labels": labels,
        }
        print(f"Processing image metadata: {image_metadata}")
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

        try:
            es_response = requests.post(
                url, auth=awsauth, json=image_metadata, headers=headers
            )
            if es_response.status_code in range(200, 299):
                print("Successfully uploaded to Elasticsearch")
            else:
                print(
                    f"Failed to upload to Elasticsearch. Status code: {es_response.status_code}, Response: {es_response.text}"
                )
        except Exception as e:
            print(f"Failed to upload to Elasticsearch. Exception: {str(e)}")
            print(traceback.format_exc())
    except Exception as e:
        print(f"Unexpected error occurred. Exception: {str(e)}")
        print(traceback.format_exc())
