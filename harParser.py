import json

def createHeaders(headersList):
    headers = {}
    for obj in headersList:
        headers[obj['name']] = obj['value']
    
    return json.dumps(headers)

def parseHar(content):
    obj = json.loads(content)

    query = obj['log']['entries'][0]['request']['postData']['text']
    headers = createHeaders(obj['log']['entries'][0]['request']['headers'])
    resHeaders = createHeaders(obj['log']['entries'][0]['response']['headers'])
    response = obj['log']['entries'][0]['response']['content']['text']

    return {"queryHeader": headers, "query": query, "responseHeader": resHeaders, "response": response}