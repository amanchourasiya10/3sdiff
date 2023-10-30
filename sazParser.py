from txtParser import *

def update_dict(input_dict):
    keys_and_values = {
        'query': '{}',
        'response': '{}',
        'queryHeader': '{}',
        'responseHeader': '{}'
    }

    for key, value in keys_and_values.items():
        if key not in input_dict:
            input_dict[key] = value

    return input_dict

def parseSaz(content):
    try:
        splitData = processData(content.split('\r\n\r\n'))

        if (len(splitData) == 1):
            text = splitData[0].strip()
            if (checkQHeader(text)):
                headers = text
                return {"queryHeader": headers_to_dict(headers)}
            elif (checkQuery(text)):
                query = text
                return {"query": query}
            elif (checkResponse(text)):
                response = text
                return {"response": response}
            elif (checkRHeader(text)):
                resHeaders = text
                return {"responseHeader": headers_to_dict(resHeaders)}
        elif (len(splitData) == 2):
            print("Miaa--------------------------------------------------------------------------------")
            if (checkQHeader(splitData[0]) and checkQuery(splitData[1])):
                headers = splitData[0]
                query = splitData[1]
                return {"queryHeader": headers_to_dict(headers), "query": query}
            elif (checkRHeader(splitData[0]) and checkResponse(splitData[1])):
                resHeaders = splitData[0]
                response = splitData[1]
                return {"responseHeader": headers_to_dict(resHeaders), "response": response}
        else:
            return {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}
    except:
        return {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}

