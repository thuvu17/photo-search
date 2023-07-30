import requests
import json
import boto3
from requests_aws4auth import AWS4Auth
import datetime


def check_document_format(doc):
    expected_keys = set(["objectKey", "bucket", "createdTimestamp", "labels"])
    doc_keys = set(doc.keys())

    # Check if there are any unexpected keys in the document
    if doc_keys - expected_keys:
        return False

    # Check if 'objectKey' and 'bucket' are strings
    if not isinstance(doc["objectKey"], str) or not isinstance(doc["bucket"], str):
        return False

    # Check if 'createdTimestamp' is a string and can be converted to a datetime object
    try:
        datetime.datetime.strptime(doc["createdTimestamp"], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False

    # Check if 'labels' is a list and all its elements are strings
    if not isinstance(doc["labels"], list) or not all(
        isinstance(label, str) for label in doc["labels"]
    ):
        return False

    # If the document passed all checks, return True
    return True


def is_duplicate(bucket, object_key, existing_pairs):
    return (bucket, object_key) in existing_pairs


if __name__ == "__main__":
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        "us-east-1",
        "es",
        session_token=credentials.token,
    )
    host = "search-photos1-hwrbp5mxflgqrrzwku2dllowjm.us-east-1.es.amazonaws.com"
    url = "https://" + host + "/photos/_search/"
    response = requests.get(url, auth=awsauth)
    existing_pairs = set()
    incorrect_docs = []
    duplicate_docs = []

    for hit in response.json()["hits"]["hits"]:
        doc = hit["_source"]
        doc_id = hit["_id"]

        if not check_document_format(doc):
            incorrect_docs.append(doc_id)
            print(f"Incorrect document format for document {doc_id}: {doc}")
        else:
            bucket = doc["bucket"]
            object_key = doc["objectKey"]

            if is_duplicate(bucket, object_key, existing_pairs):
                duplicate_docs.append(doc_id)
                print(f"Duplicate document detected with id {doc_id}: {doc}")
            else:
                existing_pairs.add((bucket, object_key))

    for doc_id in incorrect_docs + duplicate_docs:
        proceed = input(f"Proceed with deletion of document {doc_id}? (y/n): ")
        if proceed.lower() == "y":
            url = f"https://{host}/photos/_doc/{doc_id}"
            response = requests.delete(url, auth=awsauth)
            if response.status_code == 200:
                print(f"Successfully deleted document {doc_id}")
            else:
                print(f"Failed to delete document {doc_id}. Response: {response.text}")
        else:
            print("Skipped deletion.")
