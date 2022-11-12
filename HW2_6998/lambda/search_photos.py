import json
import requests
import boto3

def lambda_handler(event, context):
    # get the q from event object
    print("This is event: ",event)
    #q = event['queryStringParameters']['q']
    q=event['inputTranscript']
    print(q)
    print('Request: '+ q)
    # connect to lex bot
    # LexV2 client uses 'lexv2-runtime'
    client = boto3.client('lexv2-runtime')
    response = client.recognize_text(
        botId='IAYDFGIKXY',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=q)
    key = response['messages'][0]['content']
    print('Keyword: ' + key)
    # not matched with uttarance
    if key=='no':
        return {"statusCode": 200, "body": ""}
    # search in the elasticsearch photos
    headers = { "Content-Type": "application/json" }
    index = "photos"
    query = {
        "query": {
            "match_phrase": {
                "labels": str(key)
            }
        }
    }
    url = 'https://search-photos-kawwnot2xsbqag4malrcxrtunu.us-east-1.es.amazonaws.com' + '/' + index + '/_search/'
    result = requests.get(url, headers=headers, data=json.dumps(query))
    result = json.loads(result.text)
    hits = result['hits']['hits']
    res = set()
    for item in hits:
        temp = 'https://b2hw26998.s3.amazonaws.com/'+str(item["_source"]["objectKey"])
        res.add(temp)
    print(res)
    if len(res)==0:
        return {"statusCode": 200, "body": ""}
    return {"statusCode": 200, 
    "body": "  ".join(list(res)), 
    "headers":{"Access-Control-Allow-Origin":"*"}}
