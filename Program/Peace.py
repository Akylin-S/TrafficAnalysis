import csv
import time
import datetime
import timedelta
import numpy as np
import os as os

#   This part is used to define some global variables
HEADERS = ["时间", "15min交通量", "15min上行外侧车道速度均值", "15min上行外侧车道速度标准差", "15min上行中间车道速度均值", 
            "15min上行中间车道速度标准差", "15min上行内侧车道速度均值", "15min上行内侧车道速度标准差", "15min下行内侧车道速度均值", "15min下行内侧车道速度标准差", 
            "15min下行中间车道速度均值", "15min下行中间车道速度标准差", "15min下行外侧车道速度均值", "15min下行外侧车道速度标准差", "15min上行速度均值", 
            "15min上行速度标准差", "15min下行速度均值", "15min下行速度标准差", "15min 上行大型车数量", "15min 上行中型车数量", 
            "15min 上行小型车数量", "15min 下行大型车数量", "15min 下行中型车数量", "15min 下行小型车数量", "分钟能见度m", 
            "降水天气现象", "气温℃", "湿度%RH", "瞬时风速m/s", "瞬时风向°", 
            "分钟内极大风速m/s", "分钟内极大风向°", "2 min平均风速m/s", "2 min平均风向°", "10 min平均风速m/s", 
            "10 min平均风向°", "气压hPa", "路面温度℃", "路面状况 ", "水膜厚度mm",
            "冰层厚度mm", "雪层厚度mm", "湿滑系数"]

FILE_PATH_TRAFFIC   = "E:/files/Traffic/"       #   specific the localation of csv file in the computer
FILE_PATH_WEATHER   = "E:/files/weather/"

FILE_PATH_SAVER     = "E:/files/Done/"          #   The Directory that is used to save the already dealed data 
SAVE_FILE_NAME      = ""
FORMATE_1           = "%H:%M:%S"                #   hours, mins, secs: used to transfer the data format of time
FORMATE_2           = "%Y-%m-%d"
FORMATE_3           = "%Y/%m/%d %H:%M:%S"
FORMATE_4           = "%H:%M"
SAVE_FORMONTH       = "%Y-%m"          #   Parts of csv file name, month part
SAVE_FORMATE        = "%Y-%m-%d %H:%M"
Index               = 1                         #   used to local the current row of the csv table
TimesOf15Mins       = 4*24                      #   the number of 15 mins in whole day
LastTimeStamp       = "10:00"                   #   used to specific the current row that need to compute
EndTimeStamp        = ""

TimeHeader          = ""

LittleCarMin    = 0.0
LittleCarMax    = 6.0
MiddleCarMin    = 6.0
MiddleCarMax    = 12.0
LargeCarMin     = 12.0
LargeCarMax     = 99.0

UpOuterRoad     = 6.8
UpMiddleRoad    = 10.6
UpInnerRoad     = 18.8
DownInnerRoad   = 18.8
DownMiddleRoad  = 22.6
DownOuterRoad   = 22.6


"""
------------------------------------------------------------------First Program-------------------------------------------------------------------
This is the first program that used to compute the traffic of each 15 mins in the whole day
--------------------------------------------------------------------------------------------------------------------------------------------------
"""
#   This function is used to open a file, the argument is FILE_PATH_TRAFFIC
def openFiles(path): 
    with open(file = path, mode="r", newline="", encoding="GBK") as file:
        csv_file = csv.reader(file)
        rows = [row for row in csv_file]
        return rows

#   This function is used to get the traffic in 15 mins
def getTrafficIn15Mins(weatherTimeFormat, trafficTimeFormat, Rows, endStamp):
    global Index
    global LastTimeStamp
    LastTimeStamp = datetime.datetime.strptime(LastTimeStamp, weatherTimeFormat)
    endTime = LastTimeStamp + timedelta.Timedelta(minutes=15)
    Total = 0
    Time = LastTimeStamp
    while Time <= endTime:
        tempTime = datetime.datetime.strptime(Rows[Index][0], trafficTimeFormat)
        tempTimeS = tempTime.strftime(weatherTimeFormat)
        Time = datetime.datetime.strptime(tempTimeS, weatherTimeFormat)
        if(Time < LastTimeStamp):
            Index = Index + 1
            continue
        Total = Total + 1
        if tempTime == endStamp: # TODO: to fix the end time
            break
        Index = Index + 1
    LastTimeStamp = endTime.strftime(weatherTimeFormat)
    return Total


#   This function is used to get all the traffic in the whole day
def getTotalTraffic(rows):
    global TimesOf15Mins
    # global FILE_PATH_TRAFFIC
    # path = FILE_PATH_TRAFFIC + "2019-07-01.csv"
    # rows = openFiles(path)
    endTime = datetime.datetime.strptime(rows[-1][0], FORMATE_1)
    print(endTime)
    print(len(rows))
    i = 1
    Total = [[], []]
    while i <= TimesOf15Mins:
        Total[0].append(TimeHeader + " " +  LastTimeStamp)
        print("第", i, "轮15分钟车流量：", getTrafficIn15Mins(FORMATE_4, FORMATE_1, rows, endTime), "   截止时间为：", LastTimeStamp)
        # Total[1].append(getTrafficIn15Mins(FORMATE_4, FORMATE_1, rows, endTime))
        # secondProgram = getTrafficIn15MinsByVehicleType(FORMATE_4, FORMATE_1, rows, endTime)
        i = i + 1
    return Total


"""
------------------------------------------------------------------Second Program-------------------------------------------------------------------
This is the second program that used to compute the traffic of each 15 mins in the whole day
---------------------------------------------------------------------------------------------------------------------------------------------------
"""
#   This function is used to get the traffic in 15 mins and divide into three parts according the given three vehicle type
def getTrafficIn15MinsByVehicleType(weatherTimeFormat, trafficTimeFormat, Rows, endStamp):
    global Index
    global LastTimeStamp
    LastTimeStamp = datetime.datetime.strptime(LastTimeStamp, weatherTimeFormat)
    endTime = LastTimeStamp + timedelta.Timedelta(minutes=15)
    Total = [0, 0, 0, 0]        # Little, Middle, Large, Total
    Time = LastTimeStamp
    while Time <= endTime:
        tempTime = datetime.datetime.strptime(Rows[Index][0], trafficTimeFormat)
        tempTimeS = tempTime.strftime(weatherTimeFormat)
        Time = datetime.datetime.strptime(tempTimeS, weatherTimeFormat)
        length = float(Rows[Index][2])
        if length < LittleCarMax :
            Total[0] = Total[0] + 1
        elif length < MiddleCarMax :
            Total[1] = Total[1] + 1
        else:
            Total[2] = Total[2] + 1 
        Index = Index + 1
        Total[3] = Total[3] + 1
        if tempTime == endStamp: # TODO: to fix the end time
            break
        Index = Index + 1
    LastTimeStamp = endTime.strftime(weatherTimeFormat)
    return Total


#   This function is used to ge all the traffic for each 15 mins in the whole day 
#   and the traffic of each 15 mins is divided into three parts according the given three vehicle type
def getTotalTrafficByVehicleType(rows):
    global TimesOf15Mins
    # rows = openFiles(path)
    endTime = datetime.datetime.strptime(rows[-1][0], FORMATE_1)
    print(endTime)
    print(len(rows))
    i = 1
    while i <= TimesOf15Mins:
        Total = getTrafficIn15MinsByVehicleType(FORMATE_4, FORMATE_1, rows, endTime)
        print("第", i, "轮15分钟车流量：", Total[3], "   截止时间为：", LastTimeStamp)
        print("小型车辆数： ", Total[0], "----中型车辆数： ", Total[1], "----大型车辆数： ", Total[2])
        print("-------------------------------------------------------------------------------------")
        i = i + 1


"""
------------------------------------------------------------------Third Program-------------------------------------------------------------------
This is the third program that used to compute the Mean of Speed, Stander Difference
---------------------------------------------------------------------------------------------------------------------------------------------------
"""
#   This function is used to get the Speed Mean and Speed Stander Difference of different road types in one 15 mins
def getTheMeanAndStanDiffOfRodeIn15Mins(weatherTimeFormat, trafficTimeFormat, Rows, endStamp):
    global Index
    global LastTimeStamp
    LastTimeStamp = datetime.datetime.strptime(LastTimeStamp, weatherTimeFormat)
    endTime = LastTimeStamp + timedelta.Timedelta(minutes=15)
    upStream = [0, 0, 0, 0]             # Total, Inner, Middle, Outer
    downStream = [0, 0, 0, 0]           # Total, Inner, Middle, Outer
    upNumber = [0, 0, 0, 0]             # Total, Inner, Middle, Outer
    downNumber = [0, 0, 0, 0]           # Total, Inner, Middle, Outer
    upStreamVehicle = [0, 0, 0]         # Little, Middle, Large
    downStreamVehicle = [0, 0, 0]       # Little, Middle, Large
    upOrigin = [[], [], [], []]             # save the Orginal Speed from CSV file and parts by Different upRoad: inner, Middle, Outer, Total
    downOrigin = [[], [], [], []]           # save the Orginal Speed from CSV file and parts by Different downRoad: inner, Middle, Outer, Total

    Time = LastTimeStamp
    TotalTraffic = 0

    while Time <= endTime:
        if Index == len(Rows):
            break
        tempTime = datetime.datetime.strptime(Rows[Index][0], trafficTimeFormat)
        tempTimeS = tempTime.strftime(weatherTimeFormat)
        Time = datetime.datetime.strptime(tempTimeS, weatherTimeFormat)
        length = float(Rows[Index][2])
        yPoint = float(Rows[Index][4])
        xSpeed = float(Rows[Index][5])
        if xSpeed > 0:
            upOrigin[3].append(float(Rows[Index][5]))
            #   Compute the Speed and the Number of UpStream Vehicle
            if yPoint < UpOuterRoad :
                upStream[3] = upStream[3] + float(float(Rows[Index][5]))
                upNumber[3] = upNumber[3] + 1
                upOrigin[2].append(float(float(Rows[Index][5])))
            elif yPoint < UpMiddleRoad :
                upStream[2] = upStream[2] + float(float(Rows[Index][5]))
                upNumber[2] = upNumber[2] + 1
                upOrigin[1].append(float(Rows[Index][5]))
            elif yPoint < UpInnerRoad :
                upStream[1] = upStream[1] + float(Rows[Index][5])
                upNumber[1] = upNumber[1] + 1 
                upOrigin[0].append(float(Rows[Index][5]))
            #   Compute the Number of different Vehicle which run in the UpStream
            if length < LittleCarMax :
                upStreamVehicle[0] = upStreamVehicle[0] + 1
            elif length < MiddleCarMax :
                upStreamVehicle[1] = upStreamVehicle[1] + 1
            else:
                upStreamVehicle[2] = upStreamVehicle[2] + 1 
            
        else:
            downOrigin[3].append(float(Rows[Index][5]))
            #   Compute the Speed and the Number of DownStream Vehicle
            if yPoint >= DownOuterRoad :
                downStream[3] = downStream[3] + float(Rows[Index][5])
                downNumber[3] = downNumber[3] + 1
                downOrigin[2].append(float(Rows[Index][5]))
            elif yPoint < DownMiddleRoad :
                downStream[2] = downStream[2] + float(Rows[Index][5])
                downNumber[2] = downNumber[2] + 1
                downOrigin[1].append(float(Rows[Index][5]))
            elif yPoint < DownInnerRoad :
                downStream[1] = downStream[1] + float(Rows[Index][5])
                downNumber[1] = downNumber[1] + 1
                downOrigin[0].append(float(Rows[Index][5]))
            #   Compute the Number of different Vehicle which run in the DownStream
            if length < LittleCarMax :
                downStreamVehicle[0] = downStreamVehicle[0] + 1
            elif length < MiddleCarMax :
                downStreamVehicle[1] = downStreamVehicle[1] + 1
            else:
                downStreamVehicle[2] = downStreamVehicle[2] + 1 
        TotalTraffic = TotalTraffic + 1
        Index = Index + 1
        if tempTime == endStamp: # TODO: to fix the end time
            break

    Total = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]                              # upTotalMean, upIneerMean, upIneerStanDiff, upMiddleMean, upMiddleStanDiff, upOuterMean, upOuterStanDiff, 
                                                                                                            # downTotalMean, downInnerMean, downStanDiff, downMiddleMean, downMiddleStanDiff, downOuterMean, downOuterStanDiff
                                                                                                            # upLittle, upMiddle, upLarge, downLittle, downMiddle, downLarge
    upNumber[0] = upNumber[1] + upNumber[2] +upNumber[3]                                                    # The total number of upStream Vehicles
    downNumber[0] = downNumber[1] + downNumber[2] + downNumber[3]                                           # The total number of downStream Vehicles


    Total[0][0] = TotalTraffic
    
    #   Compute the Mean of UpStream, parts by three kind of road which are inner, middle, outer 
    Total[0][1] = np.mean(upOrigin[0])                                                                      # Inner
    Total[0][3] = np.mean(upOrigin[1])                                                                      # Middle
    Total[0][5] = np.mean(upOrigin[2])                                                                      # Outer
    Total[0][7] = np.mean(upOrigin[3])                                                                      # Total 
    #   Compute the Stander Difference of UpStream, parts by three kind of road which are inner, middle, outer 
    Total[0][2] = np.std(upOrigin[0])                                                                       # Inner
    Total[0][4] = np.std(upOrigin[1])                                                                       # Middle
    Total[0][6] = np.std(upOrigin[2])                                                                       # Outer
    Total[0][8] = np.std(upOrigin[3])                                                                       # Outer

    #   Compute the Mean of DownStream, parts by three kind of road which are inner, middle, outer 
    Total[1][1] = np.mean(downOrigin[0])                                                                    # Inner
    Total[1][3] = np.mean(downOrigin[1])                                                                    # Middle
    Total[1][5] = np.mean(downOrigin[2])                                                                    # Outer
    Total[1][7] = np.mean(downOrigin[3])                                                                    # Outer
    #   Compute the Stander Difference of DownStream, parts by three kind of road which are inner, middle, outer 
    Total[1][2] = np.std(downOrigin[0])                                                                     # Inner
    Total[1][4] = np.std(downOrigin[1])                                                                     # Middle
    Total[1][6] = np.std(downOrigin[2])                                                                     # Outer
    Total[1][8] = np.std(downOrigin[3])                                                                     # Outer


    #   Save the Traffic of UpStream from array upStreamVehicle to array Total, parts by different types
    Total[2][0] = upStreamVehicle[0]                                                                        # Little
    Total[2][1] = upStreamVehicle[1]                                                                        # Middle
    Total[2][2] = upStreamVehicle[2]                                                                        # Large
    #   Save the Traffic of DownStream from array upStreamVehicle to array Total, parts by different types
    Total[2][3] = downStreamVehicle[0]                                                                      # Little
    Total[2][4] = downStreamVehicle[1]                                                                      # Middle
    Total[2][5] = downStreamVehicle[2]                                                                      # Large


    # print("上行内侧车道速度为：", upOrigin[0])
    # print("上行中间车道速度为：", upOrigin[1])
    # print("上行外侧车道速度为：", upOrigin[2])

    # print("上行内侧车道速度为：", downOrigin[0])
    # print("上行中间车道速度为：", downOrigin[1])
    # print("上行外侧车道速度为：", downOrigin[2])

    LastTimeStamp = endTime.strftime(weatherTimeFormat)
    return Total

#   This function is used to get the Speed Mean and Stander Difference of each 15 mins, by call the getTheMeanAndStanDiffOfRodeIn15Mins(FORMATE_1, rows) function
def getTotalMeanAndStandDiffOfRoadIn15Mins(rows):
    global TimesOf15Mins
    endTime = datetime.datetime.strptime(rows[-1][0], FORMATE_1)
    # print(endTime)
    # print(len(rows))
    # print(len(rows))
    i = 1
    Total1 = [[], [], [], [], [],   [], [], [], [], [],    [], [], [], [], [],    [], [], [], [], [],   [], [], [], []]
    while i <= (TimesOf15Mins +1):
        Total = getTheMeanAndStanDiffOfRodeIn15Mins(FORMATE_4, FORMATE_1, rows, endTime)
        Total1[0].append(TimeHeader + " " +  LastTimeStamp)
        Total1[1].append(Total[0][0])
        Total1[2].append(Total[0][5])
        Total1[3].append(Total[0][6])
        Total1[4].append(Total[0][3])
        Total1[5].append(Total[0][4])
        Total1[6].append(Total[0][1])
        Total1[7].append(Total[0][2])

        Total1[8].append(Total[1][5])
        Total1[9].append(Total[1][6])
        Total1[10].append(Total[1][3])
        Total1[11].append(Total[1][4])
        Total1[12].append(Total[1][1])
        Total1[13].append(Total[1][2])

        Total1[14].append(Total[0][7])
        Total1[15].append(Total[0][8])

        Total1[16].append(Total[1][7])
        Total1[17].append(Total[1][8])

        Total1[18].append(Total[2][2])
        Total1[19].append(Total[2][1])
        Total1[20].append(Total[2][0])

        Total1[21].append(Total[2][5])
        Total1[22].append(Total[2][4])
        Total1[23].append(Total[2][3])
        # print("----------------------------------------------------------------------------------------------------------------------------------")
        # print("第 ", i, "轮15分钟的---上行---车道的平均速度为：", Total[0][7], "  标准差为：  ", Total[0][8], " 上行内侧车道平均速度为： ", Total[0][1], " 标准差为： ", Total[0][2], " 中间车道平均速度： ", Total[0][3], 
        #     "标准差为：", Total[0][4], "外侧车道平均速度： ", Total[0][5], "标准差为：", Total[0][6] )
        # print("第 ", i, "轮15分钟的---下行---车道的平均速度为：", Total[1][7] , "  标准差为：  ", Total[1][8], " 下行内侧车道平均速度为： ", Total[1][1], " 标准差为： ", Total[1][2], " 中间车道平均速度： ", Total[1][3], 
        #     "标准差为：", Total[1][4], "外侧车道平均速度： ", Total[1][5], "标准差为：", Total[1][6] )
        # print("第 ", i, "轮15分钟的---上行---车道的小车数量为：", Total[2][0], "中车数量为：", Total[2][1], "大车数量为：", Total[2][2])
        # print("第 ", i, "轮15分钟的---下行---车道的小车数量为：", Total[2][3], "中车数量为：", Total[2][4], "大车数量为：", Total[2][5])
        i = i + 1
    return Total1

"""
------------------------------------------------------------------Forth Program-------------------------------------------------------------------
This is the Forth program that used to compute the Mean of the CSV file
---------------------------------------------------------------------------------------------------------------------------------------------------
"""
def openFilesWeather(path):
    with open(file = path, mode="r", newline="", encoding="gbk") as file:
        csv_file = csv.reader(file)
        rows = [row for row in csv_file]
        return rows

def getAllTheMeanOfWeather(path):
    rowsWeather = openFilesWeather(path)
    Total = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    i = 1
    while i < len(rowsWeather):
        # print(rowsWeather)
        Total[1].append(float(rowsWeather[i][1]))
        Total[2].append(float(rowsWeather[i][2]))
        Total[3].append(float(rowsWeather[i][3]))
        Total[4].append(float(rowsWeather[i][4]))
        Total[5].append(float(rowsWeather[i][5]))
        Total[6].append(float(rowsWeather[i][6]))
        Total[7].append(float(rowsWeather[i][7]))
        Total[8].append(float(rowsWeather[i][8]))
        Total[9].append(float(rowsWeather[i][9]))
        Total[10].append(float(rowsWeather[i][10]))
        Total[11].append(float(rowsWeather[i][11]))
        Total[12].append(float(rowsWeather[i][12]))
        Total[13].append(float(rowsWeather[i][13]))
        Total[14].append(float(rowsWeather[i][14]))
        Total[15].append(float(rowsWeather[i][15]))
        Total[16].append(float(rowsWeather[i][16]))
        Total[17].append(float(rowsWeather[i][17]))
        Total[18].append(float(rowsWeather[i][18]))
        Total[19].append(float(rowsWeather[i][19]))
        i = i + 1
    i = 1
    while i < 20:
        print("第 ", i, " 列平均值为： ", np.mean(Total[i]))
        i = i + 1

"""
------------------------------------------------------------------Fifth Program--------------------------------------------------------------------
This is the Fifth program that used to compute the Mean of the CSV file
---------------------------------------------------------------------------------------------------------------------------------------------------
"""
#   This function is used to get all the files name which in weather and traffic directory
def getAlltheFilesName(trafficFilePath, weatherFilePath):
    FilesName = [[], []]
    trafFilesName = os.listdir(trafficFilePath)
    weatFilesName = os.listdir(weatherFilePath)
    i = 0
    while i < len(trafFilesName):
        FilesName[0].append(trafFilesName[i])
        i = i + 1

    j = 0
    while j < len(weatFilesName):
        FilesName[1].append(weatFilesName[j])
        j = j + 1
    print('Traffic目录下的文件名都为：', FilesName[0][1])
    print('Weather目录下的文件名都为：', FilesName[1][1])
    getRowsIn15Mins(FilesName)
    return FilesName

# Used to get the mean in 15 mins, 
def getWeatherIn15Mins(weatherTimeFormat, Rows, endStamp):
    global Index
    global LastTimeStamp
    LastTimeStamp = datetime.datetime.strptime(LastTimeStamp, weatherTimeFormat)
    endTime = LastTimeStamp + timedelta.Timedelta(minutes=15)
    Total15 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    Total1 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    Time = LastTimeStamp
    while Time <= endTime:
        temp = datetime.datetime.strptime(Rows[Index][0], FORMATE_3)
        tempS = temp.strftime(weatherTimeFormat)
        Time = datetime.datetime.strptime(tempS, weatherTimeFormat)
        
        Total15[1].append(float(Rows[Index][1]))
        Total15[2].append(float(Rows[Index][2]))
        Total15[3].append(float(Rows[Index][3]))
        Total15[4].append(float(Rows[Index][4]))
        Total15[5].append(float(Rows[Index][5]))

        Total15[6].append(float(Rows[Index][6]))
        Total15[7].append(float(Rows[Index][7]))
        Total15[8].append(float(Rows[Index][8]))
        Total15[9].append(float(Rows[Index][9]))
        Total15[10].append(float(Rows[Index][10]))

        Total15[11].append(float(Rows[Index][11]))
        Total15[12].append(float(Rows[Index][12]))
        Total15[13].append(float(Rows[Index][13]))
        Total15[14].append(float(Rows[Index][14]))
        Total15[15].append(float(Rows[Index][15]))

        Total15[16].append(float(Rows[Index][16]))
        Total15[17].append(float(Rows[Index][17]))
        Total15[18].append(float(Rows[Index][18]))
        Total15[19].append(float(Rows[Index][19]))
        if Time == endStamp: # TODO: to fix the end time
            break
        Index = Index + 1

    i = 1
    while i < 20:
        if (i == 2 or i == 15) :
            Total1[i].append(np.max(Total15[i]))
            i = i +1 
            continue
        Total1[i].append(np.mean(Total15[i]))
        i = i+1
    LastTimeStamp = endTime.strftime(weatherTimeFormat)
    return Total1

# Get the total dealed weather data of one day
def getTotalWeather(rows):
    global TimesOf15Mins
    # global FILE_PATH_TRAFFIC
    # path = FILE_PATH_TRAFFIC + "2019-07-01.csv"
    # rows = openFiles(path)
    endTime = datetime.datetime.strptime(rows[-1][0], FORMATE_3)
    temp = endTime.strftime(FORMATE_4)
    endTime = datetime.datetime.strptime(temp, FORMATE_4)
    # print(endTime)
    # print(len(rows))
    i = 1
    Totals = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    while i <= (TimesOf15Mins + 1):
        Total = getWeatherIn15Mins(FORMATE_4, rows, endTime)
        Totals[0].append(TimeHeader + " " +  LastTimeStamp)
        j = 1
        while j < 20:
            Totals[j].append(Total[j])   
            j = j + 1       
        i = i + 1
    return Totals

#   Used to creat a new file according to different month. Name format: Date-xxxx/xx-createTime-xxxx-xx-xx-xx-xx-xx
def createNewCSVFile(dateMonth):
    global HEADERS
    global SAVE_FILE_NAME
    global FILE_PATH_SAVER
    now = datetime.datetime.now()
    nowString = now.strftime("%Y-%m-%d-%H-%M-%S")
    SAVE_FILE_NAME = FILE_PATH_SAVER + "Date-"+dateMonth + "-createTime-" + nowString + ".csv"
    with open(file= SAVE_FILE_NAME, mode="w", newline="", encoding="GBK") as file:
        csv_file = csv.writer(file)
        csv_file.writerow(HEADERS)


#   This function is used to save the data that in 15 mins, the saving file is SAVE_FILE_NAME 
def saveDataToFile(rowsIn15Mins):
    with open(file = SAVE_FILE_NAME, mode="a", newline="", encoding="GBK") as file:
        csv_file = csv.writer(file)
        csv_file.writerows(rowsIn15Mins)

#   To set Global Varables: LastTimeStamp, TimeHeader, TimesOf15Mins
def setGlobalVairables(weatherRowsInOneDay, indexDatesInOneWeatherFile, FORMATE):
    weatherDateTimeTypeS = datetime.datetime.strptime(weatherRowsInOneDay[indexDatesInOneWeatherFile][0], FORMATE)        # get the weather-one-day-rows starting time
    weatherDateTimeTypeE = datetime.datetime.strptime(weatherRowsInOneDay[-1][0], FORMATE)                                # get the weather-one-day-rows ending time 
    weatherStartTimeTypeS = weatherDateTimeTypeS.strftime(FORMATE_4)                                                        # start time: String type, format: "00:00"
    weatherStartTimeTypeE = datetime.datetime.strptime(weatherStartTimeTypeS, FORMATE_4)                                    # start time : Time type, format: 00:00
    secDiffStart = (weatherStartTimeTypeE - datetime.datetime.strptime("00:00", FORMATE_4)).seconds                         # seconds that between 00:00:00 to weatherStartTimeTypeE
    numOf15MinStart = int(secDiffStart / (60*15))
    HoursStart = int(numOf15MinStart / 4)                                                                                   # used to get the start Hour
    MinsStart  = int(numOf15MinStart % 4) * 15                                                                              # used to get the start Mins
    tempTimeChange = datetime.datetime(year=1900, month=1, day=1, hour=HoursStart, minute=MinsStart, second=0)
    global LastTimeStamp
    LastTimeStamp = tempTimeChange.strftime(FORMATE_4)
    global TimeHeader
    if(weatherDateTimeTypeS.strftime(FORMATE_2) != '1900-01-01'):
        TimeHeader = weatherDateTimeTypeS.strftime(FORMATE_2)                                                                   # give a year-month-day
    secondDiff = (weatherDateTimeTypeE - weatherDateTimeTypeS).seconds                                                      # get the seconds betweent starting time and ending time 
    NumOf15Mins = int(secondDiff / (60*15))                                                                                 # get the number of circulations of execute(15 mins each execute)
    global TimesOf15Mins 
    TimesOf15Mins = NumOf15Mins

#   Used to get the final SavaDates
def getFinalDates(weatherRows, trafficRows, FORMATE):
    weatherLen = len(weatherRows[0])
    trafficLen = len(trafficRows[0])
    wIndex = 0
    writeDates = [[], [], [], [], [],   [], [], [], [], [],    [], [], [], [], [],   [], [], [], [], [],   [], [], [], [], [],   [], [], [], [], [],   [], [], [], [], [],   [], [], [], [], [],   [], [], []]
    while wIndex < weatherLen:
        tIndex = 0
        dateWeather = datetime.datetime.strptime(weatherRows[0][wIndex], FORMATE)
        while tIndex < trafficLen:
            if trafficRows[0][tIndex] not in weatherRows[0]:
                tIndex = tIndex + 1
                continue
            dateTraf = datetime.datetime.strptime(trafficRows[0][tIndex], FORMATE)
            # test
            if trafficRows[0][tIndex] == '2019-09-25 00:15':
                i=1
            while dateTraf > dateWeather:
                if wIndex == weatherLen:
                    break
                wIndex = wIndex + 1
                if wIndex == weatherLen:
                    break
                dateWeather = datetime.datetime.strptime(weatherRows[0][wIndex], FORMATE)

            if (dateTraf == dateWeather):
                i = 0
                while i < 24:
                    j = i + 24
                    writeDates[i].append(trafficRows[i][tIndex])
                    if j < 43:
                        writeDates[j].append(weatherRows[i + 1][wIndex])
                    i = i + 1
                wIndex = wIndex + 1
                if wIndex == weatherLen:
                    break
                dateWeather = datetime.datetime.strptime(weatherRows[0][wIndex], FORMATE)
            tIndex = tIndex + 1
        if wIndex == weatherLen:
            break
        wIndex = wIndex + 1
    writeDatesFinal = list(map(list, zip(*writeDates)))
    return writeDatesFinal

#   This function is used to 
def getRowsIn15Mins(fileNames):
    global FILE_PATH_TRAFFIC                                                        # the directory that includes all the traffic files
    global FILE_PATH_WEATHER                                                        # the directory that includes all the weather files
    numOfTrafficFiles = len(fileNames[0])                                           # num of traffic files 
    numOfWeatherFiles = len(fileNames[1])                                           # num of weather files

    dateMonth = ""                                                                  # used to save the date data for current month csv file               
    weatherIndex = 0                                                                # indicate the next weather file that waiting read
    #   used to save the finial data
    while weatherIndex < numOfWeatherFiles:
        

        weatherFileName = FILE_PATH_WEATHER + fileNames[1][weatherIndex]            # weather file path, used to open the file, get rows 
        # print(weatherFileName)
        weatherRows = openFiles(weatherFileName)                                    # all the rows in a weather file

        replaceIndex = 1
        if  "-" in weatherRows[1][0]:
            while replaceIndex < len(weatherRows):  
                temp = weatherRows[replaceIndex][0].replace('-', '/')
                weatherRows[replaceIndex][0] = temp
                # print(weatherRows[replaceIndex][0])
                replaceIndex = replaceIndex + 1
        # print(weatherRows[1][0])

        dateMonthTemp = datetime.datetime.strptime(weatherRows[1][0] , FORMATE_3)
        dateMonth = dateMonthTemp.strftime(SAVE_FORMONTH) 
        createNewCSVFile(dateMonth)                                                 # Create a new csv file for this month according this month weather file. 

        indexDate = datetime.datetime.strptime(weatherRows[1][0], FORMATE_3)        # Time object
        TraffDateType = datetime.datetime.strftime(indexDate, FORMATE_2)            # string type: 2020-xx-xx

        weatherDates = []                                                           # used to save all the files name of traffic
        indexDatesInOneWeatherFile = 1                                              # used to indicate the next row in arry weather rows
        weatherTempDate = ""                                                        # used to save the name of last time stamp, format: 2020-xx-xx
        weatherDayIndex = []                                                        # used to save the index in weatherRows when the day changed
        # print(len(weatherRows))
        while indexDatesInOneWeatherFile < len(weatherRows):        
            # tempS      = weatherRows[indexDatesInOneWeatherFile][0]                                                 # Used to deal the time with "2020-xx-xx" type
            # tempS.replace("-", "/")
            timeObject = datetime.datetime.strptime(weatherRows[indexDatesInOneWeatherFile][0], FORMATE_3)          # change the date type from string to time, saveed in a new variable
            indexDatesInOneWeatherFile = indexDatesInOneWeatherFile +1
            stringType = datetime.datetime.strftime(timeObject, FORMATE_2)                                          # change the date type from time to string and change the time format: 2020-xx-xx
            if(stringType != weatherTempDate):
                weatherDayIndex.append(indexDatesInOneWeatherFile)
                weatherTempDate = stringType
                saveType = stringType + ".csv"                                      # with .csv, in order to handly compare with traffic file, its file name format is 2020-xx-xx.csv
                weatherDates.append(saveType)

        indexDatesInOneWeatherFile = 0                                              # Before this "while" circulation, reset the index
        trafficIndex = 0                                                            # indicate the next traffic file that waiting read
        while trafficIndex < numOfTrafficFiles:
            indexOnDay = 0
            if fileNames[0][trafficIndex] not in weatherDates:
                trafficIndex = trafficIndex + 1 
                continue
            trafficFileName = FILE_PATH_TRAFFIC + fileNames[0][trafficIndex]
            # trafficRows = openFiles(trafficFileName)
            indexOnDay = weatherDates.index(fileNames[0][trafficIndex])
            weatherDayIndexLength = len(weatherDayIndex) - 1
            weatherRowsInOneDay = weatherRows[weatherDayIndex[indexOnDay]-1:]                                                       # prevent to became a local variable(only worked in If block)
            if(indexOnDay == weatherDayIndexLength):
                weatherRowsInOneDay = weatherRows[weatherDayIndex[indexOnDay]-1:]                                                   # get the weather rows that in one day 
            else:
                weatherRowsInOneDay = weatherRows[weatherDayIndex[indexOnDay]-1: weatherDayIndex[indexOnDay + 1]-1]                 # get the weather rows that in one day 


            setGlobalVairables(weatherRowsInOneDay, indexDatesInOneWeatherFile, FORMATE_3)
            global Index
            Index = 0
            weatherOneDayDates = getTotalWeather(weatherRowsInOneDay)     

            indexDatesInOneTrafficFile = 1
            trafficRowsOneDay = openFiles(trafficFileName)
            setGlobalVairables (trafficRowsOneDay, indexDatesInOneTrafficFile, FORMATE_1)
            Index = 1 
            # trafficOneDayDates = getTotalTraffic(trafficRowsOneDay)
            trafficOneDayDates = getTotalMeanAndStandDiffOfRoadIn15Mins(trafficRowsOneDay)
            saverRows = getFinalDates(weatherOneDayDates, trafficOneDayDates, SAVE_FORMATE)                                         # get the rows of one day
            saveDataToFile(saverRows)                                                                                               # add thoes rows to current month CSV file

            indexOnDay = indexOnDay + 1 
            trafficIndex = trafficIndex + 1 




            
        weatherIndex = weatherIndex + 1 





def main():
    # getTotalTraffic(FILE_PATH_TRAFFIC)
    # getTotalTrafficByVehicleType(FILE_PATH_TRAFFIC)
    # getTotalMeanAndStandDiffOfRoadIn15Mins(FILE_PATH_TRAFFIC)
    # getAllTheMeanOfWeather(FILE_PATH_TRAFFIC)
    # getAlltheFilesName(FILE_PATH_TRAFFIC, FILE_PATH_WEATHER)global FILE_PATH_TRAFFIC
    # NumOf15Mins= 7
    # Hours = int(NumOf15Mins/4)
    # Mins  = int(NumOf15Mins%4) * 15
    # global LastTimeStamp
    # LastTimeStamp = datetime.datetime(year = 1900, month = 1, day = 1,hour=Hours, minute=Mins, second=0)
    # print(LastTimeStamp)
    getAlltheFilesName(FILE_PATH_TRAFFIC, FILE_PATH_WEATHER)
    print(os.listdir(FILE_PATH_SAVER))
    a = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    
    b =  list(map(list, zip(*a)))
    print(b)


if __name__ == "__main__":
    main()