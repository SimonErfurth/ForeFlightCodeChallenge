import json
import sys


# Get parameters to look up in JSON file, if provided.
def getParameters(arg):
    n = len(arg)
    if n != 5:
        print("Parameters not provided as arguments, please input manually:")
        distance = float(input("Please enter distance in NM: "))
        weight = float(input("Please enter weight in pounds: "))
        height = float(input("Please enter height in feet: "))
        temperature = float(input("Please enter temperature in celcius: "))
    else:
        distance = float(arg[1])
        weight = float(arg[2])
        height = float(arg[3])
        temperature = float(arg[4])
    print(
        "Using parameters: distance",
        distance,
        "NM, weight",
        weight,
        "lbs, height",
        height,
        "feet, and temperature",
        temperature,
        "celcius.",
    )
    return distance, weight, height, temperature


# Choose a dictionary from a list of dictionaries, based on a key,value pair.
def getDict(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if dictionary.get(key) == value:
            return dictionary


# Return list of possible values for key in the dictionaries in dictionary_list
def getDictValues(dictionary_list, key):
    res = []
    for dictionary in dictionary_list:
        res.append(dictionary.get(key))
    return res


# From a list of dictionaries, return the dictionary with the key-value closest
# to target_value. Note that we need to check all, since the list might not be
# sorted. Might be worth preprocessing it?
def getClosestDict(dictionary_list, key, target_value):
    options = getDictValues(dictionary_list, key)
    minDist = abs(target_value - options[0])
    dictionary = dictionary_list[0]
    for i in range(1, len(options)):
        if abs(target_value - options[i]) < minDist:
            minDist = abs(target_value - options[i])
            dictionary = dictionary_list[i]
    return dictionary


# Solving main part of challenge
def getSingleFlightTimeAndFuelUse(planeData, distance, weight, height, temperature):
    # Find relevant values in planeData.
    tmpDict = planeData.get("cruise")[0]
    tmpDict = getClosestDict(tmpDict.get("weights"), "weight_lbs", weight)
    tmpDict = getClosestDict(tmpDict.get("temperatures"), "disa_c", temperature)
    tmpDict = getClosestDict(tmpDict.get("cruisePoints"), "altitude_ft", height)
    speed = tmpDict.get("speed_ktas")
    fuelFlow = tmpDict.get("fuelFlow_pph")

    # Calculate flight time and fuel use, and printreturn result.
    flightTime = distance / speed
    fuelUse = flightTime * fuelFlow
    return flightTime, fuelUse


# Load JSON file into dictionary planeData
planeDataFileName = "Cirrus SR22 G1 (1).json"
planeData = json.loads(open(planeDataFileName).read())

flightTime, fuelUse = getSingleFlightTimeAndFuelUse(planeData, *getParameters(sys.argv))
print(
    "Flgiht time is",
    "{0:02.0f}:{1:02.0f}".format(*divmod(flightTime * 60, 60)),
    "hours and fuel use is",
    "{0:.3f}".format(fuelUse),
    "lbs.",
)


###
### Here starts code only related to the optional challenge.
###


def optionalChallenge(planeData, distance, weights, temperatures):
    for weight in weights:
        for temperature in temperatures:
            # To avoid repeating the next two calls with the same value, we
            # could instead rename tmpDict for each level. This would be a
            # tradeoff where we instead use more memory.
            tmpDict = planeData.get("cruise")[0]
            tmpDict = getClosestDict(tmpDict.get("weights"), "weight_lbs", weight)
            tmpDict = getClosestDict(tmpDict.get("temperatures"), "disa_c", temperature)
            # Retrieve known altitude options for this weight/temperature.
            altitude_options = getDictValues(tmpDict.get("cruisePoints"), "altitude_ft")
            # Use the first altitude option to find starting values.
            flightTime, fuelUse = getSingleFlightTimeAndFuelUse(
                planeData, distance, weight, altitude_options[0], temperature
            )
            minTime = flightTime
            minFuel = fuelUse
            minTimeAlt = minFuelAlt = altitude_options[0]
            # Check if any other altitude option is faster/more fuel efficient.
            for i in range(1, len(altitude_options)):
                flightTime, fuelUse = getSingleFlightTimeAndFuelUse(
                    planeData, distance, weight, altitude_options[i], temperature
                )
                if flightTime < minTime:
                    minTime = flightTime
                    minTimeAlt = altitude_options[i]
                if fuelUse < minFuel:
                    minFuel = fuelUse
                    minFuelAlt = altitude_options[i]
            # Print fastest and most fuel efficient option.
            print(
                "Weigth:",
                weight,
                "lbs.; Temperature:",
                temperature,
                "celsius.\n",
                "    Minimal flight time is",
                "{0:02.0f}:{1:02.0f}".format(*divmod(minTime * 60, 60)),
                "hours at",
                minTimeAlt,
                "feet.\n",
                "    Minimal fuel use is",
                "{0:.3f}".format(minFuel),
                "lbs. at",
                minFuelAlt,
                "feet.",
            )


# optionalChallenge(planeData, 1337, [3000, 4200], [10, 2, -10])
