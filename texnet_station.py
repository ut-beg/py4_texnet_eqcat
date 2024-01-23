import csv
from datetime import datetime
import json

with open ("config.json","r") as configfile:
    config=json.load(configfile)

with open(config["inputcsvpath_station"],'r') as texnetstation:
    readfile=csv.reader(texnetstation)

    with open(config["outputcsvpath_station"],'w',newline='') as texnetstationplus:
        writefile=csv.writer(texnetstationplus)
        for i,row in enumerate(readfile):
            if i==0:
                writefile.writerow(["network","station","longitude","latitude","affiliation","archive","location","place","elevation","enddate","startdate","label"])
            else:
                result=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[10],row[9]]
                labelinfo=""
                network=row[0]
                station=row[1]
                enddate=row[10]
                stationfound=False
                if network == "TX":
                    if station[0:2]=="DG":
                        labelinfo= "TexNet short period"
                        stationfound=True
                    if station[0:2]=="OG":
                        labelinfo= "TexNet short period"
                        stationfound=True
                    if station[0:2] == "EF":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:2] == "FW":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:2] == "MB":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:2] == "PB":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:2] == "PH":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:2] == "SN":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if station[0:4] == "SNAG":
                        labelinfo= "TexNet permanent"
                        stationfound=True
                    if station[0:4] == "ELG6":
                        labelinfo= "TexNet short period"
                        stationfound=True
                    if station[0:4] == "ET01":
                        labelinfo= "TexNet portable"
                        stationfound=True
                    if stationfound == False:
                        labelinfo= "TexNet permanent"

                if network in ["2T","4F","4T","ZW"]:
                    labelinfo = "TexNet portable"

                if network in ["4O","DB"]:
                    labelinfo = "Private shared"

                if network in ["AE","AG","AM","EP","G","GM","IM","IU","MG","MX","N4","NQ","OK","PI","SC","US","ZP"]:
                    labelinfo = "Other"

                if len(enddate)>0:
                    labelinfo = "Decomissioned"
                
                result.append(labelinfo)
                writefile.writerow(result)