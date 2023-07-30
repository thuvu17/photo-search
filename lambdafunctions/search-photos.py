import boto3
import uuid
import json
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


def extract_keywords(lex_response):
    keywords = []
    if "Keyword" in lex_response["sessionState"]["intent"]["slots"]:
        keyword_values = lex_response["sessionState"]["intent"]["slots"]["Keyword"][
            "values"
        ]
        for value in keyword_values:
            keywords.append(value["value"]["interpretedValue"])
    return keywords


def lambda_handler(event, context):
    user_id = str(uuid.uuid4())
    query = event.get("queryStringParameters", {}).get("q")
    print(f"Query: {query}")

    lex = boto3.client("lexv2-runtime", region_name="us-east-1")
    lex_response = lex.recognize_text(
        botId="4G2QTRTNLS",
        botAliasId="TSTALIASID",
        localeId="en_US",
        sessionId=user_id,
        text=query,
    )
    keywords = extract_keywords(lex_response)
    print(f"Lex response: {keywords}")

    query_body = {
        "query": {
            "bool": {"should": [{"match": {"labels": keyword}} for keyword in keywords]}
        }
    }
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
    headers = {"Content-Type": "application/json"}
    response = requests.get(
        url, auth=awsauth, headers=headers, data=json.dumps(query_body)
    )
    print(response.json())
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": keywords,
            }
        ),
    }
