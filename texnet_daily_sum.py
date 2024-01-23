import csv
import json
from datetime import datetime

currentmonth = datetime.now().month
currentyear = datetime.now().year

## ENTER START YEAR below
startyear = 2020

print("current year = " + str(currentyear))

welldictionarylist=[]
uniquewelllist=[]

with open ("config.json","r") as configfile:
    config=json.load(configfile)

with open(config["inputcsvpath_sum_daily"],'r') as dailyPostPY:
    readfile=csv.reader(dailyPostPY)
    for i,row in enumerate(readfile):
        if i > 0:
            if i%10==0:
                print("processing row"+str(i))
            UIC=row[0]
            api=row[1]
            slon=row[2]
            slat=row[3]
            uictype=row[11]
            InjDate=row[17]
            VolBBLS=row[21]
            VolMCF=row[22]
            injbot=row[27]
            formation=row[28]
        
            if api not in uniquewelllist:
                uniquewelllist.append(api)
    print("unique wells in spreadsheet = " + str(len(uniquewelllist)))


for welllistpos,well in enumerate(uniquewelllist):
    welldictionarylist.append({"api":well})
    monthdelta = ((currentyear-startyear)*12) + currentmonth
    monthcount = 0

    while monthcount < monthdelta:
        currentprocessingyear = int(startyear + (monthcount/12))
        currentprocessingmonth = ((monthcount+12)%12) + 1
        currentprocessingyearmonthstring =  str(currentprocessingmonth) + "/" + str(currentprocessingyear)
        welldictionarylist[welllistpos][str(currentprocessingyearmonthstring)+"_mcf"] = 0
        welldictionarylist[welllistpos][str(currentprocessingyearmonthstring)+"_bbls"] = 0
        monthcount += 1
 
    with open(config["inputcsvpath_sum_daily"],'r') as dailyPostPY:
        readfile=csv.reader(dailyPostPY)
        for i,row in enumerate(readfile):
            if i > 0:
                UIC=row[0]
                api=row[1]
                slon=row[2]
                slat=row[3]
                uictype=row[11]
                InjDate=row[17]
                VolBBLS=row[21]
                VolMCF=row[22]
                injbot=row[27]
                formation=row[28]
                
                welldictionarylist[welllistpos]["uictype"] = uictype           
                welldictionarylist[welllistpos]["formation"] = formation           
                welldictionarylist[welllistpos]["injbot"] = injbot           
                welldictionarylist[welllistpos]["slon"] = slon
                welldictionarylist[welllistpos]["slat"] = slat

                InjMonth = InjDate.split("/")[0] + "/" + InjDate.split("/")[2]

                if api == well:              
                #add MCF
                    for k,v in welldictionarylist[welllistpos].items():
                        if InjMonth == k.split("_")[0] and "_mcf" in k:
                            welldictionarylist[welllistpos][k] += float(VolMCF)            
                #add BBLS
                    for k,v in welldictionarylist[welllistpos].items():
                        if InjMonth == k.split("_")[0]and "_bbls" in k:
                            welldictionarylist[welllistpos][k] += float(VolBBLS)

    for k,v in welldictionarylist[welllistpos].items():
        if "_mcf" in k or "_bbls" in k:
            if int(v) > 0:
                print(k + ": " + str(v))

    print("\n\n\n")

def writeoutputcsv(unitofmeasurement):
      
    with open(config["outputcsvpath_sum_daily"]+unitofmeasurement+"_bypython.csv","w",newline="") as outputcsv:
        print("csv file created")
        outputcsvwriter = csv.writer(outputcsv)
        headerrowlist = ['api','uictype','formation','injbot','slon','slat']
        monthdelta = ((currentyear-startyear)*12) + currentmonth
        monthcount = 0

        while monthcount < monthdelta:
            currentprocessingyear = int(startyear + (monthcount/12))
            currentprocessingmonth = ((monthcount+12)%12) + 1
            currentprocessingyearmonthstring =  str(currentprocessingmonth) + "/" + str(currentprocessingyear)
            headerrowlist.append(currentprocessingyearmonthstring)
            monthcount += 1

        outputcsvwriter.writerow(headerrowlist)
        print("header row written")

        for welllistpos,well in enumerate(welldictionarylist):
            print("processing well id: " + str(well['api']))
            rowvalues = [well['api'], well['uictype'], well['formation'], well['injbot'], well['slon'], well['slat']]
            monthdelta = ((currentyear-startyear)*12) + currentmonth
            monthcount = 0

            while monthcount < monthdelta:
                currentprocessingyear = int(startyear + (monthcount/12))
                currentprocessingmonth = ((monthcount+12)%12) + 1
                currentprocessingyearmonthstring =  str(currentprocessingmonth) + "/" + str(currentprocessingyear)

                for k,v in well.items():
                    if k == currentprocessingyearmonthstring + "_" + unitofmeasurement:
                        rowvalues.append(v)
                monthcount += 1

            outputcsvwriter.writerow(rowvalues)

writeoutputcsv("mcf")
writeoutputcsv("bbls")