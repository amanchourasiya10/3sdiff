import json

def createHeaders(headersList):
    headers = {}
    for obj in headersList:
        headers[obj['name']] = obj['value']
    
    return json.dumps(headers)

def parseHar(content):
    obj = json.loads(content)
    try:
        query = obj['log']['entries'][0]['request']['postData']['text']
    except:
        query = '{}'
    
    try:
        headers = createHeaders(obj['log']['entries'][0]['request']['headers'])
    except:
        headers = '{}'
    
    try:
        resHeaders = createHeaders(obj['log']['entries'][0]['response']['headers'])
    except:
        resHeaders = '{}'

    try:
        response = obj['log']['entries'][0]['response']['content']['text']
    except:
        response = '{}'

    return {"queryHeader": headers, "query": query, "responseHeader": resHeaders, "response": response}