import json
import sys

# Get parameters to look up in JSON file, if provided.
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

# Choose a dcitionary from a list of dictionaries, based on a key,value pair.
def getDict(dictionary_list,key,value):
    for dictionary in dictionary_list:
        if dictionary.get(key) == value:
            return dictionary

# Return list of possible values for key in the dictionaries in dictionary_list
def getDictValues(dictionary_list,key):
    res = []
    for dictionary in dictionary_list:
        res.append(dictionary.get(key))
    return res

# From a list of dictionaries, return the dictionary with the key-value closest to target_value.
# Note that we need to check all, since the list might not be sorted.
def getClosestDict(dictionary_list,key,target_value):
    options = getDictValues(dictionary_list,key)
    minDist = abs(target_value - options[0])
    dictionary = dictionary_list[0]
    for i in range(1,len(options)):
        if abs(target_value - options[i]) < minDist:
            minDist = abs(target_value - options[i])
            dictionary = dictionary_list[i]
    return dictionary

# Load JSON file into dictionary
planeDataFileName = 'Cirrus SR22 G1 (1).json'
planeData = json.loads(open(planeDataFileName).read())

distance,weight,height,temperature = getParameters(sys.argv)

# Find relevant data in list.
tmpDict = planeData.get("cruise")[0]
tmpDict = getClosestDict(tmpDict.get("weights"), "weight_lbs", weight)
tmpDict = getClosestDict(tmpDict.get("temperatures"), "disa_c", temperature)
tmpDict = getClosestDict(tmpDict.get("cruisePoints"), "altitude_ft", height)
speed = tmpDict.get("speed_ktas")
fuelFlow = tmpDict.get("fuelFlow_pph")

# Calculate flight time and fuel use, and print result.
flightTime = distance/speed
fuelUse = flightTime*fuelFlow
print("Flgiht time is", '{0:02.0f}:{1:02.0f}'.format(*divmod(flightTime * 60, 60)), "hours and fuel use is", '{0:.3f}'.format(fuelUse), "lbs." )
