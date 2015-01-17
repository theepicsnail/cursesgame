import json
import sys

if len(sys.argv) != 2 or sys.argv[1][-4:] != "json":
    print "Usage:"
    print "python %s [file.json]" % sys.argv[0]
    sys.exit(1)

data = json.load(file(sys.argv[1]))
width = data['width']
height = data['height']
layers = data['layers']

with open(sys.argv[1][:-4]+"lvl", "w") as out:
    out.write("%s,%s" % (width, height))
    for layer in layers:
        for data in layer["data"]:
            out.write(",%s" % data)

