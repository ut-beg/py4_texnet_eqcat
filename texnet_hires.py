import csv
import json

with open ("C:/DataCB/github/py4_texnet_eqcat/config.json","r") as configfile:
    config=json.load(configfile)

with open(config["inputcsvpath_hires"],'r') as texnethires:
    readfile=csv.reader(texnethires)

    with open(config["outputcsvpath_hires"],'w',newline='') as texnethiresplus:
        writefile=csv.writer(texnethiresplus)
        
        for i,row in enumerate(readfile):
            if i==0:
                writefile.writerow(["eventID","year","month","day","LatReloc","LonReloc","depthReloc","mag","LatCat","LonCat","depthCat"])
            else:
                result=[row[2],row[3],row[4],row[5],row[10],row[11],row[12],row[13],row[25],row[26],row[27]]
                writefile.writerow(result)
