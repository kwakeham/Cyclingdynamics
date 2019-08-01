from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import os
import math
from matplotlib import animation

# from basic_units import radians, degrees, cos

DEBUG = True
SHOW = True
SAVE = not SHOW


def log(s):
    if DEBUG:
        print(s)

# with open('file.csv', 'rb') as csvfile:
root = os.path.dirname(os.path.realpath(__file__)) # This gets the current local path
root = root + '\\'
# log(root)
full_root = []
datafiles = []
filename = []
df_name = []

data = []

for file in os.listdir(root): #Finds the data.csv
    if file.endswith("-clean.csv"): # Don't change this, I want the _data.csv files
        filename.append(file)
        full_root.append(root + file)

log(full_root)
begin = False

#select which file that ends in -clean.csv
df = pd.read_csv(full_root[0], sep =',')
# print(df)

raw_timestamp = df['record.timestamp_x[s]']
raw_left_right_balance = df['record.left_right_balance']
raw_cadence = df['record.cadence[rpm]']
raw_accumulated_power = df['record.accumulated_power[watts]']
raw_power = df['record.power[watts]']
raw_left_power_phase = df['record.left_power_phase[degrees]']
raw_left_power_phase_peak = df['record.right_power_phase_peak[degrees]']
raw_right_power_phase = df['record.right_power_phase[degrees]']
raw_right_power_phase_peak = df['record.right_power_phase_peak[degrees]']
raw_left_torque_effectiveness = df['record.left_torque_effectiveness[percent]']
raw_right_torque_effectiveness = df['record.right_torque_effectiveness[percent]']
raw_left_pedal_smoothness = df['record.left_pedal_smoothness[percent]']
raw_right_pedal_smoothness = df['record.right_pedal_smoothness[percent]']

left_power_phase_start = []
left_power_phase_end = []

for x in range(len(raw_left_power_phase)):
    try:
        txt = raw_left_power_phase[x]
        y = txt.split("|")
        left_power_phase_start.append(float(y[0]))
        left_power_phase_end.append(float(y[1]))
    except:
        left_power_phase_start.append(0)
        left_power_phase_end.append(0)

left_power_phase_peak_start = []
left_power_phase_peak_end = []

for x in range(len(raw_left_power_phase_peak)):
    try:
        txt = raw_left_power_phase_peak[x]
        y = txt.split("|")
        left_power_phase_peak_start.append(float(y[0]))
        left_power_phase_peak_end.append(float(y[1]))
    except:
        left_power_phase_peak_start.append(0)
        left_power_phase_peak_end.append(0)


right_power_phase_start = []
right_power_phase_end = []

for x in range(len(raw_right_power_phase)):
    try:
        txt = raw_right_power_phase[x]
        y = txt.split("|")
        right_power_phase_start.append(float(y[0]))
        right_power_phase_end.append(float(y[1]))
    except:
        right_power_phase_start.append(0)
        right_power_phase_end.append(0)

log("length raw_right_power_phase, length right_power_phase_start, length right_power_phase_end")
log(len(raw_right_power_phase))
log(len(right_power_phase_start))
log(len(right_power_phase_end))

right_power_phase_peak_start = []
right_power_phase_peak_end = []

for x in range(len(raw_right_power_phase_peak)):
    try:
        txt = raw_right_power_phase_peak[x]
        y = txt.split("|")
        right_power_phase_peak_start.append(float(y[0]))
        right_power_phase_peak_end.append(float(y[1]))
    except:
        right_power_phase_peak_start.append(0)
        right_power_phase_peak_end.append(0)

log("length raw_right_power_phase_peak, length right_power_phase_peak_start, length right_power_phase_end")
log(len(raw_right_power_phase_peak))
log(len(right_power_phase_peak_start))
log(len(right_power_phase_peak_end))

true_left_right_balance = (raw_left_right_balance-128) 
left_power = (true_left_right_balance/100)*raw_power
right_power = raw_power - left_power
rev_time = 1/(raw_cadence/60)

log("length true_left_right_balance, length left_power, length right_power, length rev_time")
log(len(true_left_right_balance))
log(len(left_power))
log(len(right_power))
log(len(rev_time))



left_phase_start_time = left_power_phase_start*rev_time/360
left_phase_peak_start_time = left_power_phase_peak_start*rev_time/360
left_phase_peak_end_time = left_power_phase_peak_end*rev_time/360
left_phase_end_time = left_power_phase_end*rev_time/360
left_torque_peak_time = (left_phase_peak_start_time + left_phase_peak_end_time)/2

right_phase_start_time = right_power_phase_start*rev_time/360
right_phase_peak_start_time = right_power_phase_peak_start*rev_time/360
right_phase_peak_end_time = right_power_phase_peak_end*rev_time/360
right_phase_end_time = right_power_phase_end*rev_time/360
right_torque_peak_time = (right_phase_peak_start_time + right_phase_peak_end_time)/2


log("length left_phase_start_time, length left_phase_peak_start_time, length left_torque_peak_time, length left_phase_peak_end_time, length left_torque_peak_time")
log(len(left_phase_start_time))
log(len(left_phase_peak_start_time))
log(len(left_torque_peak_time))
log(len(left_phase_peak_end_time))
log(len(left_torque_peak_time))

left_torque_trough_time = []
for i in range(len(left_phase_start_time)):
        try:
                if(left_phase_start_time[i]<left_phase_end_time[i]):
                        left_torque_trough_time.append((rev_time[i]+left_phase_start_time[i]+left_phase_end_time[i])/2)

                else:
                        left_torque_trough_time.append((left_phase_start_time[i]+left_phase_end_time[i])/2)
        except:
                left_torque_trough_time.append(0)
log("length left_torque_trough_time")
log(len(left_torque_trough_time))

right_torque_trough_time = []
for i in range(len(right_phase_start_time)):
        try:
                if(right_phase_start_time[i]<right_phase_end_time[i]):
                        right_torque_trough_time.append((rev_time[i]+right_phase_start_time[i]+right_phase_end_time[i])/2)
                else:
                        right_torque_trough_time.append((right_phase_start_time[i]+right_phase_end_time[i])/2)
        except:
                right_torque_trough_time.append(0)


left_torque_peak_angle = []
for i in range(len(left_power_phase_peak_start)):
        try:
                left_torque_peak_angle.append((left_power_phase_peak_start[i]+left_power_phase_peak_end[i])/2)
        except:
                left_torque_peak_angle.append(0)

right_torque_peak_angle = []
for i in range(len(right_power_phase_peak_start)):
        try:
                right_torque_peak_angle.append((right_power_phase_peak_start[i]+right_power_phase_peak_end[i])/2)
        except:
                right_torque_peak_angle.append(0)

left_torque_trough_angle = []
for i in range(len(left_power_phase_start)):
        try:
                if(left_power_phase_start[i]<left_power_phase_end[i]):
                        left_torque_trough_angle.append((360+left_power_phase_start[i]+left_power_phase_end[i])/2)

                else:
                        left_torque_trough_angle.append((left_power_phase_start[i]+left_power_phase_end[i])/2)
        except:
                left_torque_trough_angle.append(0)

right_torque_trough_angle = []
for i in range(len(right_power_phase_start)):
        try:
                if(right_power_phase_start[i]<right_power_phase_end[i]):
                        right_torque_trough_angle.append((360+right_power_phase_start[i]+right_power_phase_end[i])/2)

                else:
                        right_torque_trough_angle.append((right_power_phase_start[i]+right_power_phase_end[i])/2)
        except:
                right_torque_trough_angle.append(0)



# for i in range(len(left_phase_start_time)):
#         try:
#                 if(left_power_phase_start[i]<left_power_phase_end[i]):
#                         left_torque_trough_angle.append((360+left_power_phase_start[i]+left_power_phase_end[i])/2)
#                 else:
#                         left_torque_trough_angle.append((left_power_phase_start[i]+left_power_phase_end[i])/2)
#         except:
#                 left_torque_trough_angle.append(0)

# right_torque_trough_angle = []
# for i in range(len(right_phase_start_time)):
#         try:
#                 if(right_power_phase_start[i]<right_power_phase_end[i]):
#                         right_torque_trough_angle.append((360+right_power_phase_start[i]+right_power_phase_end[i])/2)
#                 else:
#                         right_torque_trough_angle.append((right_power_phase_start[i]+right_power_phase_end[i])/2)
#         except:
#                 right_torque_trough_angle.append(0)

log("length right_torque_trough_time")
log(len(right_torque_trough_time))

left_torque = left_power/((raw_cadence/60)*2*3.141592)
right_torque = right_power/((raw_cadence/60)*2*3.141592)
left_peak_torque = left_torque/(raw_left_pedal_smoothness/100)
right_peak_torque = right_torque/(raw_right_pedal_smoothness/100)

# print(left_power[50],right_power[50],left_torque[50],right_torque[50])
# print(raw_left_pedal_smoothness[50],raw_right_pedal_smoothness[50],left_peak_torque[50],right_peak_torque[50])

left_phase_start_torque = 0
left_phase_end_torque = 0
right_phase_start_torque = 0
right_phase_end_torque = 0
left_phase_peak_start_torque = left_peak_torque/2
left_phase_peak_end_torque = left_peak_torque/2
right_phase_peak_start_torque = right_peak_torque/2
right_phase_peak_end_torque = right_peak_torque/2

left_torque_trough = []
right_torque_trough = []

for i in range(len(left_phase_start_time)):
        try:
                if(left_phase_start_time[i]<left_phase_end_time[i]):
                        a = (0.5*left_phase_peak_start_torque[i]*(left_phase_peak_start_time[i]-left_phase_start_time[i]))
                        b = (0.5*(left_peak_torque[i]-left_phase_peak_start_torque[i])*(left_torque_peak_time[i]-left_phase_peak_start_time[i]))
                        c = ((left_phase_peak_start_torque[i])*(left_torque_peak_time[i]-left_phase_peak_start_time[i]))
                        d = (0.5*(left_peak_torque[i]-left_phase_peak_end_torque[i])*(left_phase_peak_end_time[i]-left_torque_peak_time[i]))
                        e = ((left_phase_peak_end_torque[i])*(left_phase_peak_end_time[i]-left_torque_peak_time[i]))
                        f = (0.5*left_phase_peak_end_torque[i]*(left_phase_end_time[i]-left_phase_peak_end_time[i]))
                        area_top = a+b+c+d+e+f
                        area_btm = area_top*(1-raw_left_torque_effectiveness[i]/100)
                        left_torque_neg_peak = -area_btm/(left_phase_start_time[i]+rev_time[i]-left_phase_end_time[i])
                        left_torque_trough.append(left_torque_neg_peak)
                        if (i == 48):
                                print(a,b,c,d,e,f)
                                print(raw_left_torque_effectiveness[i],area_top,area_btm, left_peak_torque[i], left_torque_neg_peak)
                else:
                        a = (0.5*left_phase_peak_start_torque[i]*(left_phase_peak_start_time[i]-left_phase_start_time[i]+rev_time[i]))
                        b = (0.5*(left_peak_torque[i]-left_phase_peak_start_torque[i])*(left_torque_peak_time[i]-left_phase_peak_start_time[i]))
                        c = ((left_phase_peak_start_torque[i])*(left_torque_peak_time[i]-left_phase_peak_start_time[i]))
                        d = (0.5*(left_peak_torque[i]-left_phase_peak_end_torque[i])*(left_phase_peak_end_time[i]-left_torque_peak_time[i]))
                        e = ((left_phase_peak_end_torque[i])*(left_phase_peak_end_time[i]-left_torque_peak_time[i]))
                        f = (0.5*left_phase_peak_end_torque[i]*(left_phase_end_time[i]-left_phase_peak_end_time[i]))
                        area_top = a+b+c+d+e+f
                        area_btm = area_top*(1-raw_left_torque_effectiveness[i]/100)
                        left_torque_neg_peak = -area_btm/(left_phase_start_time[i] - left_phase_end_time[i])
                        left_torque_trough.append(left_torque_neg_peak)
                        if (i == 47):
                                print(a,b,c,d,e,f)
                                print(raw_left_torque_effectiveness[i],area_top,area_btm,left_peak_torque[i], left_torque_neg_peak)
        except:
                print(i)
                left_torque_trough.append(0)

for i in range(len(right_phase_start_time)):
        try:
                if(right_phase_start_time[i]<right_phase_end_time[i]):
                        a = (0.5*right_phase_peak_start_torque[i]*(right_phase_peak_start_time[i]-right_phase_start_time[i]))
                        b = (0.5*(right_peak_torque[i]-right_phase_peak_start_torque[i])*(right_torque_peak_time[i]-right_phase_peak_start_time[i]))
                        c = ((right_phase_peak_start_torque[i])*(right_torque_peak_time[i]-right_phase_peak_start_time[i]))
                        d = (0.5*(right_peak_torque[i]-right_phase_peak_end_torque[i])*(right_phase_peak_end_time[i]-right_torque_peak_time[i]))
                        e = ((right_phase_peak_end_torque[i])*(right_phase_peak_end_time[i]-right_torque_peak_time[i]))
                        f = (0.5*right_phase_peak_end_torque[i]*(right_phase_end_time[i]-right_phase_peak_end_time[i]))
                        area_top = a+b+c+d+e+f
                        area_btm = area_top*(1-raw_right_torque_effectiveness[i]/100)
                        right_torque_neg_peak = -area_btm/(right_phase_start_time[i]+rev_time[i]-right_phase_end_time[i])
                        right_torque_trough.append(right_torque_neg_peak)
                        # if (i == 48):
                        #         print(a,b,c,d,e,f)
                        #         print(raw_right_torque_effectiveness[i],area_top,area_btm, right_peak_torque[i], right_torque_neg_peak)
                else:
                        a = (0.5*right_phase_peak_start_torque[i]*(right_phase_peak_start_time[i]-right_phase_start_time[i]+rev_time[i]))
                        b = (0.5*(right_peak_torque[i]-right_phase_peak_start_torque[i])*(right_torque_peak_time[i]-right_phase_peak_start_time[i]))
                        c = ((right_phase_peak_start_torque[i])*(right_torque_peak_time[i]-right_phase_peak_start_time[i]))
                        d = (0.5*(right_peak_torque[i]-right_phase_peak_end_torque[i])*(right_phase_peak_end_time[i]-right_torque_peak_time[i]))
                        e = ((right_phase_peak_end_torque[i])*(right_phase_peak_end_time[i]-right_torque_peak_time[i]))
                        f = (0.5*right_phase_peak_end_torque[i]*(right_phase_end_time[i]-right_phase_peak_end_time[i]))
                        area_top = a+b+c+d+e+f
                        area_btm = area_top*(1-raw_right_torque_effectiveness[i]/100)
                        right_torque_neg_peak = -area_btm/(right_phase_start_time[i] - right_phase_end_time[i])
                        right_torque_trough.append(right_torque_neg_peak)
                        # if (i == 47):
                        #         print(a,b,c,d,e,f)
                        #         print(raw_right_torque_effectiveness[i],area_top,area_btm,right_peak_torque[i], right_torque_neg_peak)
        except:
                print(i)
                right_torque_trough.append(0)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
# ax = plt.axes(xlim=(0, 1), ylim=(-15, 90))
ax = plt.subplot(111, polar=True)
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
# ax.set_rmax(100)
ax.set_rlim(-40,120)
DPI = fig.get_dpi()
fig.set_size_inches(1920.0/float(DPI),1080.0/float(DPI))
plt.xlabel('Angle (s)')
plt.ylabel('Torque N-M')


plotlays, plotcols = [2], ["blue","red"]
lines = []
for index in range(2):
    lobj = ax.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)


# initialization function: plot the background of each frame
def init():
    for line in lines:
        line.set_data([],[])
    return lines

xl,xla,yl = [],[],[]
xr,xra,yr = [],[],[]


# animation function.  This is called sequentially
def animate(i):
        if(left_phase_start_time[i]<left_phase_end_time[i]):
                xl = [left_phase_start_time[i],left_phase_peak_start_time[i],left_torque_peak_time[i],left_phase_peak_end_time[i],left_phase_end_time[i],left_torque_trough_time[i],(left_phase_start_time[i]+rev_time[i])]
                xla = [left_power_phase_start[i],left_power_phase_peak_start[i],left_torque_peak_angle[i],left_power_phase_peak_end[i],left_power_phase_end[i],left_torque_trough_angle[i],(left_power_phase_start[i]+360)]
                xla_radians = []
                for z in range(len(xla)):
                        xla_radians.append(xla[z]*3.141592/180)
                yl = [left_phase_start_torque,left_phase_peak_start_torque[i],left_peak_torque[i],left_phase_peak_end_torque[i],left_phase_end_torque,left_torque_trough[i],left_phase_start_torque]

        else:
                xl = [(left_phase_start_time[i]-rev_time[i]),left_phase_peak_start_time[i],left_torque_peak_time[i],left_phase_peak_end_time[i],left_phase_end_time[i],left_torque_trough_time[i],(left_phase_start_time[i])]
                xla = [(left_power_phase_start[i]-360),left_power_phase_peak_start[i],left_torque_peak_angle[i],left_power_phase_peak_end[i],left_power_phase_end[i],left_torque_trough_angle[i],(left_power_phase_start[i])]
                xla_radians = []
                for z in range(len(xla)):
                        xla_radians.append(xla[z]*3.141592/180)
                yl = [left_phase_start_torque,left_phase_peak_start_torque[i],left_peak_torque[i],left_phase_peak_end_torque[i],left_phase_end_torque,left_torque_trough[i],left_phase_start_torque]

        if(right_phase_start_time[i]<right_phase_end_time[i]):
                xr = [right_phase_start_time[i],right_phase_peak_start_time[i],right_torque_peak_time[i],right_phase_peak_end_time[i],right_phase_end_time[i],right_torque_trough_time[i],(right_phase_start_time[i]+rev_time[i])]
                xra = [right_power_phase_start[i],right_power_phase_peak_start[i],right_torque_peak_angle[i],right_power_phase_peak_end[i],right_power_phase_end[i],right_torque_trough_angle[i],(right_power_phase_start[i]+360)]
                xra_radians = []
                for z in range(len(xra)):
                        xra_radians.append(xra[z]*3.141592/180)
                yr = [right_phase_start_torque,right_phase_peak_start_torque[i],right_peak_torque[i],right_phase_peak_end_torque[i],right_phase_end_torque,right_torque_trough[i],right_phase_start_torque]

        else:
                xr = [(right_phase_start_time[i]-rev_time[i]),right_phase_peak_start_time[i],right_torque_peak_time[i],right_phase_peak_end_time[i],right_phase_end_time[i],right_torque_trough_time[i],(right_phase_start_time[i])]
                xra = [(right_power_phase_start[i]-360),right_power_phase_peak_start[i],right_torque_peak_angle[i],right_power_phase_peak_end[i],right_power_phase_end[i],right_torque_trough_angle[i],(right_power_phase_start[i])]
                xra_radians = []
                for z in range(len(xra)):
                        xra_radians.append(xra[z]*3.141592/180)
                yr = [right_phase_start_torque,right_phase_peak_start_torque[i],right_peak_torque[i],right_phase_peak_end_torque[i],right_phase_end_torque,right_torque_trough[i],right_phase_start_torque]



        xlist = [xla_radians, xra_radians]
        ylist = [yl, yr]

            #for index in range(0,1):
        for lnum,line in enumerate(lines):
                line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 
        # line.set_data(x, y)
        return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(left_phase_start_time), interval=100, blit=True)

anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

# for i in range(len(left_phase_start_time)):
#         if(left_phase_start_time[i]<left_phase_end_time[i]):
#                 x = [left_phase_start_time[i],left_phase_peak_start_time[i],left_torque_peak_time[i],left_phase_peak_end_time[i],left_phase_end_time[i],left_torque_trough_time[i],(left_phase_start_time[i]+rev_time[i])]
#                 xla = [left_power_phase_start[i],left_power_phase_peak_start[i],left_torque_peak_angle[i],left_power_phase_peak_end[i],left_power_phase_end[i],left_torque_trough_angle[i],(left_power_phase_start[i]+360)]
#                 xla_radians = []
#                 for z in range(len(xla)):
#                         xla_radians.append(xla[z]*3.141592/180)
#                 # xla = 3.1415*xla/180
#                 y = [left_phase_start_torque,left_phase_peak_start_torque[i],left_peak_torque[i],left_phase_peak_end_torque[i],left_phase_end_torque,left_torque_trough[i],left_phase_start_torque]
#                 plt.figure(1)
#                 ax = plt.subplot(111, polar=True)
#                 ax.set_theta_zero_location("N")
#                 ax.set_rlim(-40,120)
#                 plt.plot(xla_radians,y, color='blue',linewidth=3)
#                 print(xla)
#                 print(y)
#                 plt.show()
#                 # input("Press Enter to continue...")
#         else:
#                 x = [(left_phase_start_time[i]-rev_time[i]),left_phase_peak_start_time[i],left_torque_peak_time[i],left_phase_peak_end_time[i],left_phase_end_time[i],left_torque_trough_time[i],(left_phase_start_time[i])]
#                 xla = [(left_power_phase_start[i]-360),left_power_phase_peak_start[i],left_torque_peak_angle[i],left_power_phase_peak_end[i],left_power_phase_end[i],left_torque_trough_angle[i],(left_power_phase_start[i])]
#                 xla_radians = []
#                 for z in range(len(xla)):
#                         xla_radians.append(xla[z]*3.141592/180)
#                 y = [left_phase_start_torque,left_phase_peak_start_torque[i],left_peak_torque[i],left_phase_peak_end_torque[i],left_phase_end_torque,left_torque_trough[i],left_phase_start_torque]
#                 plt.figure(1)
#                 ax = plt.subplot(111, polar=True)
#                 ax.set_theta_zero_location("N")
#                 ax.set_rlim(-40,120)
#                 plt.plot(xla_radians,y, color='blue',linewidth=3)
#                 print(xla)
#                 print(y)
#                 plt.show()
#                 # input("Press Enter to continue...")

