import json
import sys

# Get parameters to look up in JSON file.
def getParameters(arg):
    n = len(arg)
    if n != 5:
        print("Parameters not provided as arguments, please input manually:")
        distance = input("Please enter distance in NM: ")
        weight = input("Please enter weight in pounds: ")
        height = input("Please enter height in feet: ")
        temperature= input("Please enter temperature in celcius: ")
    else:
        distance = float(arg[1])
        weight = float(arg[2])
        height = float(arg[3])
        temperature = float(arg[4])
    print("Using parameters: distance", distance, "NM, weight", weight,"lbs, height", height, "feet, and temperature", temperature, "celcius.")
    return distance,weight,height,temperature

# Function to choose a dcitionary from a list of dictionaries, based on a key,value pair.
def getDict(dictionary_list,key,value):
    for dictionary in dictionary_list:
        if dictionary[key] == value:
            return dictionary

# Load JSON file into dictionary
planeDataFile = 'Cirrus SR22 G1 (1).json'
planeData = json.loads(open(planeDataFile).read())

distance,weight,height,temperature = getParameters(sys.argv)

# Find relevant data in list.
tmpDict = planeData.get("cruise")[0].get("weights")
tmpDict = getDict(tmpDict, "weight_lbs", weight)
tmpDict = getDict(tmpDict.get("temperatures"), "disa_c", temperature)
tmpDict = getDict(tmpDict.get("cruisePoints"), "altitude_ft", height)
speed = tmpDict.get("speed_ktas")
fuelFlow = tmpDict.get("fuelFlow_pph")

flightTime = distance/speed
fuelUse = flightTime*fuelFlow

print("Flgiht time is", '{0:02.0f}:{1:02.0f}'.format(*divmod(flightTime * 60, 60)), "hours and fuel use is", '{0:.3f}'.format(fuelUse), "lbs." )
