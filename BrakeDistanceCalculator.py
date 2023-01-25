'''
Coding assignement - Brake distance simulation

Johannes Aumayr
s2210710043

NOTE: There might be similarities in the code and the sources with Mr. Hoffmann's coding submission due to discussion and alignments. Anyhow, coding was done independently.
'''

# libaries
import numpy as np
import math
from importlib.metadata import metadata
import matplotlib as mpl    
import matplotlib.pyplot as plt
#----
#copy code
#source: https://stackoverflow.com/questions/5484922/secondary-axis-with-twinx-how-to-add-to-legend
from matplotlib import rc
rc('mathtext', default='regular')
#endcopy
#----

# prompt user and programm discription
print("Deceleration and brake distance calculator V1.0\n")
print("Based on the velocity of a vehicle, the road inclination and road surface and road condition, the calculator will determine the brake distance.")

# functions
def distanceRoT(v): # returns a brake distance with a rough estimation with a rule of thumb
     sRoT = pow(v/10, 2)
     return sRoT
     
def maxTimeFunc(my, v, ang): #returns time of v=0 based on the given inclination angle, the actual velocity and the actual coefficient of friction
    g = 9.81
    aMax = my * g * math.cos(math.radians(ang)) + g * math.sin(math.radians(ang))       # Comment: Mass does not go into equation!
    return v / aMax

def aMaxFunc(my, ang): # returns the maximum available accelearation based on the given inclination angle and the actual coefficient of friction
    g = 9.81
    aMax = my * g * math.cos(math.radians(ang)) + g * math.sin(math.radians(ang))       # Comment: Mass does not go into equation!
    return aMax

def calcDis(surface, condition, angle, vCalc): # Selection of right friction + calculation of distance and velocity
    myStatic = [0.65, 0.4, 0.2, 0.1, 0.1, 0, 0]
    myDynamic = [0.5, 0.35, 0.15, 0.08, 0.05, 0.35, 0.3]

    if surface == "concrete" and condition == "dry":
        myCalc = [myStatic[0], myDynamic[0]]
    elif surface == "concrete" and condition == "wet":
        myCalc = [myStatic[1], myDynamic[1]]
    elif surface == "ice" and condition == "dry":
        myCalc = [myStatic[2], myDynamic[2]]
    elif surface == "ice" and condition == "wet":
        myCalc = [myStatic[3], myDynamic[3]]
    elif surface == "water":
        myCalc = [myStatic[4], myDynamic[4]]
    elif surface == "gravel":
        myCalc = [myStatic[5], myDynamic[5]]
    elif surface == "sand":
        myCalc = [myStatic[6], myDynamic[6]]
    else:
        print("Something gone wrong!")
    
    # call maxTime fuction for time of v0
    t = maxTimeFunc((myCalc[0] + myCalc[1]), vCalc, angle)    
    #print(myCalcDis)
    #print(vCalc, "m/s")
    #print(t, "s")
    tRounded = abs(math.ceil(t))                                       #source of math methode: https://codegree.de/runden-in-python/                   
    timeVector = np.arange(0, tRounded, 0.1)                           #source for numpy methode: https://pynative.com/python-range-for-float-numbers/
    disVector = [None] * len(timeVector)                               #source for creating an empty list: https://stackoverflow.com/questions/10712002/create-an-empty-list-with-certain-size-in-python
    vVector = [None] * len(timeVector)                                 #source unpacking operator *:https://www.geeksforgeeks.org/range-to-a-list-in-python/
    vVector[0] = vCalc
    
    i = 0
    while i < len(timeVector):
        timeInt = timeVector[1] - timeVector[0]
        disVector[i] = vCalc * timeVector[i] - 1/2 * aMaxFunc((myCalc[0] + myCalc[1]), angle) * pow(timeVector[i], 2)  #source: https://austria-forum.org/af/AustriaWiki/Bremsweg
        if vVector[i] <= 0:
            break
        vVector[i+1] = vVector[i] - aMaxFunc((myCalc[0] + myCalc[1]), angle) * timeInt
        i += 1
    #print(timeVector, "[s]")
    #print(disVector, "[m]")
    #print(vVector, "m/s")
    return timeVector, disVector, vVector, tRounded

def plotFunction(t, s, v, tMax, sRoT): #plots the linearly decreasing velocity, calculated and estimated braking distance over time
    # plot results
    #----
    #copy code
    #source: https://stackoverflow.com/questions/5484922/secondary-axis-with-twinx-how-to-add-to-legend
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    lns1 = ax1.plot(t, s, label = 'Brake distance', color = 'r')
    lns2 = ax1.plot(t, sRoTVector, label = 'Estimated distance w. rule of thumb', color = 'g')
    #lns2 = ax1.scatter(tMax, sRoT, label = 'rule of thumb', color = 'g')
    ax2 = ax1.twinx()
    lns3 = ax2.plot(t, v, label = 'velocity', color = 'b')
    # added these three lines
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(loc=0)
    ax2.legend(loc=0)    
    ax1.grid()
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Distance [m]', color = 'r')
    ax2.set_ylabel('Velocity [m/s]', color = 'b')
    ax1.set_ylim(0, )
    ax2.set_ylim(0, )
    ax1.set_xlim(0, )
    #ax2.set_ylim(0, )
    #end copy
    #----
    plt.title("Velocity and Distance over Time")
    plt.savefig(fileName, format = None, metadata=None)                    #source for safe with filneame: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
    plt.show()    

# gather information + main program
vKph = int(input ("Enter a velocity (1-300kph): "))
if vKph >= 0 and vKph <= 300:
    incAngle = int(input("Enter a positive inclination angle (0-45deg): "))
    if incAngle >= 0 and incAngle <= 45:
        roadSur = input("Enter a road surface type between (concrete, ice, water, gravel or sand): ")
        if roadSur == "concrete" or roadSur == "ice" or roadSur == "water" or roadSur == "gravel" or roadSur == "sand":
            roadCond = input("Enter a road condition between (dry, wet):")
            if roadCond == "dry" or roadCond == "wet":
                print("Thank you for your selection")
                vMetric = vKph / 3.6
                fileName = 'Decelaration_' + str(vKph) + 'kph' + '_' + str(incAngle) + 'degree' + '_' + roadSur + '_' + roadCond   #source for concatinate strings: https://note.nkmk.me/en/python-string-concat/
                
                #call function to calculate distances
                calcMatrix = calcDis(roadSur, roadCond, incAngle, vMetric)
                t = calcMatrix[0]
                s = calcMatrix[1]
                v = calcMatrix[2]
                tMax = calcMatrix[3]

                # call rule of thumb function
                sRoT = distanceRoT(vKph)
                sRoTVector = [sRoT] * len(t)

                # call plot function
                plotFunction(t, s, v, tMax, sRoT)
            else:
                print("You entered a wrong word!")
        else:
            print("You entered a wrong word!") 
    else:
        print("You entered a wrong number!") 
else:
    print("You entered a wrong number!")

