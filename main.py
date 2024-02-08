import os
import pandas as pd
import pghbustime
from tkinter import *
from colour import Color
import meteostat
from datetime import datetime
from datetime import timedelta
import pandas as pd
import sys
import time
import requests
from randfacts import get_fact
from PIL import Image, ImageTk
import PIL.Image

def busFunction(stpid, maxpredictions):
    mykey = "ZdGwvXBCdzSuhSw4rLyL3fJ6g"

    api = pghbustime.BustimeAPI(mykey, _format="xml")
    info = api.predictions(stpid=stpid, maxpredictions=maxpredictions)#make list

    all_bus_dict = {}
    given_string = str(info).replace("\\r", "").replace("\\n", "").replace("\\t", "")
    for j in range(1,6):
        each_bus_dict = {}
        for i in ["stpnm", "rt", "prdtm"]:

            start_string = "<" + i +">"
            end_string = "</"+ i +">"

            start_index = given_string.find(start_string) + len(start_string)
            end_index = given_string.find(end_string)
            if i == "stpnm" and given_string[start_index:end_index][0] != "F":
                break
            else:
                each_bus_dict[i] =given_string[start_index:end_index]
        all_bus_dict[j] = each_bus_dict

        start_string_remove = "<prd>"
        end_string_remove = "</prd>"
        start_index = given_string.find(start_string_remove) + len(start_string_remove)
        end_index = given_string.find(end_string_remove)
        given_string = given_string.replace(given_string[start_index-5:end_index+6],"")

    '''
                    `tmstp`: when prediction was generated
                    `typ`: prediction type ('A' = arrival, 'D' = departure)
                    `stpid`: stop ID for prediction
                    `stpnm`: stop name for prediction
                    `vid`: vehicle ID for prediction
                    `dstp`: vehicle distance to stop (feet)
                    `rt`: bus route
                    `des`: bus destination
                    `prdtm`: ETA/ETD
                    `dly`: True if bus delayed
                    `tablockid`, `tatripid`, `zone`: internal, see `self.vehicles`
    '''

    return all_bus_dict

def getDate():
    text = datetime.today().strftime("%A, %B %d, %Y")
    dateLabel.config(text= text)
    dateLabel.after(1000*60*5,getDate)

def getTime():
    timeLabel.config(text=datetime.today().strftime("%H:%M:%S"))
    timeLabel.after(100,getTime)

def getWeather():
   try:
    # Set time period
    start = datetime.today()-timedelta(hours = 1)
    end = datetime.today()
    # Get hourly data
    data = meteostat.Hourly(meteostat.Point(40.440624, -79.995888, 100), start, end, model="False")
    data = data.fetch()
    pd.set_option('display.max_columns', None)
    # Print DataFrame

    weather_dict = {1:'Clear',2:'Fair',3:'Cloudy',4:'Overcast',5:'Fog',6:'Freezing Fog',7:'Light Rain',8:'Rain',9:'Heavy Rain',10:'Freezing Rain',11:'Heavy Freezing Rain',12:'Sleet',13:'Heavy Sleet',14:'Light Snowfall',15:'Snowfall',16:'Heavy Snowfall',17:'Rain Shower',18:'Heavy Rain Shower',19:'Sleet Shower',
20:'Heavy Sleet Shower',21:'Snow Shower',22:'Heavy Snow Shower',
23:'Lightning',24:'Hail',25:'Thunderstorm',26:'Heavy Thunderstorm',
27:'Storm'}

    weatherLabel.config(text= str(int(data["temp"]))+chr(176) +"C" +" / "+ str(int(float(data["temp"])*1.8 + 32))+ chr(176) + "F" + " "+ weather_dict[int(data["coco"])])
    weatherLabel.after(1000,getWeather)
   except:
       print("Error, Trying again")
       weatherLabel.after(1000,getWeather)


def getBus1(keyBus):
    bus_data = {27: "Forbes + Coltart"}
    try:
        testtime = datetime.now().hour

        busDict = busFunction(keyBus, 5)

        busText = ""
        if busDict == {}:
            busLabel1.config(text = "No busses atm")
            busLabel1.after(20*1000,getBus1, keyBus)
        for key in busDict:
            if busDict[key] == {}:
                continue
            busText += busDict[key]['rt'] + " - "
            if (datetime.strptime(busDict[key]["prdtm"],'%Y%m%d %H:%M:%S') -datetime.now()).total_seconds() /60 < 2:
                busText += "Now\n "
            else:
                busText += datetime.strptime(busDict[key]["prdtm"],'%Y%m%d %H:%M:%S').strftime('%H:%M:%S') + " (" + str(int((datetime.strptime(busDict[key]["prdtm"],'%Y%m%d %H:%M:%S') -datetime.now()).total_seconds() //60)) + "m) " +"\n"
        if keyBus == 27:
            busLabel1.config(text = busText[0:len(busText)-2])
            busLabel1.after(20*1000,getBus1, keyBus) #20s
    except:
        print("try again")
        busLabel1.after(20*1000,getBus1, keyBus)


def change(delay, frame, sequence, index):
    index = (index + 1) % len(sequence)
    frame.configure(background=sequence[index])
    if datetime.now().minute == 0 and datetime.now().second == 0:
        frame.after(1, lambda: change(1, frame, sequence, index))
    else:
        frame.after(100, lambda: change(100, frame, sequence, index))


sequence = []
lowest = 200
value = 255-lowest
for i in range(0,value):
    sequence.append('#%02x%02x%02x' % (255-i, i+lowest, 0+lowest))
for i in range(0,value):
    sequence.append('#%02x%02x%02x' % (0+lowest, 255-i, i+lowest))
for i in range(0,value):
    sequence.append('#%02x%02x%02x' % (i+lowest, 0+lowest, 255-i))
##################################


if __name__ == "__main__":
    #Import the tkinter library

    #Create an instance of the canvas
    win = Tk()
    frame = Frame(win, background = "#000000", height =300, width = 500, highlightbackground="black", highlightthickness=5)
    frame.grid(row=0, column = 0)
    #ewin.attributes('-fullscreen',True)

    #Select the title of the window
    win.title("Screensaver")

    #Define the geometry of the window
    win.geometry("950x1080")

    win['bg']='black'

    #Creating the label with text property of the clock
    dateLabel= Label(frame,text= "",font=("Bahnschrift", 30), fg= "black", justify = CENTER, bd = 2, bg = 'white', relief = "groove", padx = 100, pady = 0, height=1)
    dateLabel.grid(row=0, column=0, columnspan=8, sticky= W+E+N+S)

    timeLabel= Label(frame,text= "",font=("Verdana", 70, 'bold'), fg= "white", bg = "black", justify = CENTER, bd = 2,  relief = "groove", padx = 0, pady = 0, height=1)
    timeLabel.grid(row=1, column=0, columnspan=8, sticky= W+E+N+S)

    weatherLabel= Label(frame, text= "", font=("Bahnschrift",30), fg= "black", justify = RIGHT, bd = 2, bg = 'white', relief = "groove", padx = 0, pady = 0, width=35, height=1)
    weatherLabel.grid(row=2, column=0, columnspan=8, sticky= W+E+N+S)

    busTitle = Label(frame, text = "Bus Times for Forbes and Halket (assume 5m to get down)", font=("Bahnschrift",25, 'underline'), fg= "black", justify = CENTER, bd = 2, bg = 'light blue', relief = "groove", padx = 15, pady = 15,  anchor = N, height=1)
    busTitle.grid(row=3, column=0, columnspan=8, sticky= W+E+N+S)

    busLabel1= Label(frame, text= "", font=("Bahnschrift",40) , fg= "black", justify = CENTER, bd = 2, bg = 'light blue', relief = "groove", padx = 15, pady = 15, wraplength = 700,  height=5)
    busLabel1.grid(row=4, column=0, columnspan=8, sticky= W+E+N+S)




    # picLabel= Label(frame, image = ph, wraplength = 500, height=4, fg= "white", justify = LEFT, bd = 2, bg = 'white', relief = "groove", padx = 15, pady = 2)
    # picLabel.image = PhotoImage(file='important_image.png')
    # picLabel.grid(row=6, column=4, columnspan=1, sticky= N+E+S+W)

    #variable2 = StringVar(frame)
    #variable2.set("Choose Bus Stop")
    #choose_test = OptionMenu(frame, variable2, *list((f'{key:04}' + " - " + bus_data[key]) for key in bus_data),command = getBus2)
    #choose_test.config(font=("arial", 20)) # set the button font

    #menu = frame.nametowidget(choose_test.menuname)  # Get menu widget.
    #menu.config(font=("arial", 20))  # Set the dropdown menu's font
    #choose_test.grid(row=4, column=1, sticky='nsew')

    win.grid_columnconfigure(0, weight=3)
    win.grid_rowconfigure(0, weight=3)

    #Calling the functions
    print("date")
    getDate()
    print("time")
    getTime()
    print("weather")
    getWeather()
    print("bus1")
    getBus1(27)

    change(1000, win, sequence, -1)

    #Keep Running the window
    print("showing window")
    win.mainloop()

