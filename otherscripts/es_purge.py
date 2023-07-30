import requests
import boto3
from getpass import getpass
from requests_aws4auth import AWS4Auth


def purge_index(awsauth, host, index):
    url = f"https://{host}/{index}/_search"

    # count number of documents before deletion
    response = requests.get(
        url, auth=awsauth, headers={"Content-Type": "application/json"}
    )
    num_docs = response.json()["hits"]["total"]["value"]

    # Get confirmation from user
    print(f"Number of documents to be deleted: {num_docs}")
    confirmation = getpass(
        f"Are you sure you want to delete all documents in index {index}? Type 'yes' to confirm: "
    )

    if confirmation.lower() == "yes":
        # Delete all documents in the index
        url = f"https://{host}/{index}/_delete_by_query"
        payload = {"query": {"match_all": {}}}
        response = requests.post(
            url,
            auth=awsauth,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        print(f"Deletion status: {response.json()}")

    else:
        print("Operation cancelled.")


if __name__ == "__main__":
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

    purge_index(awsauth, host, index)
