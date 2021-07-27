import json
import sys
from os import listdir
from os.path import isfile, join

def process(filename):

    file = open(filename, 'rb')
    jsonObject = json.load(file)
    file.close()
    # do something useful with the json response here
    print(jsonObject)

def run():

    path = "."
    for f in sorted(listdir(path)):
        filename = join(path, f)
        if isfile(filename) and filename.endswith(".json"):
            print("processing " + filename)
            process(filename)

if __name__ == '__main__':
    run()


