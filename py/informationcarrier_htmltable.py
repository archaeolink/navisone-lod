__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2022, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@rgzm.de"
__status__ = "beta"
__update__ = "2022-11-18"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib  # py3
import sys

# set UTF8 as default
importlib.reload(sys)  # py3
# reload(sys) #py2

# uncomment the line below when using Python version <3.0
# sys.setdefaultencoding('UTF8')

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input csv
csv = "lod_objects.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\csv") + "\\" + csv

print(file_in)

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['id', 'label', 'type', 'img']
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []

# start table
lines.append('<table border="1">')
lines.append('<tr><th>ID</th><th>label</th><th>type</th><th>LOD page</th></tr>')
for index, row in data.iterrows():
    url = '<a href="https://archaeolink.github.io/navisone-lod/obj_' + str(row['id']) + '/index.html" target="_blank">' + 'navisone-lod/obj_' + str(row['id']) + '</a>'
    lines.append('<tr><td>' + str(row['id']) + '</td><td>' + str(row['label']) + '</td><td>' + str(row['type']) + '</td><td>' + url + '</td></tr>')
lines.append('</table>')

#####################

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing turtle files...")

filename = "objtable.htm"
for x in range(1, int(files) + 1):
    filename = dir_path.replace("\\py", "\\src") + "\\" + filename
    file = codecs.open(filename, "w", "utf-8")
    for i, line in enumerate(lines):
        file.write(line)
        file.write("\r\n")
    print("Yuhu! > " + filename)
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
