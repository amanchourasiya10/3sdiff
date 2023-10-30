import json


def checkQHeader(text):
    text = text.strip()
    if (text[:6].find("POST") != -1):
        return True
    return False


def checkQuery(text):
    text = text.strip()
    if (text[:30].find("AnswerEntityRequests") != -1):
        return True
    return False


def checkResponse(text):
    text = text.strip()
    if (text[:30].find("ApiVersion") != -1):
        return True
    return False


def checkRHeader(text):
    text = text.strip()
    if (text[:6].find("HTTP") != -1):
        return True
    return False


def processData(splitData):
    print("kay be")
    processedData = []
    print("ayayayyaya")
    for elem in splitData:
        if (check_string(elem)):
            processedData.append(elem)

    return processedData


def headers_to_dict(headers):
    if (not headers):
        return {}
    
    lines = headers.strip().split('\n')

    method, url = lines[0].split(' ', 1)
    headers_dict = {method: url}

    for line in lines[1:]:
        try:
            key, value = line.split(':', 1)
        except:
            key, value = line.split(' ', 1)

        headers_dict[key.strip()] = value.strip()

    return json.dumps(headers_dict)


def check_string(s):
    return any(char.isalnum() for char in s)


def parseText(content):
    try:
        splitData = processData(content.split('\r\n\r\n'))

        if (len(splitData) == 3):
            headers = splitData[0]
            query = splitData[1].split('}\r\nHTTP')[0] + '}'

            resHeaders = 'HTTP' + splitData[1].split('}\r\nHTTP')[1]
            response = splitData[2]
        elif (len(splitData) == 1):
            text = splitData[0].strip()
            if (checkQHeader(text)):
                headers = text
                query = '{}'
                resHeaders = ''
                response = '{}'
            elif (checkQuery(text)):
                headers = ''
                query = text
                resHeaders = ''
                response = '{}'
            elif (checkResponse(text)):
                headers = text
                query = '{}'
                resHeaders = ''
                response = text
            elif (checkRHeader(text)):
                headers = text
                query = '{}'
                resHeaders = text
                response = '{}'
        elif (len(splitData) == 2):
            if (checkQHeader(splitData[0]) and checkQuery(splitData[1])):
                headers = splitData[0]
                query = splitData[1]
                resHeaders = ''
                response = '{}'
            elif (checkRHeader(splitData[0]) and checkResponse(splitData[1])):
                headers = ''
                query = '{}'
                resHeaders = splitData[0]
                response = splitData[1]
            elif (checkQHeader(splitData[0]) and checkRHeader(splitData[1])):
                headers = splitData[0]
                query = '{}'
                resHeaders = splitData[1]
                response = '{}'

        return {"queryHeader": headers_to_dict(headers), "query": query, "responseHeader": headers_to_dict(resHeaders), "response": response}
    except:
        return {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}
