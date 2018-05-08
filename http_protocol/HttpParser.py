def httpParser(bStream, req):
    try:
        strArray = bStream.decode('utf-8').split("\r\n\r\n")
        #header
        headerArray = strArray[0].split("\r\n")
        for index, value in enumerate(headerArray):
            if index == 0:
                #method,uri,ver
                requestLineArray = value.split(" ")
                req.method = requestLineArray[0]
                req.uri = requestLineArray[1]
                req.ver = requestLineArray[2]
            else:
                headerLineArray = value.split(": ")
                headerKey = headerLineArray[0]
                headerValue = headerLineArray[1]
                req.header[headerKey] = headerValue

        #content
        if len(strArray) > 1:
            req.context = strArray[1]

    except Exception as e:
        print("httpparser error", e)

    # else:
    #     req.print()
