import boto3
import uuid
import json
import requests
from requests_aws4auth import AWS4Auth


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters")
    if not query_params:
        return {
            "statusCode": 403,
            "body": json.dumps({"code": 403, "message": "Missing query parameters"}),
        }
    query = query_params.get("q")
    if not query:
        return {
            "statusCode": 403,
            "body": json.dumps({"code": 403, "message": "Missing query string"}),
        }

    try:
        lex = boto3.client("lexv2-runtime", region_name="us-east-1")
        user_id = str(uuid.uuid4())
        lex_response = lex.recognize_text(
            botId="4G2QTRTNLS",
            botAliasId="TSTALIASID",
            localeId="en_US",
            sessionId=user_id,
            text=query,
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"code": 500, "message": f"Failed to call Lex: {str(e)}"}
            ),
        }

    try:
        keyword_values = (
            lex_response.get("sessionState", {})
            .get("intent", {})
            .get("slots", {})
            .get("Keyword", {})
            .get("values", [])
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "code": 500,
                    "message": f"Failed to extract keyword values from Lex response: {str(e)}",
                }
            ),
        }

    keywords = []
    for value in keyword_values:
        interpreted_value = value.get("value", {}).get("interpretedValue")
        if interpreted_value:
            keywords.append(interpreted_value)

    query_body = {
        "query": {
            "bool": {"should": [{"match": {"labels": keyword}} for keyword in keywords]}
        }
    }

    try:
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
        es_response = requests.get(
            url, auth=awsauth, headers=headers, data=json.dumps(query_body)
        ).json()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"code": 500, "message": f"Failed to call Elasticsearch: {str(e)}"}
            ),
        }

    hits = es_response.get("hits", {}).get("hits", [])

    photos = []
    for hit in hits:
        try:
            photo_data = hit.get("_source", {})
            photo_url = "https://{}.s3.amazonaws.com/{}".format(
                photo_data["bucket"], photo_data["objectKey"]
            )
            photo_labels = photo_data.get("labels", [])
            photos.append({"url": photo_url, "labels": photo_labels})
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"code": 500, "message": f"Failed to process hit: {str(e)}"}
                ),
            }

    return {"statusCode": 200, "body": json.dumps({"results": photos})}
