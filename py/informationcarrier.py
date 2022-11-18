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
csv2 = "lod_object_metadata.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\csv") + "\\" + csv
file_in2 = dir_path.replace("\\py", "\\csv") + "\\" + csv2

print(file_in)
print(file_in2)

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

# add parent items
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 250 == 0:
        print(tmpno)
    lineNo += 1
    lines.append("no:obj_" + str(row['id']) + " " + "rdf:type" + " lado:InformationCarrier .")
    lines.append("no:obj_" + str(row['id']) + " " + "rdfs:label" + " " + "'" + str(row['label']).replace('\'', '`') + "'@en" + ".")
    lines.append("no:obj_" + str(row['id']) + " " + "lado:hasType" + " " + "lado:" + str(row['type']).capitalize().replace(" ", "") + "" + ".")
    img = str(row['img']).lower()
    if "navis3" in img:
        img = img.replace("https://www1.rgzm.de/navis3/", "https://gitlab.rlp.net/wissit/img/navisone-images/-/raw/main/")
    elif "/navis/ships/" in img:
        img = img.replace("/navis/ships/", "https://gitlab.rlp.net/wissit/img/navisone-images/-/raw/main/")
    elif "alta" in img:
        img = "https://gitlab.rlp.net/wissit/img/navisone-images/-/raw/main/" + img
    else:
        img = "https://gitlab.rlp.net/wissit/img/navisone-images/-/raw/main/" + img
    lines.append("no:obj_" + str(row['id']) + " " + "lado:hasImage" + " " + "<" + img + "> .")
    doclink = "https://archaeolink.github.io/navisone-lod/obj_" + str(row['id']) + "/index.html"
    lines.append("no:obj_" + str(row['id']) + " " + "rdfs:seeAlso" + " " + "<" + doclink + "> .")
    # prov-o
    lines.append("no:" + str(row['id']) + " " + "prov:wasAttributedTo" + " no:ImportPythonScript .")
    lines.append("no:" + str(row['id']) + " " + "prov:wasDerivedFrom" + " <http://www.wikidata.org/entity/Q115264680> .")
    lines.append("no:" + str(row['id']) + " " + "prov:wasGeneratedBy" + " no:activity_" + str(row['id']) + " .")
    lines.append("no:activity_" + str(row['id']) + " " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("no:activity_" + str(row['id']) + " " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("no:activity_" + str(row['id']) + " " + "prov:endedAtTime '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("no:activity_" + str(row['id']) + " " + "prov:wasAssociatedWith" + " no:ImportPythonScript .")
    lines.append("")

# read csv file
data2 = pd.read_csv(
    file_in2,
    encoding='utf-8',
    sep='|',
    usecols=['fk_id_object', 'name', 'en', 'de']
)
print(data2.info())

# add parent items
for index, row in data2.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 250 == 0:
        print(tmpno)
    lineNo += 1
    if str(row['name']) == "material":
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:madeOfString" + " " + "'" + str(row['en']) + "'@en .")
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:madeOfString" + " " + "'" + str(row['de']) + "'@de .")
    elif str(row['name']) == "culture":
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:timeInterval" + " " + "'" + str(row['en']) + "'@en .")
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:timeInterval" + " " + "'" + str(row['de']) + "'@de .")
    elif str(row['name']) == "technique":
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:madeByString" + " " + "'" + str(row['en']) + "'@en .")
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:madeByString" + " " + "'" + str(row['de']) + "'@de .")
    elif str(row['name']) == "objecttype":
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:hasObjectTypeString" + " " + "'" + str(row['en']) + "'@en .")
        lines.append("no:obj_" + str(row['fk_id_object']) + " " + "lado:hasObjectTypeString" + " " + "'" + str(row['de']) + "'@de .")

#####################

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing turtle files...")

f = 0
step = 100000
filename = "navisone_obj.ttl"
prefixes = ""
prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
prefixes += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\r\n"
prefixes += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
prefixes += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
prefixes += "@prefix dc: <http://purl.org/dc/elements/1.1/> .\r\n"
prefixes += "@prefix dct: <http://purl.org/dc/terms/> .\r\n"
prefixes += "@prefix prov: <http://www.w3.org/ns/prov#> .\r\n"
prefixes += "@prefix lado: <http://archaeology.link/ontology#> .\r\n"
prefixes += "@prefix no: <http://data.archaeology.link/data/navisone/> .\r\n"
prefixes += "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\r\n"
prefixes += "@prefix wd: <http://www.wikidata.org/entity/> .\r\n"
prefixes += "@prefix cc: <http://creativecommons.org/ns#> .\r\n"
prefixes += "\r\n"

for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\data") + "\\" + filename
    file = codecs.open(filename, "w", "utf-8")
    file.write("# create triples from " + csv + " and " + csv2 + " \r\n")
    file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print("Yuhu! > " + filename)
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
