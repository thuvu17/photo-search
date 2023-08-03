import boto3
import json
import uuid
from datetime import datetime
import base64


def lambda_handler(event, context):
    is_base64_encoded = event.get("isBase64Encoded", False)
    file_content = event["body"]
    print({key: value for key, value in event.items() if key != "body"})
    if is_base64_encoded:
        file_content = base64.b64decode(file_content)

    if len(file_content) > 5 * 1024 * 1024:
        return {
            "statusCode": 400,
            "body": json.dumps("File size too large: must be under 5MB"),
        }

    custom_labels = event["headers"].get("x-amz-meta-customLabels", "")

    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    bucket_name = "burning-photos"
    file_path = f"{timestamp}_{unique_id}.jpg"

    s3 = boto3.client("s3")
    try:
        response = s3.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=file_content,
            Metadata={"x-amz-meta-customLabels": custom_labels},
        )
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }

        return {
            "statusCode": 200,
            "body": json.dumps("File uploaded successfully!"),
            "headers": headers,
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"An error occurred while uploading the file: {str(e)}"),
        }
