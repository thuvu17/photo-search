import boto3
import uuid
import json

# import requests
# from aws_requests_auth.aws_auth import AWSRequestsAuth


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
    print("Lex response: ", keywords)
    # intents = lex_response.get("messages", [])
    # slots = {
    #     slot["name"]: slot["value"]["interpretedValue"]
    #     for message in intents
    #     for slot in message.get("slots", [])
    #     if slot["shape"] == "Scalar"
    # }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": keywords,
            }
        ),
    }
    # # Lex bot

    # # Invoke the Lex v2 bot with the user input
    # bot_id = "4G2QTRTNLS"
    # bot_alias_id =     # locale_id = ""

    # if "sessionState" in response:
    #     # Get keywords
    #     message = response["sessionState"]["intent"]["slots"]["Keyword"]["values"]
    #     keywords = []
    #     match_query = []
    #     for i in range(len(message)):
    #         keywords.append(message[i]["value"]["interpretedValue"])
    #         match_query.append({"term": {"labels": keywords[i]}})
    #     # return match_query

    #     # Query ElasticSearch
    #     index = "photos"
    #     host = "search-photos1-hwrbp5mxflgqrrzwku2dllowjm.us-east-1.es.amazonaws.com"
    #     url = "https://" + host + "/" + index + "/_search/"

    #     headers = {"Content-Type": "application/json"}
    #     region = "us-east-1"
    #     service = "es"

    #     session = boto3.Session()
    #     credentials = session.get_credentials()

    #     auth = AWSRequestsAuth(
    #         aws_access_key=credentials.access_key,
    #         aws_secret_access_key=credentials.secret_key,
    #         aws_host=host,
    #         aws_region=region,
    #         aws_service=service,
    #         aws_token=credentials.token,
    #     )

    #     query = {"query": {"bool": {"should": match_query, "minimum_should_match": 1}}}

    #     headers = {"Content-Type": "application/json"}

    #     response = requests.get(url, auth=auth, headers=headers, json=query)
    #     return response.json()
    #     hits = response.json()["hits"]["hits"]
    #     return_photos = [hit["_source"]["keyword"] for hit in hits]

    #     return return_photos

    # return {"statusCode": 500, "body": "No response from Lex!"}
