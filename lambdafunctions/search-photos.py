import boto3
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


def lambda_handler(event, context):
    # Extract the user input text from the input event
    user_input = "show me dogs"

    # Lex bot
    lex = boto3.client("lexv2-runtime", region_name="us-east-1")

    # Invoke the Lex v2 bot with the user input
    bot_id = "4G2QTRTNLS"
    bot_alias_id = "TSTALIASID"
    locale_id = "en_US"

    response = lex.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        localeId=locale_id,
        sessionId="abc1234",
        text=user_input,
    )

    if "sessionState" in response:
        # Get keywords
        message = response["sessionState"]["intent"]["slots"]["Keyword"]["values"]
        keywords = []
        match_query = []
        for i in range(len(message)):
            keywords.append(message[i]["value"]["interpretedValue"])
            match_query.append({"term": {"labels": keywords[i]}})
        # return match_query

        # Query ElasticSearch
        index = "photos"
        host = "search-photos1-hwrbp5mxflgqrrzwku2dllowjm.us-east-1.es.amazonaws.com"
        url = "https://" + host + "/" + index + "/_search/"

        headers = {"Content-Type": "application/json"}
        region = "us-east-1"
        service = "es"

        session = boto3.Session()
        credentials = session.get_credentials()

        auth = AWSRequestsAuth(
            aws_access_key=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            aws_host=host,
            aws_region=region,
            aws_service=service,
            aws_token=credentials.token,
        )

        query = {"query": {"bool": {"should": match_query, "minimum_should_match": 1}}}

        headers = {"Content-Type": "application/json"}

        response = requests.get(url, auth=auth, headers=headers, json=query)
        return response.json()
        hits = response.json()["hits"]["hits"]
        return_photos = [hit["_source"]["keyword"] for hit in hits]

        return return_photos

    return {"statusCode": 500, "body": "No response from Lex!"}
