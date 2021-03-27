import os
import time
import random
from datetime import datetime
#import RPi.GPIO as GPIO
from threading import Thread
from tkinter import *
import tkinter
from PIL import ImageTk, Image
from tkinter.ttk import Combobox
from tkinter import messagebox


##########################################################################################################
"""
    CONFIG RASPBERRY PI ZERO
"""

##########################################################################################################
# #select type serial is BCM
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# # setup chanel raspberry pi zero
# #Chanel IN
# GPIO.setup( 12 , GPIO.IN) # input status Air1
# GPIO.setup( 16 , GPIO.IN) # input status Air2
# GPIO.setup( 17 , GPIO.IN) # input temphumi

# #Chanel OUT
# GPIO.setup( 5 , GPIO.OUT) #Air1
# GPIO.setup( 6 , GPIO.OUT) #Air2
# GPIO.setup( 13, GPIO.OUT) #Air3
# GPIO.setup( 26, GPIO.OUT) #Air4

##########################################################################################################
"""
    INITIAL VALUES
"""

##########################################################################################################
# default values for controller
now = datetime.now()
inputvaluelist = {
    "initialTime": datetime.now().strftime("%H:%M:%S"),
    "timeRun": 4,
    "timeStop": 22,
    "timeCycle": 1,
    "mode": "Time",
    "tempRun": 30,
    "tempStop": 15,
    "tempNomal": 20,
    "tempHigh": 45,
    "btnAir1": 0,
    "btnAir2": 0,
    "returntemp": 0
}

listMode = ["Time", 'Temp', 'Manual']
listCycle = ["1"]
for cyc in range(1, 301):
    if cyc % 5 == 0:
        listCycle.append(cyc)
listTime = []
for time in range(0, 24):
    listTime.append(time)
listTemp = []
for i in range(0, 100):
    listTemp.append(i)


##########################################################################################################
"""
    FUNCTION HANDLE
"""

##########################################################################################################
# handle output relay


def onchange(data):
    temperature_return = random.randint(0, 100)
    if data["mode"].lower() == "time":
        if temperature_return >= data["tempHigh"]:
            print("run 2 Air")
            #GPIO.output( 5, GPIO.HIGH)
            #GPIO.output( 6, GPIO.HIGH)
        elif (temperature_return <= data["tempRun"]):
            if data["timeRun"] > data["timeStop"]:
                if data["timeRun"] > now.hour and data["timeStop"] <= now.hour:
                    thread = Thread(target=funcion_stop_time)
                    thread.start()
                else:
                    thread = Thread(target=funcion_run_time, args=(
                        data["timeCycle"], data["initialTime"],))
                    thread.start()
            else:
                if data["timeRun"] <= now.hour and data["timeStop"] > now.hour:
                    thread = Thread(target=funcion_run_time, args=(
                        data["timeCycle"], data["initialTime"],))
                    thread.start()
                else:
                    thread = Thread(target=funcion_stop_time)
                    thread.start()

    elif data["mode"].lower() == "temp":
        if temperature_return >= data["tempHigh"]:
            print("run 2 Air")
            #GPIO.output( 5, GPIO.HIGH)
            #GPIO.output( 6, GPIO.HIGH)
        elif temperature_return <= data["tempRun"] and temperature_return >= data["tempStop"]:
            print("run two Air luan phien")
            thread = Thread(target=funcion_run_time, args=(
                data["timeCycle"], data["initialTime"],))
            thread.start()
        elif temperature_return < data["tempStop"]:
            print("Off all Air")
            #GPIO.output( 5, GPIO.LOW)
            #GPIO.output( 6, GPIO.lOW)

    elif data["mode"].lower() == "manual":
        if data["btnAir1"] == 1:
            #GPIO.output( 5, GPIO.HIGH)
            print("nanual running Air 1")
        elif data["btnAir1"] == 0:
            #GPIO.output( 5, GPIO.LOW)
            print("nanual stoping Air 1")
        if data["btnAir2"] == 1:
            #GPIO.output( 6, GPIO.HIGH)
            print("nanual running Air 2")
        elif data["btnAir2"] == 0:
            #GPIO.output( 6, GPIO.LOW)
            print("nanual stoping Air 2")


# handle mode time


def funcion_run_time(time_cycle, initial_time):
    time_now = datetime.now().strftime("%H:%M:%S")
    initial_time_seconds = convert_to_seconds(initial_time)
    time_now_seconds = convert_to_seconds(time_now)
    results = (time_now_seconds - initial_time_seconds)//(time_cycle*60)+1
    print(time_now)
    print(results)
    if results % 2 == 0:
        #GPIO.output( 5, GPIO.LOW)
        #GPIO.output( 6, GPIO.HIGH)
        print("chay dieu hoa 2")
    else:
        #GPIO.output( 6, GPIO.LOW)
        #GPIO.output( 5, GPIO.HIGH)
        print("chay dieu hoa 1")


def funcion_stop_time():
    #GPIO.output( 6, GPIO.LOW)
    #GPIO.output( 5, GPIO.LOW)
    print("stop")

# handle convert time to string time_cycle


def converTimeToDict(time):
    data = {
        "hour": int(time.split(":")[0]),
        "minute": int(time.split(":")[1]),
        "seconds": int(time.split(":")[2])
    }
    return data
# handle convert time to seconds


def convert_to_seconds(time):
    result = converTimeToDict(time)
    result = result['hour']*3600 + result['minute']*60 + result['seconds']
    return result


##########################################################################################################
"""
    READ VALUE RETURN
"""
##########################################################################################################


def read_value_return():
    # inputvaluelist["returntemp"] = random.randrange(0, 100, 4)
    inputvaluelist["returntemp"] = random.randrange(19, 30)
    data = {
        "status_air_01": "",
        "status_air_02": ""
    }
    #statusAir01 = GPIO.input(12)
    statusAir01 = 0
    if statusAir01 > -1:
        if statusAir01 == 1:
            print("bật air 01")
            data["status_air_01"] = "ON"
        else:
            print("Tat air 01")
            data["status_air_01"] = "OFF"
    #statusAir02 = GPIO.input(16)
    statusAir02 = 1
    if statusAir02 > -1:
        if statusAir02 == 1:
            print("bật air 02")
            data["status_air_02"] = "ON"
        else:
            print("Tat air 02")
            data["status_air_02"] = "OFF"
    return data


##########################################################################################################
"""
    CONFIG WINDOW FORM
"""
##########################################################################################################
window = Tk()
# mywin=MyWindow(window)
_width = 600
_height = 300
# info screen
width_screen = window.winfo_screenwidth()
height_screen = window.winfo_screenheight()
# caculator screen center
posx = width_screen/2 - _width/2
posy = height_screen/2 - _height/2
window.title('Controller Air')

top_frame = LabelFrame(window, width=600, height=40).grid(row=0, columnspan=5)
# add logo ems
img = Image.open('ems_logo.png')
img = img.resize((60, 30), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(top_frame, image=img).grid(row=0, column=0)
Label(top_frame, text="Controller Air", fg='red',
      font=("Arial Bold", 15)).grid(row=0, column=2)

# overview
overview_frame1 = Frame(window, width=600, height=20).grid(row=1, columnspan=5)
lbl1 = Label(overview_frame1, text="Temperaturn:",
             font=("Arial Bold", 8)).grid(row=1, column=0)
lbl2 = Label(overview_frame1, text="35*C",
             font=("Arial Bold", 8))
lbl2.grid(row=1, column=1)
lbl3 = Label(overview_frame1, text="Mode:", font=(
    "Arial Bold", 8))
lbl3.grid(row=1, column=3)
lbl4 = Label(overview_frame1, text="TIME", font=(
    "Arial Bold", 8))
lbl4.grid(row=1, column=4)
overview_frame2 = Frame(window, width=600, height=20).grid(row=2, columnspan=5)
lbl5 = Label(overview_frame2, text="Status Air I:",
             font=("Arial Bold", 8))
lbl5.grid(row=2, column=0)
lbl6 = Label(overview_frame2, text="ON:", font=(
    "Arial Bold", 8))
lbl6.grid(row=2, column=1)
lbl7 = Label(overview_frame2, text="Status Air II:",
             font=("Arial Bold", 8))
lbl7.grid(row=2, column=3)
lbl8 = Label(overview_frame2, text="OFF", font=(
    "Arial Bold", 8))
lbl8.grid(row=2, column=4)

# setting mode
center = LabelFrame(window, text="Setting mode", width=580, height=180, font=(
    "Arial Bold", 10), pady=10).grid(row=3, columnspan=5, rowspan=6)
lbl9 = Label(center, text="Time Run:", font=(
    "Arial Bold", 8)).grid(column=0, row=4)
lbl10 = Label(center, text="Time Stop:", font=(
    "Arial Bold", 8)).grid(column=0, row=5)
lbl11 = Label(center, text="Time Cycle:", font=(
    "Arial Bold", 8)).grid(column=0, row=6)
lbl12 = Label(center, text="Mode:", font=(
    "Arial Bold", 8)).grid(column=0, row=7)

cbox_01 = Combobox(center, values=listTime, width=8, font=("Arial Bold", 8))
cbox_01.insert(0, '4')
cbox_01.grid(column=1, row=4)
cbox_02 = Combobox(center, values=listTime, width=8, font=("Arial Bold", 8))
cbox_02.insert(0, '22')
cbox_02.grid(column=1, row=5)
cbox_03 = Combobox(center, values=listCycle, width=8, font=("Arial Bold", 8))
cbox_03.insert(0, '15')
cbox_03.grid(column=1, row=6)
cbox_04 = Combobox(center, values=listMode, width=8, font=("Arial Bold", 8))
cbox_04.insert(0, 'Time')
cbox_04.grid(column=1, row=7)
lbl13 = Label(center, text="Temp Run:", font=(
    "Arial Bold", 8)).grid(column=3, row=4)
lbl14 = Label(center, text="Temp Stop:", font=(
    "Arial Bold", 8)).grid(column=3, row=5)
lbl15 = Label(center, text="Temp Nomal:", font=(
    "Arial Bold", 8)).grid(column=3, row=6)
lbl16 = Label(center, text="Temp High", font=(
    "Arial Bold", 8)).grid(column=3, row=7)

cbox_05 = Combobox(center, values=listTemp, width=8, font=("Arial Bold", 8))
cbox_05.insert(0, '30')
cbox_05.grid(column=4, row=4)
cbox_06 = Combobox(center, values=listTemp, width=8, font=("Arial Bold", 8))
cbox_06.insert(0, '15')
cbox_06.grid(column=4, row=5)
cbox_07 = Combobox(center, values=listTemp, width=8, font=("Arial Bold", 8))
cbox_07.insert(0, '20')
cbox_07.grid(column=4, row=6)
cbox_08 = Combobox(center, values=listTemp, width=8, font=("Arial Bold", 8))
cbox_08.insert(0, '45')
cbox_08.grid(column=4, row=7)


# handel buttons


def handleCancel():
    labelResult.configure(text="Action cancel !")
    return


def handleSetup():
    inputvaluelist["initialTime"] = datetime.now().strftime("%H:%M:%S")
    inputvaluelist["timeRun"] = int(cbox_01.get())
    inputvaluelist["timeStop"] = int(cbox_02.get())
    inputvaluelist["timeCycle"] = int(cbox_03.get())
    inputvaluelist["mode"] = cbox_04.get()
    inputvaluelist["tempRun"] = int(cbox_05.get())
    inputvaluelist["tempStop"] = int(cbox_06.get())
    inputvaluelist["tempNomal"] = int(cbox_07.get())
    inputvaluelist["tempHigh"] = int(cbox_08.get())
    labelResult.configure(text="result")
    messagebox.showinfo("Notification", "result")
    window.focus_set()
    labelResult.configure(text='')
    return


def handleCheckBox():
    if(inputvaluelist["mode"].lower() == 'manual'):
        inputvaluelist["btnAir1"] = checkvar1.get()
        inputvaluelist["btnAir2"] = checkvar2.get()


btnSetup = Button(center, text="Setup", fg='green', width=10, font=(
    "Arial Bold", 8), command=handleSetup).grid(column=0, row=8)
btnCancel = Button(center, text="Cancel", fg='red', width=10, font=(
    "Arial Bold", 8), command=handleCancel).grid(column=1, row=8)
labelResult = Label(center, text="", font=("Arial Bold", 8))
labelResult.grid(column=2, row=8)
checkvar1 = IntVar()
checkvar2 = IntVar()
ch_box_01 = Checkbutton(center, text="Air I", variable=checkvar1,
                        onvalue=1, offvalue=0, height=2, width=8, command=handleCheckBox)
ch_box_01.grid(column=3, row=8)
ch_box_02 = Checkbutton(center, text="Air II", variable=checkvar2,
                        onvalue=1, offvalue=0, height=2, width=8, command=handleCheckBox)
ch_box_02.grid(column=4, row=8)


# bottom layout
bottom = LabelFrame(window, bg='red', width=580,
                    height=35).grid(row=10, columnspan=5)
lblTime = Label(bottom, text=datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"), bg='red', fg="yellow", font=("Arial Bold", 10))
lblTime.grid(row=10, column=2)


# *****************************************************************************************************
"""
        handel update data realtime
"""

# *****************************************************************************************************


def update_realtime():
    value = read_value_return()
    currentime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lblTime.config(text=currentime)
    lbl2.config(text=inputvaluelist['returntemp'])
    lbl4.config(text=inputvaluelist['mode'])
    lbl6.config(text=value['status_air_01'])
    lbl8.config(text=value['status_air_02'])
    onchange(inputvaluelist)
    lblTime.after(1000, update_realtime)


# **********************************************************************************************************
"""
MAIN Processor"""
# **********************************************************************************************************


def main():
    try:
        update_realtime()
        window.resizable(True, True)
        window.geometry("%dx%d+%d+%d" % (_width, _height, posx, posy))
        window.mainloop()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
