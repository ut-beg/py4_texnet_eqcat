import csv
from datetime import datetime
import json

with open ("config.json","r") as configfile:
    config=json.load(configfile)

with open(config["inputcsvpath_event"],'r') as texnetevent:
    readfile=csv.reader(texnetevent)

    with open(config["outputcsvpath_event"],'w',newline='') as texneteventplus:
        writefile=csv.writer(texneteventplus)
        
        for i,row in enumerate(readfile):
            if i==0:
                writefile.writerow(["EventID","Status","OriginD","OriginT","Magnitude","MagType","Latitude","LatErr","Longitude","Long_Err","Dp_km_MSL","Dp_km_GS","Depth_unc","Qyear","omonth","oday","oyear"])
            else:
                result=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]]
                origdate=row[2]
                year = int(origdate.split("-")[0])
                day =  origdate.split("-")[2]
                month = origdate.split("-")[1]

                if month[0] == "0":
                    month = month[1]
                if day[0] == "0":
                    day = day[1]
                month, day = int(month), int(day)
                quarter = ""

                if month < 4:
                   quarter = "Q1"
                if month > 3 and month < 7:
                   quarter = "Q2"
                if month > 6 and month < 10:
                   quarter = "Q3"
                if month > 9:
                   quarter = "Q4"

                if config["filterbymagnitude"]:
                    if float(row[4]) >=config["magnitudethreshold"]:
                        result.append(str(year) + " " + quarter)
                        result.append(origdate.split("-")[1])
                        result.append(origdate.split("-")[2])
                        result.append(int(origdate.split("-")[0]))
                        writefile.writerow(result)
                else:
                    result.append(str(year) + " " + quarter)
                    result.append(origdate.split("-")[1])
                    result.append(origdate.split("-")[2])
                    result.append(int(origdate.split("-")[0]))
                    writefile.writerow(result)
