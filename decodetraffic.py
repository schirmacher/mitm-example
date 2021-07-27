import brotli
import json
import sys
from os import listdir
from os.path import isfile, join


def body(file, length):
    data = file.read(length)
    return data

def parserequest(file):

    content_length = 0
    content_encoding = ''
    request = file.readline()
    #sys.stdout.buffer.write(request)

    while True:
        line = file.readline()
        if not line:
            break
        elif line == b'\r\n':
            data = body(file, content_length)
            if content_encoding == b'br':
                data = brotli.decompress(data)
            #print()
            #sys.stdout.buffer.write(data)
            return request, data

        entity, parameter = line.split(b': ', 1)
        if entity == b'Content-Length':
            content_length = int(parameter)
        elif entity == b'Content-Encoding':
            content_encoding = parameter.strip()

        #sys.stdout.buffer.write(line)

def parseresponse(file):

    content_length = 0
    content_encoding = ''
    content_type = b''
    transfer_encoding = ''
    upgrade = ''
    status = file.readline()
    #sys.stdout.buffer.write(status)

    while True:
        line = file.readline()
        if not line:
            break
        elif line == b'\r\n':
            if upgrade == b'websocket':
                currentPos = file.tell()
                file.seek(0, 2)  # move to end of file
                endPos = file.tell()  # get current position
                length = endPos - currentPos
                file.seek(currentPos, 0)
                data = file.read(length)
            elif transfer_encoding == b'chunked':
                line = file.readline()
                chunksize = int(line, 16)
                data = b''
                while chunksize > 0:
                    data += file.read(chunksize)
                    line = file.readline()
                    line = file.readline()
                    chunksize = int(line, 16)
                line = file.readline()
            else:
                data = body(file, content_length)
            if content_encoding == b'br':
                if len(data) > 0:
                    try:
                        data = brotli.decompress(data)
                    except:
                        print("brotli decompress error")
                        data = b''
                        pass
            #print()
            #sys.stdout.buffer.write(data)
            return status, data, content_type

        entity, parameter = line.split(b': ', 1)
        if entity == b'Content-Length':
            content_length = int(parameter)
        elif entity == b'Content-Encoding':
            content_encoding = parameter.strip()
        elif entity == b'Content-Type':
            content_type = parameter.strip()
        elif entity == b'Transfer-Encoding' or entity == b'transfer-encoding':
            transfer_encoding = parameter.strip()
        elif entity == b'Upgrade':
            upgrade = parameter.strip()
        sys.stdout.buffer.write(line)
    return b'', b'', b''

def process(filename, outname):

    counter = 0
    extensions = {
        "application/javascript": ".js",
        "application/json": ".json",
        "application/octet-stream": ".bin",
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }
    file = open(filename, 'rb')
    file.seek(0, 2)  # move to end of file
    length = file.tell()  # get current position
    file.seek(0, 0)  # go back to where we started

    while file.tell() < length:
        print("Processing " + filename + " request #" + str(counter))
        request, requestdata = parserequest(file)
        status, responsedata, contenttype = parseresponse(file)
        contenttype = contenttype.decode('ascii')
        if contenttype == "application/json":
            try:
                responsedata = json.dumps(json.loads(responsedata), indent=4, sort_keys=True).encode("utf-8")
            except:
                pass

        if len(responsedata) > 0:
            #outfilename = outname + "-" + str(counter) + extensions.get(contenttype, ".txt")
            outfilename = "%s-%03.3d%s" % (outname, counter, extensions.get(contenttype, ".txt"))
            outfile = open(outfilename, 'wb')
            outfile.write(responsedata)
            outfile.close()

        sys.stdout.buffer.write(request)
        print()
        sys.stdout.buffer.write(requestdata)
        print()
        print()
        #sys.stdout.buffer.write(responsedata)

        counter += 1

        print()
        print('-----------')
        print()

    file.close()

def run():

    path = "."
    for f in listdir(path):
        filename = join(path, f)
        if isfile(filename) and filename.endswith(".log"):
            process(filename, filename[:-4])

if __name__ == '__main__':
    run()


